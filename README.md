# SDCKL Student Printing Management System with E-Wallet

## Overview
This is a student printing management system with an integrated e-wallet. Students can register, top up their wallet, and submit print jobs. The system deducts printing costs from the wallet balance.

## Technology Stack
- Backend: Python Flask with SQLAlchemy ORM
- Database: SQLite (for simplicity, can be changed to other SQL databases)
- Frontend: Simple HTML with Tailwind CSS

## Setup Instructions

### Prerequisites
- Python 3.x installed
- pip installed

### Backend Setup
1. Navigate to the `backend` directory:
   ```
   cd backend
   ```
2. Install required packages:
   ```
   pip install flask flask_sqlalchemy flask_cors
   ```
3. Initialize the database:
   Run Python shell or create a script to create tables:
   ```python
   from app import db
   db.create_all()
   ```
4. Run the backend server:
   ```
   python app.py
   ```
   The backend server will run on `http://localhost:5000`.

### Frontend Setup
1. Open the `frontend/index.html` file in a web browser.
2. The frontend communicates with the backend API at `http://localhost:5000`.

## Usage
- Register a student with Student ID, Name, and Email.
- Top up the student's wallet.
- Submit print jobs specifying document name, pages, and cost.
- Wallet balance is automatically deducted on print job submission.

## Notes
- This is a basic implementation for demonstration purposes.
- For production, consider using a more robust database like PostgreSQL or MySQL.
- Add authentication and security features as needed.
