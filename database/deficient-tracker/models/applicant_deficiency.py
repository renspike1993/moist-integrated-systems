import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='ched_so_db'
    )

# def get_all_applicant_deficiencies():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM applicant_deficiencies")
#     data = cursor.fetchall()
#     conn.close()
#     return data

def get_all_applicant_deficiencies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   select applicant.id as app_id, applicant.fullname , documents.doc_name, deficiencies.*
                    from applicant,documents,deficiencies,applicant_deficiencies
                    where applicant.id = applicant_deficiencies.applicant_id
                    and applicant_deficiencies.deficiencies_id = deficiencies.id
                    and deficiencies.doc_id = documents.doc_id
                    GROUP BY applicant.id                  
                   """)
    data = cursor.fetchall()
    conn.close()
    return data


def get_generated_response(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT applicant.id, documents.doc_name, deficiencies.description,
               deficiencies.acceptable_excuse, deficiencies.resolution_statement
        FROM applicant
        JOIN applicant_deficiencies ON applicant.id = applicant_deficiencies.applicant_id
        JOIN deficiencies ON applicant_deficiencies.deficiencies_id = deficiencies.id
        JOIN documents ON deficiencies.doc_id = documents.doc_id
        WHERE applicant.id = %s;
    """, (id,))  # ✅ Corrected single-element tuple

    data = cursor.fetchall()
    conn.close()
    return data




def get_all_applicant_deficiencies_by_applicant_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                    select applicant.id, documents.doc_name, deficiencies.description,deficiencies.prevalence,deficiencies.resolution_statement
                    from applicant,documents,deficiencies,applicant_deficiencies
                    where applicant.id = applicant_deficiencies.applicant_id
                    and applicant_deficiencies.deficiencies_id = deficiencies.id
                    and deficiencies.doc_id = documents.doc_id
                    and applicant.id = %s
                """,(id))
    data = cursor.fetchall()
    conn.close()
    return data

def get_doc_deficiencies(doc_id, app_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get document deficiencies by doc_id
    cursor.execute("""
        SELECT documents.*, deficiencies.*
        FROM documents
        JOIN deficiencies ON deficiencies.doc_id = documents.doc_id
        WHERE deficiencies.doc_id = %s
    """, (doc_id,))
    data = cursor.fetchall()


    # Add count to each document deficiency record
    for idx,doc_def in enumerate(data):
            # Get count of deficiencies for the applicant
        cursor.execute("""
            SELECT COUNT(*) as cnt
            FROM applicant_deficiencies,deficiencies
            WHERE applicant_deficiencies.applicant_id = %s
            and  applicant_deficiencies.deficiencies_id = deficiencies.id
            

        """, (app_id,))
        def_cnt = cursor.fetchone()['cnt']

        data[idx]['deficiency_count'] = def_cnt
        
        
    conn.close()
    return data




def get_applicant_deficiency(deficiency_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applicant_deficiencies WHERE deficiencies_id = %s", (deficiency_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def create_applicant_deficiency(deficiencies_id,applicant_id,excuse):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO applicant_deficiencies (deficiencies_id,applicant_id,excuse) VALUES (%s, %s, %s)",
        (deficiencies_id,applicant_id,excuse )
    )
    conn.commit()
    conn.close()

def update_applicant_deficiency(deficiency_id, applicant_id, excuse, doc_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE applicant_deficiencies SET applicant_id = %s, excuse = %s, id = %s WHERE deficiencies_id = %s",
        (applicant_id, excuse, doc_id, deficiency_id)
    )
    conn.commit()
    conn.close()

def delete_applicant_deficiency(deficiency_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applicant_deficiencies WHERE deficiencies_id = %s", (deficiency_id,))
    conn.commit()
    conn.close()
