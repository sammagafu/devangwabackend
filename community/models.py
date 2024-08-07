from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from django.utils.text import slugify
import uuid

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], upload_to='posts/', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='threads', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True, editable=False)
    starter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at'] 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.id))
        super(Thread, self).save(*args, **kwargs)

    def __str__(self):
        return f'Thread started by {self.starter}'

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class ThreadLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thread')

    def __str__(self):
        return f'{self.user.email} likes thread {self.thread.id}'

class ThreadReply(models.Model):
    thread = models.ForeignKey(Thread, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.email} replied to thread {self.thread.id}'

    def get_replies_count(self):
        return self.replies.count()

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ThreadReply, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} likes a post by {self.post.author.username}'
