-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INTEGER NOT NULL,
    course VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO students (name, email, age, course) VALUES 
    ('Alice Johnson', 'alice@example.com', 20, 'Computer Science'),
    ('Bob Smith', 'bob@example.com', 22, 'Mathematics'),
    ('Carol Davis', 'carol@example.com', 21, 'Physics'),
    ('David Wilson', 'david@example.com', 23, 'Engineering'),
    ('Emma Brown', 'emma@example.com', 19, 'Biology')
ON CONFLICT (email) DO NOTHING;