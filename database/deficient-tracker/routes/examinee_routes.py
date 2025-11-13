from flask import Blueprint, render_template, request, redirect, url_for
import mysql.connector

questions_bp = Blueprint('questions', __name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="exam"
    )


@questions_bp.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM exam_question_tbl")
    all_questions = cursor.fetchall()

    cursor.close()
    conn.close()

    # Categorize questions by subject
    categorized = {}
    for q in all_questions:
        subject = q['SUBJECT']
        if subject not in categorized:
            categorized[subject] = []
        categorized[subject].append(q)

    # return categorized  # Or jsonify(categorized) if returning JSON
       
    return render_template('entrance-exam/list.html', questions=categorized)


@questions_bp.route('/dashboard')
def dashboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
                   
SELECT 
    exam_answers.axmne_id,
    examinee_tbl.exmne_fullname,
    course_tbl.cou_name,
    SUM(CASE 
        WHEN exam_question_tbl.SUBJECT = 'ENGLISH' 
             AND exam_answers.exans_answer = exam_question_tbl.exam_answer 
        THEN 1 ELSE 0 
    END) AS english_score,

    SUM(CASE 
        WHEN exam_question_tbl.SUBJECT = 'MATHEMATICS' 
             AND exam_answers.exans_answer = exam_question_tbl.exam_answer 
        THEN 1 ELSE 0 
    END) AS math_score,

    SUM(CASE 
        WHEN exam_question_tbl.SUBJECT = 'ABSTRACT' 
             AND exam_answers.exans_answer = exam_question_tbl.exam_answer 
        THEN 1 ELSE 0 
    END) AS abstract_score,

    SUM(CASE 
        WHEN exam_question_tbl.SUBJECT = 'SCIENCE' 
             AND exam_answers.exans_answer = exam_question_tbl.exam_answer 
        THEN 1 ELSE 0 
    END) AS science_score,
    
    SUM(CASE 
        WHEN exam_question_tbl.SUBJECT IN ('ENGLISH', 'MATHEMATICS', 'ABSTRACT', 'SCIENCE') 
             AND exam_answers.exans_answer = exam_question_tbl.exam_answer 
        THEN 1 
        ELSE 0 
    END) AS total_score

FROM 
    exam_answers
JOIN 
    exam_question_tbl ON exam_answers.eqt_id = exam_question_tbl.eqt_id
JOIN 
    examinee_tbl ON exam_answers.axmne_id = examinee_tbl.exmne_id
JOIN
	course_tbl ON examinee_tbl.exmne_course = course_tbl.cou_id
WHERE 
    exam_question_tbl.SUBJECT IN ('ENGLISH', 'MATHEMATICS', 'ABSTRACT', 'SCIENCE')

GROUP BY 
    exam_answers.axmne_id, 
    examinee_tbl.exmne_fullname,
    examinee_tbl.exmne_course

ORDER BY 
    total_score DESC
LIMIT 10;
                   
                   """)
    top_10 = cursor.fetchall()

    cursor.close()
    conn.close()

    # return top_10
    # return categorized  # Or jsonify(categorized) if returning JSON
       
    return render_template('entrance-exam/dashboard.html', data= top_10)

@questions_bp.route('/create', methods=['GET', 'POST'])
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
        return redirect(url_for('questions.index'))
    return render_template('create.html')

@questions_bp.route('/update/<int:eqt_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('questions.index'))
    else:
        cursor.execute("SELECT * FROM exam_question_tbl WHERE eqt_id = %s", (eqt_id,))
        question = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('update.html', question=question)

@questions_bp.route('/delete/<int:eqt_id>', methods=['POST'])
def delete(eqt_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exam_question_tbl WHERE eqt_id = %s", (eqt_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('questions.index'))
