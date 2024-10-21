from django.urls import path
from . import views

urlpatterns = [
    path('create-user/', views.create_user, name='create_user'),           
    path('user-details/<int:user_id>/', views.retrieve_user, name='retrieve_user'),   
    path('add-expense/', views.add_expense, name='add_expense'),
    path('user-expenses/<int:user_id>/', views.retrieve_user_expenses, name='retrieve_user_expenses'),
    path('overall-expenses/', views.retrieve_overall_expenses, name='retrieve_overall_expenses'),
    path('download-balance-sheet/<int:user_id>/', views.download_balance_sheet, name='download_balance_sheet'),
]
