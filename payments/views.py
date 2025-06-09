from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum, Q
import re
import uuid
import logging

from .models import Payment, PaymentLog
from .serializers import PaymentSerializer, EarningsSerializer

logger = logging.getLogger(__name__)

class PaymentThrottle(UserRateThrottle):
    rate = '10/minute'

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [PaymentThrottle]

    def validate_payment_input(self, payment_method, phone_number, card_number):
        if payment_method not in ['mpesa', 'vodacom', 'airtel', 'mtn', 'card']:
            raise ValidationError("Invalid payment method")
        if payment_method == 'card' and not card_number:
            raise ValidationError("Card number is required for card payments")
        if payment_method != 'card' and not phone_number:
            raise ValidationError("Phone number is required for mobile payments")
        if phone_number and not re.match(r'^\+25[45]\d{9}$', phone_number):
            raise ValidationError("Invalid phone number format. Use +254 or +255 followed by 9 digits.")
        if card_number and not re.match(r'^\d{16}$', card_number):
            raise ValidationError("Invalid card number format. Use 16 digits.")

    def handle_simulated_payment(self, payment, phone_number, card_number):
        try:
            PaymentLog.objects.create(
                payment=payment,
                action='processed',
                details={
                    'method': payment.payment_method,
                    'phone_number': phone_number,
                    'card_number': card_number
                }
            )
            return {'status': 'success', 'message': f"Simulated {payment.payment_method} payment successful."}
        except Exception as e:
            logger.error(f"Simulated payment error: {str(e)}")
            PaymentLog.objects.create(
                payment=payment,
                action='failed',
                details={'error': str(e)}
            )
            raise ValidationError("Simulated payment failed.")

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):
        content_type_id = request.data.get('content_type_id')
        object_id = request.data.get('object_id')
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method', 'mpesa')
        phone_number = request.data.get('phone_number')
        card_number = request.data.get('card_number')
        idempotency_key = request.data.get('idempotency_key')

        try:
            content_type = ContentType.objects.get(id=content_type_id)
            content_object = content_type.get_object_for_this_type(id=object_id)
            self.validate_payment_input(payment_method, phone_number, card_number)

            if idempotency_key and Payment.objects.filter(order_tracking_id=idempotency_key).exists():
                payment = Payment.objects.get(order_tracking_id=idempotency_key)
                serializer = PaymentSerializer(payment)
                return Response({
                    'order_tracking_id': payment.order_tracking_id,
                    'status': payment.status,
                    'details': f"Payment already {payment.status}."
                }, status=status.HTTP_200_OK)

            payment = Payment.objects.create(
                user=request.user,
                content_type=content_type,
                object_id=object_id,
                order_tracking_id=idempotency_key or str(uuid.uuid4()),
                amount=amount,
                currency=settings.DEFAULT_CURRENCY,
                status='pending',
                payment_method=payment_method
            )

            sim_result = self.handle_simulated_payment(payment, phone_number, card_number)
            if sim_result['status'] == 'success':
                payment.status = 'succeeded'
                payment.save()
                PaymentLog.objects.create(
                    payment=payment,
                    action='confirmed',
                    details={'simulated_response': sim_result}
                )

                subject = f"Payment Confirmation: {content_object.title}"
                message = (
                    f"Dear {payment.user.full_name},\n\n"
                    f"Your payment of {payment.amount} {payment.currency} for '{content_object.title}' was successful.\n"
                    f"Order ID: {payment.order_tracking_id}\n"
                    f"Method: {payment.get_payment_method_display()}\n\n"
                    f"Thank you!\nThe Team"
                )
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[payment.user.email],
                    fail_silently=False
                )

            serializer = PaymentSerializer(payment)
            return Response({
                'order_tracking_id': payment.order_tracking_id,
                'status': payment.status,
                'details': sim_result['message']
            }, status=status.HTTP_200_OK)
        except ContentType.DoesNotExist:
            return Response({'detail': 'Invalid content type'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Checkout error: {str(e)}")
            return Response({'detail': f'Error processing payment: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def earnings(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 8))
            if page < 1 or page_size < 1:
                return Response({'detail': 'Invalid page or page size'}, status=status.HTTP_400_BAD_REQUEST)

            # Filter payments for courses/events created by the instructor
            payments = Payment.objects.filter(
                Q(course__instructor=request.user) | Q(event__created_by=request.user),
                status='succeeded'
            ).select_related('content_type').order_by('-created_at')

            total_payments = payments.count()
            total_pages = (total_payments + page_size - 1) // page_size
            start = (page - 1) * page_size
            end = start + page_size
            paginated_payments = payments[start:end]

            now = timezone.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            sales_this_month = payments.filter(created_at__gte=month_start).aggregate(Sum('amount'))['amount__sum'] or 0
            lifetime_earnings = payments.aggregate(Sum('amount'))['amount__sum'] or 0
            to_be_paid = lifetime_earnings * 0.75  # Simplified: 75% after commission

            serializer = EarningsSerializer({
                'sales_this_month': sales_this_month,
                'to_be_paid': to_be_paid,
                'lifetime_earnings': lifetime_earnings,
                'payments': paginated_payments,
                'total_pages': total_pages,
                'current_page': page
            })
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Earnings fetch error: {str(e)}")
            return Response({'detail': f'Error fetching earnings: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)