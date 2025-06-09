from rest_framework import serializers
from .models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentSerializer(serializers.ModelSerializer):
    content_object_title = serializers.SerializerMethodField()
    payment_method_display = serializers.CharField(source='get_payment_method_display')

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'content_type', 'object_id', 'order_tracking_id',
            'content_object_title', 'amount', 'currency', 'status',
            'payment_method', 'payment_method_display', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'order_tracking_id', 'created_at']

    def get_content_object_title(self, obj):
        return obj.content_object.title if obj.content_object else 'Unknown'

class EarningsSerializer(serializers.Serializer):
    sales_this_month = serializers.DecimalField(max_digits=10, decimal_places=2)
    to_be_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    lifetime_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    payments = PaymentSerializer(many=True)
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()