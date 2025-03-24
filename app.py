# Libreries Section
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
import csv
import sqlite3
import os

# Variable Section
app = Flask(__name__)
DATABASE = 'hiring.db'

# Check id the folder exist
os.makedirs('uploads/', exist_ok=True)

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER,
                name TEXT
            )
        ''')
        conn.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER,
                job TEXT
            )
        ''')
        conn.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hired_employees (
                id INTEGER,
                name TEXT,
                datetime TEXT,
                department_id INTEGER,
                job_id INTERGER
            )
        ''')
        conn.commit()                

def insert_data_from_csv(file_path):
    with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
    if 'departments' in str(file_path).lower():
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                id, name = row
                cursor.execute('''
                        INSERT INTO departments (id, name)
                        VALUES (?, ?)
                    ''', (int(id), name))
            conn.commit()
    
    if 'jobs' in str(file_path).lower():
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                id, job = row
                cursor.execute('''
                        INSERT INTO jobs (id, job)
                        VALUES (?, ?)
                    ''', (int(id), job))
            conn.commit()

    if 'hired_employees' in str(file_path).lower():
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                id, name, datetime, department_id, job_id = row
                cursor.execute('''
                        INSERT INTO hired_employees (id, name, datetime, department_id, job_id)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (int(id), name, datetime, department_id, job_id))
            conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # Check if file comes with teh request
    if 'file' in request.files:
        # Catch file
        file = request.files['file']
        # Secure the name of the file
        filename = secure_filename(file.filename)
        # Save the file in the folder that was checked before
        file.save(f'uploads/{filename}')
        #Converting to dictionaries
        insert_data_from_csv(f'uploads/{filename}')

    return 'Data Insertada correctamente'

@app.route('/view_data', methods=['GET'])
def view_data():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT a.job, c.name, IFNULL(b.Q1, 0), IFNULL(b.Q2, 0), IFNULL(b.Q3,0), IFNULL(b.Q4, 0)  FROM jobs a
                           RIGHT JOIN (
                                        SELECT job_id,
                                        (CASE WHEN (strftime('%m', datetime)+0)>=1 and (strftime('%m', datetime)+0) < 4 THEN count(id) END) Q1,
                                        (CASE WHEN (strftime('%m', datetime)+0)>=4 and (strftime('%m', datetime)+0) < 7 THEN count(id) END) Q2,
                                        (CASE WHEN (strftime('%m', datetime)+0)>=7 and (strftime('%m', datetime)+0) < 10 THEN count(id) END) Q3,
                                        (CASE WHEN (strftime('%m', datetime)+0)>=10 and (strftime('%m', datetime)+0) <= 12 THEN count(id) END) Q4, 
                                        department_id 
                                        FROM hired_employees WHERE (strftime('%Y', datetime)+0) = 2021 and (job_id is not null and department_id is not null)
                                        GROUP BY job_id, department_id) b ON a.id = b.job_id
                           LEFT JOIN departments as c on b.department_id = c.id
                           GROUP BY a.job, c.name ORDER BY name, a.job
                           
                           ''')
            records = cursor.fetchall()
            return render_template('view_data.html', records=records)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/view_data1', methods=['GET'])
def view_data1():
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT id, name, hired FROM (
                            SELECT a.id, a.name, count(b.id) as hired, avg(c.cantidad) as avg_2021 FROM departments as a
                            LEFT JOIN hired_employees as b on a.id = b.department_id
                            LEFT JOIN ( 
                                        SELECT count(id) cantidad, department_id 
                                        FROM hired_employees
                                        WHERE (strftime('%Y', datetime)+0) = 2021
                                        GROUP BY department_id
                                      ) as c
                            GROUP BY a.id, a.name ORDER BY hired desc
                           ) WHERE hired > avg_2021
                           ''')
            records = cursor.fetchall()
            return render_template('view_data1.html', records=records)
    except Exception as e:
        return f"Error: {str(e)}", 500

# Call to the main program 
if __name__ == '__main__':
    init_db()
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)