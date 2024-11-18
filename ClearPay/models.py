from django.db import models
from datetime import date ,timedelta
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=0)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
    )
    password = models.CharField(max_length=128, null=False)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username}: {self.email}"


class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,null=True)
    email = models.EmailField(max_length=254,unique=True)
    nickname = models.CharField(max_length=50,null=True,blank=True)
    photo = models.ImageField(upload_to='media/client_photos',null=True,blank=True)
    phone_number = models.CharField(max_length=50,unique=True,)
    age = models.IntegerField(default=0)
    location = models.TextField(null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True,)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateTimeField(auto_now_add=True)
    repayment_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('closed', 'Closed')],default='active')
    due_date = models.DateField(null=True,default=date.today) 
    def __str__(self):
        return (
            f"Loan for {self.client.user.username}, "
            f"Phone: {self.client.user.phone_number}, "
            f"Email: {self.client.user.email}, "
            f"Amount: {self.amount}"
        )
    def default_due_date():
        return date.today() + timedelta(days=30)


class Transaction(models.Model):
    LOAN_TYPE = 'loan'
    REPAYMENT_TYPE = 'repayment'
    Transaction_CHOICES = [
        (LOAN_TYPE, 'Loan'),
        (REPAYMENT_TYPE, 'Repayment')
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=Transaction_CHOICES,default='loan')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.transaction_type.capitalize()} of {self.amount}, "
            f"by {self.client.user.username}, "
            f"Email: {self.client.user.email}"
        )
