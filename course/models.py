from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from django.utils.text import slugify



User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE,related_name="course_creator")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ispublished = models.BooleanField(default=False)
    cover = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], upload_to='course/cover/',default="cover-img.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_deadline = models.DateTimeField(blank=True, null=True)
    
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
        return self.price * (1 - self.discount_percentage / 100)


class Module(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True,editable=False)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.SET_NULL,null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(default="description")
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Module, self).save(*args, **kwargs)


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


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Enrollment(models.Model):
    user = models.ForeignKey(User, related_name='enrol', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
