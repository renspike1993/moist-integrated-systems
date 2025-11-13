from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_pass",
        database="exam"
    )

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exam_question_tbl")
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('list.html', questions=questions)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO exam_question_tbl
        (exam_id, SUBJECT, exam_question, exam_ch1, exam_ch2, exam_ch3, exam_ch4, exam_ch5, exam_answer, exam_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            request.form['exam_id'],
            request.form['SUBJECT'],
            request.form['exam_question'],
            request.form['exam_ch1'],
            request.form['exam_ch2'],
            request.form['exam_ch3'],
            request.form['exam_ch4'],
            request.form['exam_ch5'],
            request.form['exam_answer'],
            request.form['exam_status']
        )
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:eqt_id>', methods=['GET', 'POST'])
def update(eqt_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        sql = """
        UPDATE exam_question_tbl SET
            exam_id=%s, SUBJECT=%s, exam_question=%s,
            exam_ch1=%s, exam_ch2=%s, exam_ch3=%s,
            exam_ch4=%s, exam_ch5=%s, exam_answer=%s, exam_status=%s
        WHERE eqt_id=%s
        """
        data = (
            request.form['exam_id'],
            request.form['SUBJECT'],
            request.form['exam_question'],
            request.form['exam_ch1'],
            request.form['exam_ch2'],
            request.form['exam_ch3'],
            request.form['exam_ch4'],
            request.form['exam_ch5'],
            request.form['exam_answer'],
            request.form['exam_status'],
            eqt_id
        )
        cursor.execute(sql, data)
        conn.commit()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM exam_question_tbl WHERE eqt_id = %s", (eqt_id,))
        question = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('update.html', question=question)

@app.route('/delete/<int:eqt_id>', methods=['POST'])
def delete(eqt_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exam_question_tbl WHERE eqt_id = %s", (eqt_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
