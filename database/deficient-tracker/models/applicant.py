import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ched_so_db'
    )



def get_all_applicants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applicant")
    applicants = cursor.fetchall()
    conn.close()
    return applicants


def get_all_applicant_requirements(applicant_id, program_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    applicant_id = 1
    program_id = 'BSIT'
    # Use parameterized values instead of hardcoded ones
    
    cursor.execute("""
        SELECT documents.doc_id, documents.doc_name
        FROM applicant
        JOIN programs ON applicant.program_id = programs.program_id
        JOIN program_documents ON programs.program_id = program_documents.program_id
        JOIN documents ON program_documents.doc_id = documents.doc_id
        WHERE applicant.program_id = %s
          AND applicant.id = %s
    """,(program_id,applicant_id))
    
    applicants_requirements = cursor.fetchall()

    for app_req in applicants_requirements:
        cursor.execute("SELECT * FROM deficiencies WHERE doc_id = %s", (app_req['doc_id'],))
        app_req['deficiencies'] = cursor.fetchall()  # attach deficiencies directly to each requirement


    conn.close()
    return applicants_requirements


def get_applicant_by_id(applicant_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applicant WHERE id = %s", (applicant_id,))
    applicant = cursor.fetchone()
    conn.close()
    return applicant

def get_all_programs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM programs")
    applicant = cursor.fetchall()
    conn.close()
    return applicant


def insert_applicant(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO applicant (fullname, program_id,contact_number, email)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['fullname'], data['program_id'],
        data['contact_number'], data['email']
    ))
    conn.commit()
    conn.close()




def update_applicant(applicant_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        UPDATE applicant SET fullname=%s, program_id=%s,
        contact_number=%s, email=%s WHERE id=%s
    """
    cursor.execute(sql, (
        data['fullname'], data['program_id'],
        data['contact_number'], data['email'], applicant_id
    ))
    conn.commit()
    conn.close()

def delete_applicant(applicant_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applicant WHERE id = %s", (applicant_id,))
    conn.commit()
    conn.close()
