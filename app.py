from flask import Flask, render_template, request, session, redirect, url_for  
import time
import secrets

# Generate a secure secret key with 32 bytes (256 bits)
secret_key = secrets.token_hex(32)

print(secret_key)

app = Flask(__name__)
app.secret_key = secret_key  # Set a secret key for session management

# Store the start time of the quiz
start_time = None

# List of coding questions
questions = [
    {
        'question': 'Question 1: Write a function to add two numbers.',
        'answer': 'def add_numbers(a, b):\nreturn a + b'
    },
    {
        'question': 'Question 2: Write a function to find the factorial of a number.',
        'answer': 'def factorial(n):\nif n == 0:\nreturn 1\nelse:\nreturn n * factorial(n-1)'
    },
    {
        'question': 'Question 3: Write a function to check if a number is prime.',
        'answer': 'def is_prime(n):\nif n <= 1:\nreturn False\nfor i in range(2, int(n**0.5) + 1):\nif n % i == 0:\nreturn False\nreturn True'
    }
]

# Initialize question index
question_index = 0
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accept_terms', methods=['POST'])
def accept_terms():
    # Handle the user's acceptance of terms and conditions
    # You can perform any necessary logic here (e.g., record acceptance)
    return 'Quiz Started'

@app.route('/coding_round')
def coding_round():
    # Handle the coding round logic here
    # You can render a new HTML page for the coding round or redirect to it
    return 'This is the coding round. Good luck!' 

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    global start_time
    start_time = time.time()
    session['question_index'] = 0  # Initialize question index in session
    return 'Quiz started'

@app.route('/get_question', methods=['GET'])
def get_question():
    global start_time
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Check if 30 minutes have passed
    if elapsed_time >= 30 * 60:
        return 'Time is up! Quiz ended.'

    question_index = session.get('question_index', 0)  # Get question index from session
    if question_index >= len(questions):
        return 'Congratulations! You have completed the quiz.'

    return questions[question_index]['question']

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global start_time
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Check if 30 minutes have passed
    if elapsed_time >= 30 * 60:
        return 'Time is up! Quiz ended.'

    question_index = session.get('question_index', 0)  # Get question index from session
    user_answer = request.form.get('answer')
    correct_answer = questions[question_index]['answer']

    if user_answer.strip() == correct_answer.strip():
        session['question_index'] = question_index + 1  # Increment question index in session
        if question_index < len(questions) - 1:
            return 'Correct! Next question coming up...'
        else:
            # All questions are answered correctly, quiz completed.
            return 'Congratulations! You have completed the quiz.'
    else:
        return 'Incorrect. Please try again.'

if __name__ == '__main__':
    app.run(debug=True)
