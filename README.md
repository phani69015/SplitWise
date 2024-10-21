# 💸 Daily Expenses Sharing Application (Splitwise Backend) 💸

### Developed as part of an assignment for the Backend Intern position at Convin AI.

---

## 📑 Overview

This project is a backend service for a Daily Expenses Sharing Application, built as part of a technical assignment for the **Backend Intern position at Convin AI**. The service allows users to add expenses, split them among participants, and generate downloadable balance sheets. It's built using Django and follows modular, scalable practices to ensure smooth functionality and easy integration.

---

## 🛠️ Features

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

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/splitwise-backend.git
   cd splitwise-backend
