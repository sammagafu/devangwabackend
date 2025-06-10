from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'modules', views.ModuleViewSet, basename='module')
router.register(r'videos', views.VideoViewSet, basename='video')
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'quizzes', views.QuizViewSet, basename='quiz')
router.register(r'questions', views.QuestionViewSet, basename='question')
router.register(r'answers', views.AnswerViewSet, basename='answer')
router.register(r'faqs', views.FAQViewSet, basename='faq')
router.register(r'tags', views.TagsViewSet, basename='tag')
router.register(r'module-progress', views.ModuleProgressViewSet, basename='module-progress')
router.register(r'reviews', views.CourseReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]