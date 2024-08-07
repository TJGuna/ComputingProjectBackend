from django.contrib.auth.models import User
from django.db import models

class Expert(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expertise_area = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.JSONField(default=dict)  # Stores availability in JSON format
    profile_picture = models.ImageField(upload_to='expert_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Expert"
        verbose_name_plural = "Experts"

class Session(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('canceled', 'Canceled')])

    def __str__(self):
        return f"{self.user.username} - {self.expert.user.username} at {self.scheduled_time}"