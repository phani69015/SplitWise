# Daily Expenses Sharing Application (Splitwise Backend)


---

## Overview

This project is a backend service for a Daily Expenses Sharing Application, built as part of a technical assignment for the **Backend Intern position at Convin AI**. The service allows users to add expenses, split them among participants, and generate downloadable balance sheets. It's built using Django and follows modular, scalable practices to ensure smooth functionality and easy integration.

---

## Features

- **User Registration & Authentication**: Manage user profiles and authentication securely.
- **Expense Management**: Add expenses and split them using:
  - Equal splits
  - Percentage-based splits
  - Exact amount splits
- **Balance Sheet Management**: Track amounts owed and paid.
- **CSV Download of Balance Sheets**: Export balance sheets in CSV format.
- **REST API**: Well-documented API for managing users, expenses, and balances.
- **Automated Testing**: Comprehensive test cases for expense management and user interaction.

---

## ⚙️ Tech Stack

- **Backend Framework**: [Django](https://www.djangoproject.com/)
- **Database**: dbsqlite3
- **Libraries/Tools**:
  - Django Rest Framework (DRF) for RESTful API development
  - Python's Decimal module for financial precision
  - CSV for exporting balance sheets
  - Django's Test framework for robust testing

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.x** installed.
- **Git** for version control.

### Installation and setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/phani69015/SplitWise.git
   cd SplitWise
2.  **Create a virtual environment:**
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # For Windows: myenv\Scripts\activate
3. **Install dependencies:**
   ```bash
   pip install -r req.txt
4. **Database setup (optional)**
    Configure the database settings in settings.py if wanted to use Postgre or Mysql else dbsqlite3 will be used :
   ```bash
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourdbpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    }
5. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
## 📋 API Endpoints

### Key API Endpoints for the Application( POSTMAN ):

#### User Management
- **POST expenses/create-user/** - Register a new user.
- **POST expenses/retreive-user/** - Log in a user.

#### Expense Management
- **POST expenses/add-expense/** - Add an expense with a specified split type.
- **GET expenses/user-expenses/<user_id>/** - Retrieve expenses for a specific user.

#### Balance Sheet
- **GET expenses/download-balance-sheet/<user_id>/** - Download a CSV of the user's balance sheet.

## 🔍 Testing

Run the automated tests to verify the functionality:

```bash
python manage.py test
