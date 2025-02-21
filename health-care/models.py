from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

# User Model (for Patients and Admins)
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='patient')  # Roles: patient, staff, admin

    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, foreign_keys='Appointment.patient_id')

    def __init__(self, username, email, password, role='patient'):
        self.username = username
        self.email = email
        self.password_hash = self.set_password(password)
        self.role = role

    def set_password(self, password):
        """Hashes the password."""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks the hashed password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# Department Model
class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # Relationship with doctors
    doctors = db.relationship('Doctor', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.name}>'


# Doctor Model
class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)  # Reference to User model
    
    # Relationship with appointments
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f'<Doctor {self.name} - Department: {self.department.name}>'


# Appointment Model
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)  # Appointment with a specific doctor
    appointment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')  # Statuses: Pending, Confirmed, Completed

    def __repr__(self):
        return f'<Appointment {self.id} - Status: {self.status} - Doctor: {self.doctor.name}>'


# Medicine Model
class Medicine(db.Model):
    __tablename__ = 'medicines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    low_stock_threshold = db.Column(db.Integer, nullable=False)

    # Relationship with PurchaseHistory
    purchase_history = db.relationship('PurchaseHistory', backref='medicine', lazy=True)

    def __repr__(self):
        return f'<Medicine {self.name} - Quantity: {self.quantity}>'


# PurchaseHistory Model
class PurchaseHistory(db.Model):
    __tablename__ = 'purchase_history'

    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity_purchased = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<PurchaseHistory {self.id} - Medicine ID: {self.medicine_id}>'
