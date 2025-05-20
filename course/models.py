from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from django.utils.text import slugify
from decimal import Decimal
from django.db.models import JSONField
from django.utils import timezone
import uuid

User = get_user_model()

# Course Model
class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_creator")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ispublished = models.BooleanField(default=False)
    cover = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], upload_to='course/cover/', default="cover-img.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_deadline = models.DateTimeField(blank=True, null=True)
    total_modules = models.PositiveIntegerField(default=0)
    total_videos = models.PositiveIntegerField(default=0)
    total_documents = models.PositiveIntegerField(default=0)
    total_quizzes = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tags', blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    @property
    def final_price(self):
        # Convert discount_percentage to Decimal to ensure compatibility
        discount_percentage = Decimal(str(self.discount_percentage))
        return self.price * (Decimal(1) - discount_percentage / Decimal(100))
    
    def enroll(self, user):
        if not self.enrollments.filter(user=user).exists():
            Enrollment.objects.create(user=user, course=self)

    def completion_percentage_for_user(self, user):
        if self.total_modules == 0:
            return 100.0
        completed_modules = sum(1 for module in self.modules.all() if module.is_completed_by_user(user))
        return (completed_modules / self.total_modules) * 100

    def is_completed_by_user(self, user):
        return all(module.is_completed_by_user(user) for module in self.modules.all())
# Module Model
class Module(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(default="description")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    total_videos = models.PositiveIntegerField(default=0)
    total_documents = models.PositiveIntegerField(default=0)
    total_quizzes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Module, self).save(*args, **kwargs)

    def is_completed_by_user(self, user):
        videos_completed = VideoProgress.objects.filter(video__module=self, user=user, watched=True).count() == self.total_videos
        documents_completed = DocumentProgress.objects.filter(document__module=self, user=user, read=True).count() == self.total_documents
        quizzes_passed = QuizAttempt.objects.filter(quiz__module=self, user=user, passed=True).count() == self.total_quizzes
        return videos_completed and documents_completed and quizzes_passed

# Enrollment Model
class Enrollment(models.Model):
    user = models.ForeignKey(User, related_name='enrol', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True)
    progress_notes = models.TextField(blank=True, null=True)
    certificate_issued = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} enrolled in {self.course.title}"

    def update_completion_status(self):
        self.completion_percentage = self.course.completion_percentage_for_user(self.user)
        self.is_completed = self.course.is_completed_by_user(self.user)
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        self.save()

# Video Model
class Video(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    module = models.ForeignKey(Module, related_name='videos', on_delete=models.CASCADE)
    video_url = models.TextField(max_length=300)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)

# Document Model
class Document(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    module = models.ForeignKey(Module, related_name='documents', on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='course_documents/')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Document, self).save(*args, **kwargs)

# Quiz Model
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    module = models.ForeignKey(Module, related_name='quizzes', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    pass_mark = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes. Set 0 for no time limit.")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Quiz, self).save(*args, **kwargs)

# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text

# Answer Model
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# VideoProgress Model
class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(null=True, blank=True)
    last_position = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'video')

# DocumentProgress Model
class DocumentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    page_number = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'document')

# QuizAttempt Model
class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    passed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)
    user_answers = JSONField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'quiz')

# ModuleProgress Model
class ModuleProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('enrollment', 'module')

# FAQ Model
class FAQ(models.Model):
    course = models.ForeignKey(Course, related_name='faqs', on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(auto_now=True)
    is_answered = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    is_edited_at = models.DateTimeField(auto_now=True)
    is_asked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='faq_asking')
    is_answered_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='faq_answerer')

    def __str__(self):
        return self.question

# Tags Model
class Tags(models.Model):
    tag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag
   
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('vodacom', 'Vodacom'),
        ('airtel', 'Airtel'),
        ('mtn', 'MTN'),
        ('card', 'Card'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_payments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, null=True, blank=True)
    order_tracking_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    status = models.CharField(max_length=50, default='pending')  # pending, succeeded, failed
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='mpesa')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.order_tracking_id} for {self.course.title if self.course else 'Unknown'}"