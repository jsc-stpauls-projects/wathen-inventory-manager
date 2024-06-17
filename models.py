from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Instrument(db.Model):
    __tablename__ = 'instruments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String)
    description = db.Column(db.VARCHAR, nullable=True)
    serial_no = db.Column(db.String, unique=True)
    last_valuation_date = db.Column(db.DateTime, nullable=True)
    last_valuation_amount = db.Column(db.Numeric, nullable=True)
    purchased_date = db.Column(db.DateTime, nullable=True)
    vendor = db.Column(db.String, nullable=True)
    notes = db.Column(db.String)
    maintenance_notes = db.Column(db.String)
    currently_hired_by = db.Column(db.Integer)
    is_available = db.Column(db.Boolean)
    storage_location = db.Column(db.String)
    school = db.Column(db.String)
    category = db.Column(db.String)
    loans = db.relationship('Loan', backref='instrument', lazy='dynamic')

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True, unique=True)
    forename = db.Column(db.String)
    preferred_name = db.Column(db.Integer)
    surname = db.Column(db.String)
    form = db.Column(db.String)
    tutor_email = db.Column(db.String)
    year = db.Column(db.Integer)
    loans = db.relationship('Loan', backref='student', lazy='dynamic')

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    instrument_id = db.Column(db.Integer, db.ForeignKey('instruments.id'))
    date_of_loan = db.Column(db.Date)
    duration_of_loan = db.Column(db.String)
    cost = db.Column(db.Numeric)
    date_of_return = db.Column(db.Date)
    returned = db.Column(db.Boolean)

class TermDates(db.Model):
    __tablename__ = 'term_dates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    term_name = db.Column(db.String)
    term_startdate = db.Column(db.Date)
    term_enddate = db.Column(db.Date)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)