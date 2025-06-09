from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from payments.models import Payment
import uuid

User = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    registration_deadline = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    payments = GenericRelation(Payment, related_query_name='event')

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
            while Event.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
            self.slug = unique_slug
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
        if self.registration_deadline >= self.start_time:
            raise ValidationError("Registration deadline must be before start time.")
        super().save(*args, **kwargs)

class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user} - {self.event.title}"

class Speaker(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers')
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"

class Schedule(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='schedules')
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.title} - {self.event.title}"

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
        if self.start_time < self.event.start_time or self.end_time > self.event.end_time:
            raise ValidationError("Schedule must be within event's time frame.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)