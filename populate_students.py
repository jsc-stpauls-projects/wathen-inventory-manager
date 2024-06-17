import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True, unique=True)
    forename = db.Column(db.String)
    preferred_name = db.Column(db.Integer)
    surname = db.Column(db.String)
    form = db.Column(db.String)
    tutor_email = db.Column(db.String)
    year = db.Column(db.Integer)

def insert_data_from_excel():
    # Read data from the Excel file
    data = pd.read_excel('Data.xlsx')

    # Map the column names to the corresponding database column names
    column_mapping = {
        'F': 'Student_Id',
        'A': 'Forename',
        'B': 'Preferred_Name',
        'C': 'Surname',
        'D': 'Form',
        'E': 'Tutor_Email',
        'G': 'Year'
    }

    # Rename the columns in the DataFrame based on the column mapping
    data = data.rename(columns=column_mapping)

    # Convert the DataFrame to a list of dictionaries
    records = data.to_dict(orient='records')

    # Insert the records into the database
    with app.app_context():
        for record in records:
            student = Student(**record)
            db.session.add(student)
        db.session.commit()

if __name__ == '__main__':
    insert_data_from_excel()