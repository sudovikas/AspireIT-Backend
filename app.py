from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='vikas',
        password='aspireit@2024',
        database='aspireit'
    )

@app.route('/')
def dashboard():
    return 'Hello, World!'

@app.route('/children')
def children():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM children
        GROUP BY status;
    """)
    result = cursor.fetchall()
    conn.close()
    response = {"registered": 0, "active": 0, "inactive": 0}
    for row in result:
        response[row['status'].lower()] = row['count']
    return jsonify(response)

@app.route('/caregivers')
def caregivers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM caregivers
        GROUP BY status;
    """)
    result = cursor.fetchall()
    conn.close()
    response = {"registered": 0, "active": 0, "inactive": 0}
    for row in result:
        response[row['status'].lower()] = row['count']
    return jsonify(response)

@app.route('/attendance')
def attendance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT attendance_status, COUNT(*) as count
        FROM attendance
        WHERE attendance_date = CURDATE()
        GROUP BY attendance_status;
    """)
    result = cursor.fetchall()
    print(result)
    conn.close()
    response = {"ontime": 0, "late": 0, "day_off": 0, "not_present": 0}
    for row in result:
        response[row['attendance_status'].lower()] = row['count']
    return jsonify(response)

@app.route('/enrollments')
def enrollments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT month_name, enrollments_count
        FROM enrollments
        ORDER BY FIELD(month_name, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December');
    """)
    result = cursor.fetchall()
    conn.close()
    response = {row['month_name']: row['enrollments_count'] for row in result}
    return jsonify(response)

@app.route('/financials')
def financials():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT total_revenue, income, profit_margin, expenses
        FROM financials
        ORDER BY id DESC
        LIMIT 1;
    """)
    result = cursor.fetchone()
    conn.close()
    response = {
        "total_revenue": result['total_revenue'],
        "income": result['income'],
        "profit_margin": result['profit_margin'],
        "expenses": result['expenses']
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run()
