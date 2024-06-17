import pandas as pd
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, render_template, request, jsonify
from models import Instrument, Student, Loan, TermDates, db
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

Base = declarative_base()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/in', methods=['GET', 'POST'])
def in_page():
    if request.method == 'POST':
        session = db.session()
        name = request.form['name']
        description = request.form['description']
        serial_no = request.form['serial_no']
        last_valuation_date_str = request.form['last_valuation_date']
        last_valuation_amount_str = request.form['last_valuation_amount']
        purchased_date_str = request.form['purchased_date']
        vendor = request.form['vendor']
        notes = request.form['notes']
        maintenance_notes = request.form['maintenance_notes']
        storage_location = request.form['storage_location']
        school = request.form['school']
        category = request.form['category']

        # Convert string dates to Python date objects or None if empty
        last_valuation_date = datetime.strptime(last_valuation_date_str, '%Y-%m-%d').date() if last_valuation_date_str else None
        purchased_date = datetime.strptime(purchased_date_str, '%Y-%m-%d').date() if purchased_date_str else None

        # Convert last_valuation_amount to float or None if empty
        last_valuation_amount = float(last_valuation_amount_str) if last_valuation_amount_str else None

        instrument = Instrument(name=name, description=description, serial_no=serial_no,
                                last_valuation_date=last_valuation_date,
                                last_valuation_amount=last_valuation_amount,
                                purchased_date=purchased_date, vendor=vendor,
                                notes=notes, maintenance_notes=maintenance_notes,
                                storage_location=storage_location, school=school,
                                category=category, is_available=True)
        session.add(instrument)
        session.commit()
        session.close()  # Close the session
        return render_template('in-success.html')

    return render_template('in.html')

@app.route('/out', methods=['GET', 'POST'])
def out_page():
    if request.method == 'POST':
        session = db.session()
        student_id = request.form['student_id']
        instrument_id = request.form['instrument_id']
        date_of_loan = datetime.strptime(request.form['date_of_loan'], '%Y-%m-%d').date()
        duration = int(request.form['duration'])
        duration_period = request.form['duration_period']
        cost = float(request.form['cost'])
        date_of_return = datetime.strptime(request.form['date_of_return'], '%Y-%m-%d').date()

        # Calculate the duration_of_loan based on the period
        if duration_period == 'half-term':
            duration_of_loan = f'{duration} Half-terms'
        elif duration_period == 'term':
            duration_of_loan = f'{duration} Terms'
        else:
            duration_of_loan = f'{duration} Years'

        loan = Loan(student_id=student_id, instrument_id=instrument_id,
                    date_of_loan=date_of_loan, duration_of_loan=duration_of_loan,
                    cost=cost, date_of_return=date_of_return, returned=False)

        instrument = session.query(Instrument).filter_by(id=instrument_id).first()
        if instrument:
            instrument.is_available = False
            session.commit()
        else:
            session.rollback()
            return "Instrument not found"

        session.add(loan)
        session.commit()
        session.close()
        return render_template('out-success.html')

    return render_template('out.html')

# Routes for the "Modify" sub-pages
@app.route('/modify/student')
def modify_student():
    return render_template('modify/student.html')

@app.route('/modify/instrument')
def modify_instrument():
    return render_template('modify/instrument.html')

@app.route('/modify/loan')
def modify_loan():
    return render_template('modify/loan.html')

@app.route('/return')
def return_page():
    loans = Loan.query.filter_by(returned=False).join(Student).join(Instrument).all()
    rendered_template = render_template('return.html', loans=loans)
    return rendered_template

# Route for the "Instrument Info" page
@app.route('/info/instrument')
def info_instrument():
    return render_template('info/instrument.html')

# Route for the "Student Info" page
@app.route('/info/student')
def info_student():
    return render_template('info/student.html')

@app.route('/get_students', methods=['GET'])
def get_students():
    search_term = request.args.get('search_term', '')
    students = db.session.query(Student).filter(
        or_(
            Student.forename.like(f'%{search_term}%'),
            Student.preferred_name.like(f'%{search_term}%'),
            Student.surname.like(f'%{search_term}%'),
            Student.student_id.like(f'%{search_term}%')
        )
    ).all()
    student_data = [{'id': student.student_id, 'display_name': f"{student.preferred_name} {student.surname} ({student.form})"} for student in students]
    return jsonify({'students': student_data})

@app.route('/get_instruments', methods=['GET'])
def get_instruments():
    search_term = request.args.get('search_term', '')
    instruments = db.session.query(Instrument).filter(
        or_(
            Instrument.name.like(f'%{search_term}%'),
            Instrument.description.like(f'%{search_term}%'),
            Instrument.serial_no.like(f'%{search_term}%'),
            Instrument.id.like(f'%{search_term}%')
        )
    ).all()
    instrument_data = [{'id': instrument.id, 'name': instrument.name, 'school': instrument.school} for instrument in instruments]
    return jsonify({'instruments': instrument_data})

@app.route('/check_instrument_availability', methods=['GET'])
def check_instrument_availability():
    instrument_id = request.args.get('instrument_id')

    if instrument_id:
        instrument = Instrument.query.get(instrument_id)
        if instrument:
            return jsonify({'is_available': instrument.is_available})
        else:
            return jsonify({'error': 'Instrument not found'}), 404
    else:
        return jsonify({'error': 'Invalid instrument ID'}), 400
    
@app.route('/return_instruments', methods=['POST'])
def return_instruments():
    loan_ids = request.get_json().get('loan_ids')
    if loan_ids:
        session = db.session()
        for loan_id in loan_ids:
            loan = session.query(Loan).get(loan_id)
            if loan:
                loan.returned = True
                instrument = loan.instrument
                instrument.is_available = True
        session.commit()
        session.close()
        return jsonify({'message': 'Instruments returned successfully.'})
    else:
        return jsonify({'message': 'No loans selected.'}), 400

if __name__ == "__main__":
    db_uri = "sqlite:///database.db"

