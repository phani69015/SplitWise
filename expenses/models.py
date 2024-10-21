from django.db import models

# UserProfile model
class UserProfile(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


# Expense model
class Expense(models.Model):
    payer = models.ForeignKey(UserProfile, related_name='expenses_paid', on_delete=models.CASCADE)
    participants = models.ManyToManyField(UserProfile, related_name='expenses')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    
    # Split types: equal, exact, or percentage
    SPLIT_CHOICES = [
        ('equal', 'Equal'),
        ('exact', 'Exact'),
        ('percentage', 'Percentage'),
    ]
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES)

    def __str__(self):
        return f"{self.description} - {self.amount}"


# BalanceSheet model
class BalanceSheet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.name}: Owes {self.amount_owed} - Paid {self.amount_paid}"
