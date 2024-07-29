from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from decimal import Decimal
from django_resized import ResizedImageField
from django.contrib.auth import get_user_model

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_deadline = models.DateTimeField(null=True,blank=True)
    registration_deadline = models.DateTimeField()
    cover = ResizedImageField(size=[1920, 1080], crop=['middle', 'center'], upload_to='event/cover/',default="cover-img.jpg")
    
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



class Participant(models.Model):
    session = models.ForeignKey(Event, related_name='event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='participant', on_delete=models.CASCADE, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.full_name} in {self.session}"
        else:
            return f"{self.participant_name} in {self.session}"
        
        
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.amount}"
