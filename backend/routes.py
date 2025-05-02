from flask import request, jsonify
from backend.app import app, db
from backend.models import Student, PrintJob

@app.route('/students', methods=['POST'])
def create_student():
    data = request.json
    if not data or not all(k in data for k in ('student_id', 'name', 'email')):
        return jsonify({'error': 'Missing required fields'}), 400
    if Student.query.filter_by(student_id=data['student_id']).first():
        return jsonify({'error': 'Student ID already exists'}), 400
    if Student.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    student = Student(
        student_id=data['student_id'],
        name=data['name'],
        email=data['email'],
        wallet_balance=0.0
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully', 'student': {
        'id': student.id,
        'student_id': student.student_id,
        'name': student.name,
        'email': student.email,
        'wallet_balance': student.wallet_balance
    }}), 201

@app.route('/students/<int:student_id>/wallet', methods=['GET'])
def get_wallet_balance(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({'wallet_balance': student.wallet_balance})

@app.route('/students/<int:student_id>/wallet/topup', methods=['POST'])
def topup_wallet(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    data = request.json
    amount = data.get('amount')
    if not amount or amount <= 0:
        return jsonify({'error': 'Invalid top-up amount'}), 400
    student.wallet_balance += amount
    db.session.commit()
    return jsonify({'message': 'Wallet topped up successfully', 'wallet_balance': student.wallet_balance})

@app.route('/printjobs', methods=['POST'])
def create_print_job():
    data = request.json
    required_fields = ['student_id', 'document_name', 'pages', 'cost']
    if not data or not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    student = Student.query.filter_by(id=data['student_id']).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    if student.wallet_balance < data['cost']:
        return jsonify({'error': 'Insufficient wallet balance'}), 400
    # Deduct cost from wallet
    student.wallet_balance -= data['cost']
    print_job = PrintJob(
        student_id=student.id,
        document_name=data['document_name'],
        pages=data['pages'],
        cost=data['cost'],
        status='pending'
    )
    db.session.add(print_job)
    db.session.commit()
    return jsonify({'message': 'Print job created successfully', 'print_job': {
        'id': print_job.id,
        'student_id': print_job.student_id,
        'document_name': print_job.document_name,
        'pages': print_job.pages,
        'cost': print_job.cost,
        'status': print_job.status
    }}), 201

@app.route('/printjobs/<int:print_job_id>', methods=['GET'])
def get_print_job(print_job_id):
    print_job = PrintJob.query.filter_by(id=print_job_id).first()
    if not print_job:
        return jsonify({'error': 'Print job not found'}), 404
    return jsonify({
        'id': print_job.id,
        'student_id': print_job.student_id,
        'document_name': print_job.document_name,
        'pages': print_job.pages,
        'cost': print_job.cost,
        'status': print_job.status
    })

@app.route('/students/<int:student_id>/printjobs', methods=['GET'])
def get_student_print_jobs(student_id):
    student = Student.query.filter_by(id=student_id).first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    print_jobs = PrintJob.query.filter_by(student_id=student.id).all()
    jobs_list = []
    for job in print_jobs:
        jobs_list.append({
            'id': job.id,
            'document_name': job.document_name,
            'pages': job.pages,
            'cost': job.cost,
            'status': job.status
        })
    return jsonify({'print_jobs': jobs_list})
