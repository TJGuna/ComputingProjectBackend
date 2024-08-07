from django.contrib.auth.models import User
from django.db import models


class Relationship(models.Model):
    user1 = models.ForeignKey(User, related_name='relationship_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='relationship_user2', on_delete=models.CASCADE)
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return f"{self.user1.username} and {self.user2.username} - {self.status}"

    class Meta:
        verbose_name = "Relationship"
        verbose_name_plural = "Relationships"


class Goal(models.Model):
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Milestone(models.Model):
    relationship = models.ForeignKey(Relationship, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return self.description
