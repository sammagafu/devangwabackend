from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils import timezone
from accounts.models import CustomUser, Membership
from course.models import Course, Enrollment
from coaching.models import Event, Participant
from payments.models import Payment
from community.models import Category, Thread, ThreadReply
from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncMonth

class DashboardStatsView(APIView):
    def get(self, request):
        try:
            # User stats
            total_users = CustomUser.objects.count()
            active_users = Membership.objects.filter(
                expiration_date__gte=timezone.now().date()
            ).count()  # Removed is_active since it may not exist
            new_users_this_month = CustomUser.objects.filter(
                created_at__year=timezone.now().year,
                created_at__month=timezone.now().month
            ).count()

            # Course stats
            total_courses = Course.objects.count()
            published_courses = Course.objects.filter(ispublished=True).count()
            total_enrollments = Enrollment.objects.count()
            completed_courses = Enrollment.objects.filter(is_completed=True).count()
            courses_in_progress = Enrollment.objects.filter(
                is_completed=False,
                started_at__isnull=False
            ).count()

            # Event stats
            total_events = Event.objects.count()
            upcoming_events = Event.objects.filter(start_time__gte=timezone.now()).count()
            total_participants = Participant.objects.count()

            # Payment stats
            total_revenue = Payment.objects.filter(status='succeeded').aggregate(
                total_revenue=Sum('amount')
            )['total_revenue'] or 0

            # Support requests (mock data; replace with actual model if exists)
            support_requests = [
                {
                    'id': 1,
                    'name': 'Sample User',
                    'description': 'Sample support request',
                    'time': timezone.now().isoformat(),
                    'icon_color': 'primary'
                }
            ]

            data = {
                'total_users': total_users,
                'active_users': active_users,
                'new_users_this_month': new_users_this_month,
                'total_courses': total_courses,
                'published_courses': published_courses,
                'total_enrollments': total_enrollments,
                'completed_courses': completed_courses,
                'courses_in_progress': courses_in_progress,
                'total_events': total_events,
                'upcoming_events': upcoming_events,
                'total_participants': total_participants,
                'total_revenue': float(total_revenue),
                'support_requests': support_requests
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class EarningsChartView(APIView):
    def get(self, request):
        try:
            end_date = timezone.now().date()
            start_date = end_date - relativedelta(months=11)
            earnings = Payment.objects.filter(
                status='succeeded',
                created_at__date__gte=start_date,
                created_at__date__lte=end_date
            ).annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(
                total=Sum('amount')
            ).order_by('month')

            series = [float(e['total']) for e in earnings]
            categories = [e['month'].strftime('%b %Y') for e in earnings]

            data = {
                'series': [{'name': 'Earnings', 'data': series}],
                'categories': categories
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class TopInstructorsView(APIView):
    def get(self, request):
        try:
            top_instructors = CustomUser.objects.filter(
                courses__ispublished=True
            ).annotate(
                course_count=Count('courses'),
                total_enrollments=Count('courses__enrollments')
            ).order_by('-total_enrollments')[:5]

            data = [
                {
                    'id': instructor.id,
                    'name': instructor.full_name or instructor.email,
                    'image': instructor.userdetails.avatar.url if hasattr(instructor, 'userdetails') and instructor.userdetails.avatar else null,
                    'verified': instructor.is_staff,
                    'courses': instructor.course_count,
                    'rating': 4.5  # Mock rating; replace with actual if available
                } for instructor in top_instructors
            ]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class CommunityStatsView(APIView):
    def get(self, request):
        try:
            total_communities = Category.objects.count()
            total_threads = Thread.objects.count()
            total_replies = ThreadReply.objects.count()
            most_active_users = CustomUser.objects.annotate(
                thread_count=Count('thread_set'),
                reply_count=Count('threadreply_set')
            ).order_by('-thread_count', '-reply_count')[:5]

            data = {
                'total_communities': total_communities,
                'total_threads': total_threads,
                'total_replies': total_replies,
                'most_active_users': [
                    {
                        'id': user.id,
                        'name': user.full_name or user.email,
                        'thread_count': user.thread_count,
                        'reply_count': user.reply_count
                    } for user in most_active_users
                ]
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class EventStatsView(APIView):
    def get(self, request):
        try:
            events = Event.objects.filter(start_time__gte=timezone.now())[:5]
            data = [
                {
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'time': event.start_time.isoformat(),
                    'icon': 'bell',
                    'icon_color': 'primary'
                } for event in events
            ]
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class TrafficSourcesView(APIView):
    def get(self, request):
        try:
            # Mock data; replace with actual traffic source logic
            data = {
                'series': [30, 40, 20, 10],
                'labels': ['Social Media', 'Search Engines', 'Direct', 'Referrals'],
                'colors': ['#0d6efd', '#28a745', '#ffc107', '#dc3545']
            }
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)