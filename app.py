from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('student_management_app_info', 'Student Management System', version='1.0.0')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    import urllib.parse
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'student_db')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = urllib.parse.quote_plus(os.getenv('DB_PASSWORD', 'Vi1279_@2004'))
    DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            age INTEGER NOT NULL,
            course VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM students ORDER BY id')
    students = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(student) for student in students])

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM students WHERE id = %s', (student_id,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    if student:
        return jsonify(dict(student))
    return jsonify({"error": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    if not all(k in data for k in ('name', 'email', 'age', 'course')):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(
            'INSERT INTO students (name, email, age, course) VALUES (%s, %s, %s, %s) RETURNING *',
            (data['name'], data['email'], data['age'], data['course'])
        )
        student = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(dict(student)), 201
    except psycopg2.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Check if student exists
    cur.execute('SELECT * FROM students WHERE id = %s', (student_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "Student not found"}), 404
    
    # Update student
    update_fields = []
    values = []
    for field in ['name', 'email', 'age', 'course']:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])
    
    if not update_fields:
        return jsonify({"error": "No fields to update"}), 400
    
    values.append(student_id)
    query = f"UPDATE students SET {', '.join(update_fields)} WHERE id = %s RETURNING *"
    
    try:
        cur.execute(query, values)
        student = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(dict(student))
    except psycopg2.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM students WHERE id = %s RETURNING id', (student_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    if deleted:
        return jsonify({"message": "Student deleted successfully"})
    return jsonify({"error": "Student not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)