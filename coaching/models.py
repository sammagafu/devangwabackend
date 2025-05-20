from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from decimal import Decimal
from django_resized import ResizedImageField
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('online', 'Online'),
        ('on_premises', 'On Premises'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    event_type = models.CharField(max_length=12, choices=EVENT_TYPE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_deadline = models.DateTimeField(null=True, blank=True)
    registration_deadline = models.DateTimeField()
    cover = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], upload_to='event/cover/', default="cover-img.jpg")

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while Event.objects.filter(slug=self.slug).exists():
                self.slug = f'{slugify(self.title)}-{get_random_string(4)}'
        if self.registration_deadline >= self.start_time:
            raise ValidationError("Registration deadline must be before the event start time.")
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        discount_percentage_decimal = Decimal(str(self.discount_percentage))
        discount_factor = Decimal('1') - (discount_percentage_decimal / Decimal('100'))
        return self.price * discount_factor

    def attend(self, user):
        participant, created = Participant.objects.get_or_create(session=self, user=user)
        return participant

class Speaker(models.Model):
    event = models.ForeignKey(Event, related_name='speakers', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='speakers/', null=True, blank=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    event = models.ForeignKey(Event, related_name='schedules', on_delete=models.CASCADE)
    day = models.DateField()
    title = models.CharField(max_length=255)
    time = models.CharField(max_length=50)  # e.g., "9:00 AM - 10:00 AM"
    speakers = models.ManyToManyField(Speaker, blank=True)

    def __str__(self):
        return f"{self.title} on {self.day}"

class Participant(models.Model):
    session = models.ForeignKey(Event, related_name='event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='participant', on_delete=models.CASCADE, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.full_name} in {self.session}"
        return f"Unknown in {self.session}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('mpesa', 'M-Pesa'),
        ('vodacom', 'Vodacom'),
        ('airtel', 'Airtel'),
        ('mtn', 'MTN'),
        ('card', 'Card'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_payments')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_tracking_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    currency = models.CharField(max_length=3, default='KES')
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='mpesa')

    def __str__(self):
        return f"{self.user.username} - {self.event.title if self.event else 'Unknown'} - {self.amount}"