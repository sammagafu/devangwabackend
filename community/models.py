from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from django.utils.text import slugify

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

class Thread(models.Model):
    post = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], upload_to='post')
    category = models.ForeignKey(Category, related_name='threads', on_delete=models.CASCADE)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    starter = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.content)
        super(Thread, self).save(*args, **kwargs)

    def __str__(self):
        return self.content

class ThreadLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thread')

    def __str__(self):
        return f'{self.user.username} likes {self.thread.title}'

class ThreadReply(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} on {self.thread.title}'

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ThreadReply, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} likes a post by {self.post.author.username}'
