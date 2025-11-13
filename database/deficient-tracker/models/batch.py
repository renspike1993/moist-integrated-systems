import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ched_so_db'
    )

# CREATE
def create_batch(program_id, date_of_graduation, deficiency_recommendation, deficiency_compliance, deficiency_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO batch (program_id, date_of_graduation, deficiency_recommendation, deficiency_compliance, deficiency_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (program_id, date_of_graduation, deficiency_recommendation, deficiency_compliance, deficiency_date))
    conn.commit()
    conn.close()

# READ ALL
def get_all_batches():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM batch")
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_programs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM programs")
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_applicants_no_batch():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applicant where batch_id IS NULL")
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_applicants_with_batch(batch_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"""SELECT * FROM applicant where batch_id = {batch_id}""")
    data = cursor.fetchall()
    conn.close()
    return data


def remove_deficient_applicant_by_id(applicant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE applicant SET batch_id=NULL WHERE id=%s
    """
    cursor.execute(sql, (applicant_id,))
    conn.commit()
    conn.close()


def update_applicant_batch(batch_id,applicant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE applicant SET batch_id=%s WHERE id=%s
    """
    cursor.execute(sql, (batch_id,applicant_id))
    conn.commit()
    conn.close()

# READ by ID
def get_batch(batch_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM batch WHERE id = %s", (batch_id,))
    data = cursor.fetchall()
    conn.close()
    return data




# UPDATE
def update_batch(old_program_id, old_date_of_graduation, old_id,
                 new_program_id, new_date_of_graduation, new_deficiency_recommendation,
                 new_deficiency_compliance, new_deficiency_date, new_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE batch
        SET program_id = %s,
            date_of_graduation = %s,
            deficiency_recommendation = %s,
            deficiency_compliance = %s,
            deficiency_date = %s,
            id = %s
        WHERE program_id = %s AND date_of_graduation = %s AND id = %s
    """, (
        new_program_id, new_date_of_graduation, new_deficiency_recommendation,
        new_deficiency_compliance, new_deficiency_date, new_id,
        old_program_id, old_date_of_graduation, old_id
    ))
    conn.commit()
    conn.close()


# UPDATE
def update_bat(deficiency_recommendation,deficiency_compliance, batch_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE batch
        SET deficiency_recommendation = %s,
            deficiency_compliance = %s
        WHERE id = %s
    """, (deficiency_recommendation,deficiency_compliance, batch_id))
    conn.commit()
    conn.close()


def save_history(body,batch_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
            "INSERT INTO submission_history (body, batch_id) VALUES (%s, %s)",
            (body, batch_id)
        )
    conn.commit()
    conn.close()

def get_history(history_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM submission_history WHERE id = %s", (history_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def get_history_by_batch(batch_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM submission_history WHERE batch_id = %s", (batch_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_all_history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM submission_history")
    data = cursor.fetchall()
    conn.close()
    return data

def count_history_by_batch(batch_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT count(id) FROM submission_history where batch_id",(batch_id,))
    data = cursor.fetchall()
    conn.close()
    return data


# DELETE
def delete_batch(batch_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM batch
        WHERE id = %s
    """, (batch_id,))
    conn.commit()
    conn.close()
