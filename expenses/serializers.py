from rest_framework import serializers
from .models import UserProfile, Expense, BalanceSheet

# UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'name', 'mobile_number']

# Expense Serializer
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'payer', 'participants', 'description', 'amount', 'date', 'split_type']

# BalanceSheet Serializer
class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheet
        fields = ['id', 'user', 'amount_owed', 'amount_paid']
