#!/usr/bin/env python3
import os
import sys
import psycopg2
import urllib.parse

def init_database():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_PORT = os.getenv('DB_PORT', '5432')
        DB_NAME = os.getenv('DB_NAME', 'student_db')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = urllib.parse.quote_plus(os.getenv('DB_PASSWORD', 'Vi1279_@2004'))
        DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
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
        
        cur.execute('''
            INSERT INTO students (name, email, age, course) VALUES 
                ('Alice Johnson', 'alice@example.com', 20, 'Computer Science'),
                ('Bob Smith', 'bob@example.com', 22, 'Mathematics'),
                ('Carol Davis', 'carol@example.com', 21, 'Physics'),
                ('David Wilson', 'david@example.com', 23, 'Engineering'),
                ('Emma Brown', 'emma@example.com', 19, 'Biology')
            ON CONFLICT (email) DO NOTHING
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Database initialization: {e}")

if __name__ == '__main__':
    init_database()