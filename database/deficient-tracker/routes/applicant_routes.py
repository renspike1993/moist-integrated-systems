from flask import Blueprint, render_template, request, redirect, url_for
from models import applicant as model
from math import ceil


applicants = Blueprint('applicants', __name__)

# @applicants.route('/')
# def index():
#     all_applicants = model.get_all_applicants()
#     return render_template('index.html', applicants=all_applicants)

@applicants.route('/')
def index():
    all_applicants = model.get_all_applicants()  # Do not change this

    # Pagination settings
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = len(all_applicants)
    total_pages = ceil(total / per_page)

    # Slice data
    start = (page - 1) * per_page
    end = start + per_page
    applicants = all_applicants[start:end]

    return render_template(
        'applicant/index.html',
        applicants=applicants,
        page=page,
        total_pages=total_pages
    )




    
@applicants.route('/get_all_requirements/<int:id>/<string:program>')
def get_all_requirements(id, program):
    # Use the parameters as needed
    all_requirements = model.get_all_applicant_requirements(id, program)
    applicant_info = model.get_applicant_by_id(id)
    # return requirements
    return render_template('requirements.html', requirements=all_requirements,applicant = applicant_info,programs = model.get_all_programs())


@applicants.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        model.insert_applicant(request.form)
        return redirect(url_for('applicants.index'))
    # return     model.get_all_programs()
    return render_template('form.html', applicant=None,programs = model.get_all_programs())

@applicants.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        model.update_applicant(id, request.form)
        return redirect(url_for('applicants.index'))
    applicant = model.get_applicant_by_id(id)
    return render_template('form.html', applicant=applicant)

@applicants.route('/delete/<int:id>')
def delete(id):
    model.delete_applicant(id)
    return redirect(url_for('applicants.index'))
