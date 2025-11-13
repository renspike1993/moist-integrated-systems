from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from db import get_connection  # assumes you have get_connection() in db.py
import jsonify

from flask_cors import CORS
from colorama import Fore, Style, init
# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

init()


answers_bp = Blueprint('answers', __name__, url_prefix='/answers')

CORS(answers_bp) 

@answers_bp.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exam_answers")
    answers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('answers/index.html', answers=answers)

@answers_bp.route('/submit_exam', methods=['POST'])
def submit_exam():
    action = request.form.get('action')
    if action == 'submit':
        # Save and finalize answers
        flash("Answers submitted successfully!", "success")
    elif action == 'later':
        # Save partial answers or flag for later
        flash("You chose to answer later.", "info")
    return redirect(url_for('some_page'))
from flask import request, session, jsonify
from flask_cors import cross_origin

@answers_bp.route("/submit-answer", methods=["POST"])
@cross_origin()  # Optional: enable if you're calling from a different origin
def submit_answer():
    data = request.get_json()
    exm_id = session.get('exmne_id')
    fname = session.get('exmne_fullname')    
    question_id = data.get("question_id")
    selected_answer = data.get("selected_answer")

    if not exm_id or not question_id or not selected_answer:
        return jsonify({"error": "Missing data"}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get correct answer
    cursor.execute("SELECT exam_answer FROM exam_question_tbl WHERE eqt_id = %s", (question_id,))
    question = cursor.fetchone()



    if not question:
        return jsonify({"error": "Question not found"}), 404

    correct_answer = question['exam_answer']
    result = f"{Fore.RED}INCORRECT{Style.RESET_ALL}"
    updated_score = None

    # Only update score if answer is correct
    if selected_answer == correct_answer:
        result = f"{Fore.GREEN}CORRECT{Style.RESET_ALL}" 
        cursor.execute("UPDATE examinee_tbl SET score = score + 1 WHERE exmne_id = %s", (exm_id,))
        conn.commit()

    # Fetch current score after potential update
    cursor.execute("SELECT score FROM examinee_tbl WHERE exmne_id = %s", (exm_id,))
    score_data = cursor.fetchone()
    updated_score = score_data["score"] if score_data else None

    cursor.close()
    conn.close()
    # Determine if the answer is correct (assuming result is a boolean)

    # Print with the icon
    exmnee  =  f"{Fore.YELLOW}{fname}{Style.RESET_ALL}"
    print(f"Examinee: {exm_id}. {exmnee} | Question ID: {question_id} | Answer: {selected_answer} | Result: {result} | Score: {updated_score}")

    return jsonify({
        "question_id": question_id,
        "selected_answer": selected_answer,
        "correct_answer": correct_answer,
        "result": result,
        "score": updated_score
    }), 200



@answers_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO exam_answers (axmne_id, exam_id, quest_id, exans_answer)
        VALUES (%s, %s, %s, %s)
        """
        data = (
            request.form['axmne_id'],
            request.form['exam_id'],
            request.form['quest_id'],
            request.form['exans_answer']
        )
        cursor.execute(sql, data)
        conn.commit()
        cursor.close()
        conn.close()
        flash('Answer submitted successfully.', 'success')
        return redirect(url_for('answers.index'))
    return render_template('answers/create.html')


@answers_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        sql = """
        UPDATE exam_answers
        SET axmne_id=%s, exam_id=%s, quest_id=%s, exans_answer=%s
        WHERE id=%s
        """
        data = (
            request.form['axmne_id'],
            request.form['exam_id'],
            request.form['quest_id'],
            request.form['exans_answer'],
            id
        )
        cursor.execute(sql, data)
        conn.commit()
        flash('Answer updated successfully.', 'info')
        return redirect(url_for('answers.index'))
    else:
        cursor.execute("SELECT * FROM exam_answers WHERE id = %s", (id,))
        answer = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('answers/update.html', answer=answer)


@answers_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exam_answers WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Answer deleted successfully.', 'danger')
    return redirect(url_for('answers.index'))
