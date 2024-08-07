from django.db import models
from django.contrib.auth.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20,
                              choices=[('completed', 'Completed'), ('pending', 'Pending'), ('failed', 'Failed')])

    def __str__(self):
        return f"Payment {self.transaction_id} by {self.user.username} - {self.amount}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def __str__(self):
        return f"Subscription {self.user.username} - {self.status}"
