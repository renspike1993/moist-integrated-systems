from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from db import get_connection
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():



    if request.method == 'POST':


        email = request.form['email']
        raw_password = request.form['password']
        hashed_password = hashlib.sha256(raw_password.encode()).hexdigest()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM examinee_tbl 
            WHERE exmne_email = %s AND exmne_password = %s
        """, (email, raw_password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['exmne_id'] = user['exmne_id']
            session['exmne_fullname'] = user['exmne_fullname']
            session['exmne_course'] = user['exmne_course']
            session['exmne_year_level'] = user['exmne_year_level']
            session['exmne_status'] = user['exmne_status']
            return redirect(url_for('auth.dashboard'))
        else:
            flash("Invalid email or password", "danger")
            
            
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exam_question_tbl")
    all_questions = cursor.fetchall()

    conn.close()

    # Categorize questions by subject
    categorized = {}
    for q in all_questions:
        subject = q['SUBJECT']
        if subject not in categorized:
            categorized[subject] = []
        categorized[subject].append(q)
        
    if 'exmne_id' in session:
        return render_template('entrance-exam/list.html', questions=categorized,user=session)

            
    return render_template('login.html')

@auth_bp.route('/dashboard')
def dashboard():
    if 'exmne_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exam_question_tbl")
    all_questions = cursor.fetchall()

    conn.close()
    conn.close()

    # Categorize questions by subject
    categorized = {}
    for q in all_questions:
        subject = q['SUBJECT']
        if subject not in categorized:
            categorized[subject] = []
        categorized[subject].append(q)

    # return categorized  # Or jsonify(categorized) if returning JSON
       
    return render_template('entrance-exam/list.html', questions=categorized,user=session)

    # return render_template('entrance-exam/list.html', user=session)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
