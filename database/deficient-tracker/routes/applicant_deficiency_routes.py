from flask import Blueprint, render_template, request, redirect, url_for
from models import applicant_deficiency as model
from models import applicant as app_model

import random
app_def = Blueprint('app_def', __name__)

@app_def.route('/applicant_deficiencies')
def list_applicant_deficiencies():
    data = model.get_all_applicant_deficiencies()
    return render_template('applicant_with_deficiencies_list.html', deficiencies=data)

@app_def.route('/doc_deficiencies/<int:doc_id>/<int:app_id>')
def doc_deficiencies(doc_id,app_id):

    data = model.get_doc_deficiencies(doc_id,app_id)
    
    
    
    
    # return [data]

    # return re[nder_template('applicant_with_deficiencies_list.html', deficiencies=data)

    return render_template('cases.html', deficiencies=data,app_id = app_id,doc_type = data[0]["doc_name"])

@app_def.route('/applicant_deficiencies/insert/<int:applicant_id>/<int:deficiency_id>', methods=['GET'])
def insert_applicant_deficiency(applicant_id, deficiency_id):
    model.create_applicant_deficiency(applicant_id, deficiency_id, excuse=None)

    # Redirect back to the previous page
    return redirect(request.referrer or '/')


@app_def.route('/get_generated_response/<int:applicant_id>', methods=['GET'])
def get_generated_response(applicant_id):
        
    app_info = app_model.get_applicant_by_id(applicant_id)
    response = model.get_generated_response(applicant_id)
    # return [response]
    return render_template('generated_response.html',letter_content = response)

    # Redirect back to the previous page
    # return redirect(request.referrer or '/')



@app_def.route('/applicant_deficiencies/create', methods=['GET', 'POST'])
def create_applicant_deficiency():
    if request.method == 'POST':
        applicant_id = request.form['applicant_id']
        excuse = request.form['excuse']
        doc_id = request.form['doc_id']
        model.create_applicant_deficiency(applicant_id, excuse, doc_id)
        return redirect(url_for('app_def.list_applicant_deficiencies'))
    return render_template('applicant_deficiencies/create.html')

@app_def.route('/applicant_deficiencies/edit/<int:deficiency_id>', methods=['GET', 'POST'])
def edit_applicant_deficiency(deficiency_id):
    deficiency = model.get_applicant_deficiency(deficiency_id)
    if request.method == 'POST':
        applicant_id = request.form['applicant_id']
        excuse = request.form['excuse']
        doc_id = request.form['doc_id']
        model.update_applicant_deficiency(deficiency_id, applicant_id, excuse, doc_id)
        return redirect(url_for('app_def.list_applicant_deficiencies'))
    return render_template('applicant_deficiencies/edit.html', deficiency=deficiency)

@app_def.route('/applicant_deficiencies/delete/<int:deficiency_id>', methods=['POST'])
def delete_applicant_deficiency(deficiency_id):
    model.delete_applicant_deficiency(deficiency_id)
    return redirect(url_for('app_def.list_applicant_deficiencies'))
