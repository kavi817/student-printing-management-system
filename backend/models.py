from backend.app import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    wallet_balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    print_jobs = db.relationship('PrintJob', backref='student', lazy=True)

class PrintJob(db.Model):
    __tablename__ = 'print_jobs'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    document_name = db.Column(db.String(200), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, printing, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
