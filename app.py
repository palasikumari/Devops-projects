import os
import psycopg2
from flask import Flask, render_template_string, request, redirect, url_for
import time
# --- Configuration ---
DB_HOST = os.environ.get('DB_HOST', 'db')  # 'db' is the service name in docker-compose
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASS = os.environ.get('DB_PASS', 'mypassword')

app = Flask(__name__)

# --- Database Connection and Setup ---
def get_db_connection():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn
time.sleep(5)

def init_db():
    # Attempt to connect and initialize the table
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        # Create the messages table if it doesn't exist
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id serial PRIMARY KEY,
                content varchar(150) NOT NULL
            );
            """
        )
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        # In a real app, you'd implement retry logic here

# Initialize the database on startup
init_db()

# --- Flask Routes ---
@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        # Handle form submission to add a new message
        content = request.form['content']
        if content:
            cur.execute("INSERT INTO messages (content) VALUES (%s)", (content,))
            conn.commit()
            return redirect(url_for('index'))
    # Fetch all messages for display
    cur.execute('SELECT * FROM messages;')
    messages = cur.fetchall()
    cur.close()
    conn.close()
    # Simple HTML template for the page
    html_template = """
    <!doctype html>
    <title>Docker Multi-Container Lab</title>
    <h1>Messages</h1>
    <form method="post">
        <label for="content">New Message:</label>
        <input type="text" name="content" required>
        <button type="submit">Add</button>
    </form>
    <hr>
    {% for message in messages %}
        <p><strong>ID {{ message[0] }}:</strong> {{ message[1] }}</p>
    {% endfor %}
    """
    return render_template_string(html_template, messages=messages)

if __name__ == '__main__':
    # Use host '0.0.0.0' to make the app accessible outside the container
    app.run(debug=True, host='0.0.0.0', port=5000)