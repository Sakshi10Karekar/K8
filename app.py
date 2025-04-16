from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# Environment-based configuration
HOST_NAME = os.environ.get('DB_HOST', 'db')  # Use 'db' since it's the service name in docker-compose.yml
DATABASE_NAME = os.environ.get('DB_NAME', 'postgres')
PORT = int(os.environ.get('DB_PORT', 5432))
PASSWORD = os.environ.get('DB_PASS', 'postgres')
DATABASE_USER = os.environ.get('DB_USER', 'postgres')

def get_connection():
    # Adjusting to use the correct host from docker-compose
    return psycopg2.connect(
        host=HOST_NAME,
        dbname=DATABASE_NAME,
        port=PORT,
        password=PASSWORD,
        user=DATABASE_USER
    )

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student_info (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            qualification TEXT,
            board TEXT,
            passing_year TEXT,
            percentage TEXT,
            address TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_student(name, email, phone, qualification, board, passing_year, percentage, address):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO student_info (name, email, phone, qualification, board, passing_year, percentage, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, email, phone, qualification, board, passing_year, percentage, address))
    conn.commit()
    cur.close()
    conn.close()

def fetching():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student_info")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

@app.route('/')
def personal():
    return render_template('personal.html')

@app.route('/educational', methods=['POST'])
def educational():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    return render_template('educational.html', name=name, email=email, phone=phone)

@app.route('/submited_data', methods=['POST'])
def mydata():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    qualification = request.form['qualification']
    brd = request.form['board']
    passing_year = request.form['year']
    percentage = request.form['score']
    address = request.form['address']
    insert_student(name, email, phone, qualification, brd, passing_year, percentage, address)
    return render_template(
        'submited_data.html',
        qualification=qualification, board=brd, p_year=passing_year, percentage=percentage,
        name=name, email=email, phone=phone, address=address
    )

@app.route('/show_data', methods=['POST'])
def database_data():
    student = fetching()
    return render_template('show_data.html', student=student)

@app.route('/search_data', methods=['GET', 'POST'])
def search_data():
    if request.method == 'POST':
        searchName = request.form.get('search_name')
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM student_info WHERE name = %s", (searchName,))
        data = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('search_data.html', data=data)
    return render_template('search_data.html', data=None)

@app.route('/delete_data', methods=['POST'])
def delete_data():
    student_id = request.form['id']
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM student_info WHERE id = %s", (student_id,))
    conn.commit()
    cur.close()
    conn.close()
    return "Record Deleted Successfully"

@app.route('/update', methods=['POST'])
def update_data1():
    student_id1 = request.form['id1']
    return render_template('update.html', student_id1=student_id1)

@app.route('/update_data', methods=['POST'])
def update_data():
    student_id1 = request.form['id1']
    name1 = request.form['name1']
    phone1 = request.form['phone1']
    email1 = request.form['email1']
    address1 = request.form['address1']
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE student_info SET name=%s, phone=%s, email=%s, address=%s WHERE id=%s",
        (name1, phone1, email1, address1, student_id1)
    )
    conn.commit()
    cur.close()
    conn.close()
    return "Updated Record Successfully"

@app.route('/thankyou', methods=['POST'])
def last():
    return render_template('thankyou.html')

if __name__ == "__main__":
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)

