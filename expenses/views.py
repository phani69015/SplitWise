from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from decimal import Decimal
import csv

from .models import UserProfile, Expense, BalanceSheet
from .serializers import UserProfileSerializer, ExpenseSerializer, BalanceSheetSerializer

@api_view(['POST'])
def create_user(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        # Check for existing user
        if UserProfile.objects.filter(email=serializer.validated_data['email']).exists():
            return JsonResponse({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if UserProfile.objects.filter(mobile_number=serializer.validated_data['mobile_number']).exists():
            return JsonResponse({'error': 'Mobile number already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)
    
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_user(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        serializer = UserProfileSerializer(user)
        return JsonResponse(serializer.data)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_expense(request):
    try:
        payer = UserProfile.objects.get(id=request.data['payer_id'])
        participants = UserProfile.objects.filter(id__in=request.data['participants'])
        amount = Decimal(request.data['amount'])
        split_type = request.data['split_type']
        description = request.data['description']

        # Create the expense
        expense = Expense.objects.create(payer=payer, amount=amount, split_type=split_type, description=description)
        expense.participants.set(participants)
        expense.save()

        # Implement split logic based on split_type
        if split_type == 'equal':
            split_amount = amount / len(participants)
            for participant in participants:
                BalanceSheet.objects.create(user=participant, amount_owed=split_amount, amount_paid=Decimal(0))
        elif split_type == 'exact':
            exact_splits = request.data.get('exact_splits', {})
            for participant_id, participant_amount in exact_splits.items():
                participant = UserProfile.objects.get(id=participant_id)
                BalanceSheet.objects.create(user=participant, amount_owed=Decimal(participant_amount), amount_paid=Decimal(0))
        elif split_type == 'percentage':
            percentage_splits = request.data.get('percentage_splits', {})
            total_percentage = sum(percentage_splits.values())
            if total_percentage != 100:
                return JsonResponse({'error': 'Percentages do not add up to 100%'}, status=status.HTTP_400_BAD_REQUEST)
            
            for participant_id, percentage in percentage_splits.items():
                participant = UserProfile.objects.get(id=participant_id)
                participant_amount = (Decimal(percentage) / Decimal(100)) * Decimal(amount)
                BalanceSheet.objects.create(user=participant, amount_owed=participant_amount, amount_paid=Decimal(0))

        return JsonResponse({'message': 'Expense added successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_user_expenses(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        expenses = user.expenses_paid.all()
        expense_data = [{'description': exp.description, 'amount': exp.amount, 'split_type': exp.split_type} for exp in expenses]
        return JsonResponse({'expenses': expense_data})
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def retrieve_overall_expenses(request):
    expenses = Expense.objects.all()
    expense_data = [{'payer': exp.payer.name, 'description': exp.description, 'amount': exp.amount, 'split_type': exp.split_type} for exp in expenses]
    return JsonResponse({'expenses': expense_data})


@api_view(['GET'])
def download_balance_sheet(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        balances = BalanceSheet.objects.filter(user=user)

        # Create the HttpResponse object with CSV content type
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="balance_sheet_{user_id}.csv"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Write CSV headers
        writer.writerow(['User', 'Amount Owed', 'Amount Paid'])

        # Write user balance data
        for balance in balances:
            writer.writerow([user.name, balance.amount_owed, balance.amount_paid])

        return response

    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
