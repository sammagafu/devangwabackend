from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from payments.models import Payment
import uuid

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    ispublished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payments = GenericRelation(Payment, related_query_name='course')

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            while Course.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
            self.slug = unique_slug
        super().save(*args, **kwargs)

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    total_videos = models.PositiveIntegerField(default=0)
    total_documents = models.PositiveIntegerField(default=0)
    total_quizzes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['course', 'order']),
        ]

    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Video(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    url = models.URLField()
    duration = models.PositiveIntegerField(default=0)  # Duration in seconds

    def __str__(self):
        return f"{self.title} - {self.module.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.module.total_videos = self.module.videos.count()
        self.module.save()

class Document(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"{self.title} - {self.module.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.module.total_documents = self.module.documents.count()
        self.module.save()

class Quiz(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.module.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.module.total_quizzes = self.module.quizzes.count()
        self.module.save()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return f"{self.text[:50]} - {self.quiz.title}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} - {self.question.text[:50]}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completion_percentage = models.FloatField(default=0)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    last_accessed_module = models.ForeignKey(Module, null=True, blank=True, on_delete=models.SET_NULL)
    progress_notes = models.TextField(blank=True)
    certificate_issued = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} - {self.course.title}"

class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_progress')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='progress')
    watched_duration = models.PositiveIntegerField(default=0)  # Seconds watched
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user} - {self.video.title}"

class DocumentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_progress')
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='progress')
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'document')

    def __str__(self):
        return f"{self.user} - {self.document.title}"

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0)
    attempt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.quiz.title} - Score: {self.score}"

class ModuleProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='module_progress')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('enrollment', 'module')

    def __str__(self):
        return f"{self.user} - {self.module.title}"

class FAQ(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField()
    answer = models.TextField(blank=True)
    is_asked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='asked_faqs')
    is_answered = models.BooleanField(default=False)
    is_answered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='answered_faqs')

    def __str__(self):
        return f"{self.question[:50]} - {self.course.title}"

class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)
    courses = models.ManyToManyField(Course, related_name='tags')

    def __str__(self):
        return self.name