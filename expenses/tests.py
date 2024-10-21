from django.test import TestCase
from django.urls import reverse
from .models import UserProfile, Expense, BalanceSheet
from decimal import Decimal
from io import StringIO
import csv


class ExpenseTestCase(TestCase):

    def setUp(self):
        # Creating users
        self.user1 = UserProfile.objects.create(email='user1@example.com', name='User One', mobile_number='1234567890')
        self.user2 = UserProfile.objects.create(email='user2@example.com', name='User Two', mobile_number='0987654321')
        self.user3 = UserProfile.objects.create(email='user3@example.com', name='User Three', mobile_number='1122334455')

    def test_add_expense_equal_split(self):
        # Add an expense with equal split
        url = reverse('add_expense')  # Use reverse to ensure correct URL
        data = {
            'payer_id': self.user1.id,
            'participants': [self.user1.id, self.user2.id, self.user3.id],
            'amount': 300.00,
            'split_type': 'equal',
            'description': 'Dinner'
        }
        response = self.client.post(url, data, content_type='application/json')  # Ensure content_type is JSON

        self.assertEqual(response.status_code, 201)

        # Check the balances
        balance_user2 = BalanceSheet.objects.get(user=self.user2)
        self.assertEqual(balance_user2.amount_owed, Decimal('100.00'))

    def test_add_expense_exact_split(self):
        # Add an expense with exact split
        url = reverse('add_expense')
        data = {
            'payer_id': self.user1.id,
            'participants': [self.user1.id, self.user2.id],
            'amount': 300.00,
            'split_type': 'exact',
            'description': 'Shopping',
            'exact_splits': {
                str(self.user1.id): 150.00,
                str(self.user2.id): 150.00,
            }
        }
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Check balance for user2
        balance_user2 = BalanceSheet.objects.get(user=self.user2)
        self.assertEqual(balance_user2.amount_owed, Decimal('150.00'))

    def test_add_expense_percentage_split(self):
    # Add an expense with percentage split
        url = reverse('add_expense')
        data = {
            'payer_id': self.user1.id,
            'participants': [self.user1.id, self.user2.id, self.user3.id],
            'amount': 400.00,
            'split_type': 'percentage',
            'description': 'Party',
            'percentage_splits': {
                str(self.user1.id): 50,  # 50% for user1
                str(self.user2.id): 25,  # 25% for user2
                str(self.user3.id): 25,  # 25% for user3
            }
        }
        response = self.client.post(url, data, content_type='application/json')

        # Print response for debugging
        print("Response content:", response.content)
        print("Response status code:", response.status_code)

        # Check the status code and ensure the response is successful
        self.assertEqual(response.status_code, 201)

        # Check balance for user2
        balance_user2 = BalanceSheet.objects.get(user=self.user2)
        self.assertEqual(balance_user2.amount_owed, Decimal('100.00'))


    def test_retrieve_user_expenses(self):
        # Create an expense to retrieve later
        expense = Expense.objects.create(payer=self.user1, amount=200.00, split_type='equal', description='Lunch')
        expense.participants.set([self.user1, self.user2])

        url = reverse('retrieve_user_expenses', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Lunch', response.json()['expenses'][0]['description'])

    def test_retrieve_overall_expenses(self):
        # Create a few expenses
        Expense.objects.create(payer=self.user1, amount=200.00, split_type='equal', description='Lunch')
        Expense.objects.create(payer=self.user2, amount=300.00, split_type='exact', description='Groceries')

        url = reverse('retrieve_overall_expenses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['expenses']), 2)



    def test_download_balance_sheet(self):
        # Create balance entries
        BalanceSheet.objects.create(user=self.user1, amount_owed=100.00, amount_paid=50.00)
        BalanceSheet.objects.create(user=self.user2, amount_owed=50.00, amount_paid=0.00)

        url = reverse('download_balance_sheet', args=[self.user1.id])
        response = self.client.get(url)

        # Assert the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert the content type is CSV
        self.assertEqual(response['Content-Type'], 'text/csv')

        # Parse the CSV content
        csv_content = StringIO(response.content.decode('utf-8'))
        reader = csv.reader(csv_content)
        rows = list(reader)

        # Check the CSV structure and content
        self.assertEqual(rows[0], ['User', 'Amount Owed', 'Amount Paid'])  
        self.assertEqual(rows[1], [self.user1.name, '100.00', '50.00'])   