from flask import Flask, request, jsonify, render_template
import sqlite3
from werkzeug.security import quote as url_quote, generate_password_hash, check_password_hash
from datetime import datetime

print("Flask Version:", flask.__version__)
print("Werkzeug Version:", werkzeug.__version__)

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect('cyber_defender.db')
    # Create Leaderboard table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Leaderboard (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Score INTEGER NOT NULL,
            Date TEXT NOT NULL
        )
    ''')
    # Create Questions table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Questions (
            QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
            QuestionText TEXT NOT NULL,
            OptionA TEXT NOT NULL,
            OptionB TEXT NOT NULL,
            OptionC TEXT NOT NULL,
            OptionD TEXT NOT NULL,
            CorrectAnswer TEXT NOT NULL,
            Stage INTEGER NOT NULL
        )
    ''')
    # Create Users table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL UNIQUE,
            PasswordHash TEXT NOT NULL
        )
    ''')
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    password_hash = generate_password_hash(password)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users (Username, Email, PasswordHash) VALUES (?, ?, ?)',
                       (username, email, password_hash))
        conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already exists'}), 400
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT Username, PasswordHash FROM Users WHERE Email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user[1], password):
        return jsonify({'message': 'Login successful!', 'username': user[0]}), 200
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/questions/<int:stage>', methods=['GET'])
def get_questions(stage):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT QuestionID, QuestionText, OptionA, OptionB, OptionC, OptionD FROM Questions WHERE Stage = ?', (stage,))
    questions = cursor.fetchall()
    conn.close()
    formatted_questions = [
        {
            'id': q[0],
            'question': q[1],
            'options': {
                'A': q[2],
                'B': q[3],
                'C': q[4],
                'D': q[5]
            }
        } for q in questions
    ]
    return jsonify(formatted_questions), 200

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data.get('question_id')
    selected_answer = data.get('selected_answer')
    if not question_id:
        return jsonify({'error': 'Invalid data'}), 400
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT CorrectAnswer FROM Questions WHERE QuestionID = ?', (question_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        correct_answer = result[0]
        is_correct = (correct_answer == selected_answer)
        response = {
            'correct': is_correct,
            'points': 2.5 if is_correct else 0,
            'correctAnswer': correct_answer
        }
        return jsonify(response), 200
    return jsonify({'error': 'Question not found'}), 404

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.json
    username = data.get('username')
    score = data.get('score')
    if username is None or score is None:
        return jsonify({'error': 'Invalid data'}), 400
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Leaderboard (Username, Score, Date) VALUES (?, ?, ?)',
                   (username, score, date_str))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Score saved successfully!'}), 201

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT Username, Score, Date FROM Leaderboard ORDER BY Score DESC, Date ASC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()
    formatted_leaderboard = [{'username': row[0], 'score': row[1], 'date': row[2]} for row in rows]
    return jsonify(formatted_leaderboard), 200

if __name__ == '__main__':
    app.run(debug=True)

