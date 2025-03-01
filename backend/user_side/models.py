from django.db import models
from bank_auth.models import CustomUser
class Loan(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('foreclosed', 'Foreclosed'),
    ]
    
    
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.FloatField()
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    tenure = models.IntegerField()  # tenure in months
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    foreclosure_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    foreclosure_date = models.DateField(null=True, blank=True)
    t=models.CharField(max_length=1,null=True)

    def __str__(self):
        return f"{self.name} ({self.id})"