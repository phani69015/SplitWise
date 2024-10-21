from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UserProfile
from .models import Expense, BalanceSheet, UserProfile
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from decimal import Decimal
import csv
from django.http import HttpResponse
from .models import UserProfile, BalanceSheet


@api_view(['POST'])
def create_user(request):
    try:
        email = request.data['email']
        name = request.data['name']
        mobile_number = request.data['mobile_number']

        if UserProfile.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if UserProfile.objects.filter(mobile_number=mobile_number).exists():
            return JsonResponse({'error': 'Mobile number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = UserProfile.objects.create(email=email, name=name, mobile_number=mobile_number)
        return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_user(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        return JsonResponse({
            'email': user.email,
            'name': user.name,
            'mobile_number': user.mobile_number,
        })
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
            # Exact amounts are provided in request data as a dictionary
            exact_splits = request.data.get('exact_splits', {})
            for participant_id, participant_amount in exact_splits.items():
                participant = UserProfile.objects.get(id=participant_id)
                BalanceSheet.objects.create(user=participant, amount_owed=Decimal(participant_amount), amount_paid=Decimal(0))
        elif split_type == 'percentage':
            # Percentages are provided in request data as a dictionary (ensure they sum to 100%)
            percentage_splits = request.data.get('percentage_splits', {})
            total_percentage = sum(percentage_splits.values())
            if total_percentage != 100:
                return JsonResponse({'error': 'Percentages do not add up to 100%'}, status=status.HTTP_400_BAD_REQUEST)
            
            for participant_id, percentage in percentage_splits.items():
                participant = UserProfile.objects.get(id=participant_id)
                
                # Ensure both percentage and amount are Decimal types
                participant_amount = (Decimal(percentage) / Decimal(100)) * Decimal(amount)
                
                BalanceSheet.objects.create(user=participant, amount_owed=participant_amount, amount_paid=Decimal(0))

        return JsonResponse({'message': 'Expense added successfully'}, status=status.HTTP_201_CREATED)


    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def retrieve_user_expenses(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        expenses = user.expenses.all()
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