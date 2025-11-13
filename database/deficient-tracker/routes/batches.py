from flask import Blueprint, session,flash, render_template, request, redirect, url_for,jsonify
from models import batch as model
from math import ceil
batches = Blueprint('batches', __name__)





@batches.route('/')
def index():
    all_batches = model.get_all_batches()
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = len(all_batches)
    total_pages = ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    batch_slice = all_batches[start:end]

    return render_template('batch/index.html', batches=batch_slice, page=page, total_pages=total_pages)

@batches.route('/dashboard')
def dashboard():
    return render_template('dashboard/index.html')


@batches.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        model.create_batch(
            request.form['program_id'],
            request.form['date_of_graduation'],
            request.form['deficiency_recommendation'],
            request.form['deficiency_compliance'],
            request.form['deficiency_date']
        )
        return redirect(url_for('batches.index'))


    return render_template('batch/form.html', batch=None, programs = model.get_all_programs() )



@batches.route('/add_applicants/<int:batch_id>', methods=['GET', 'POST'])
def add_applicants(batch_id):

    all_applicants = model.get_all_applicants_no_batch()  # Do not change this

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
        'batch/batch_applicants.html',
        applicants=applicants,
        page=page,
        total_pages=total_pages,
        batch_id = batch_id
        
    )
    # return model.get_all_applicants()
    # return render_template('batch/batch_applicants.html', batch=None, programs = model.get_all_programs() )


@batches.route('/add_applicant_to_cases/<int:batch_id>/<int:applicant_id>', methods=['GET', 'POST']) 
def update_applicant_batch(batch_id, applicant_id):
    model.update_applicant_batch(batch_id, applicant_id)
    flash('Successful', 'success')

    return redirect(request.referrer or '/')  # fallback to home if no referrer
    # return redirect(url_for('applicants.index'))  # or wherever you want to go next

@batches.route('/remove_deficient_applicant_by_id/<int:applicant_id>', methods=['GET', 'POST']) 
def remove_deficient_applicant_by_id(applicant_id):
    model.remove_deficient_applicant_by_id(applicant_id)
    # return [applicant_id]
    flash('Successful', 'success')
    # model.remove_deficient_applicant(applicant_id)
    return redirect(request.referrer or '/')  # fallback to home if no referrer
    # return redirect(url_for('applicants.index'))  # or wherever you want to go next



@batches.route('/response/<int:batch_id>', methods=['GET', 'POST']) 
def response(batch_id):
    all_applicants = model.get_all_applicants_with_batch(batch_id)
    get_batch = model.get_batch(batch_id)
    recommendation = get_batch[0]["deficiency_recommendation"]
    compliance = get_batch[0]["deficiency_compliance"]
    # return [get_batch[0]["deficiency_recommendation"]]
    return render_template('batch/response.html',applicants = all_applicants,batch_id = batch_id,recommendation = recommendation, compliance = compliance)



@batches.route('/generate_response/<int:batch_id>', methods=['GET', 'POST']) 
def generate_response(batch_id):
    all_applicants = model.get_all_applicants_with_batch(batch_id)
    get_batch = model.get_batch(batch_id)
    recommendation = get_batch[0]["deficiency_recommendation"]
    compliance = get_batch[0]["deficiency_compliance"]

    # return [get_batch[0]["deficiency_recommendation"]]
    return render_template('batch/generated_response.html',applicants = all_applicants,batch_id = batch_id,recommendation = recommendation, compliance = compliance)



@batches.route('/history', methods=['GET'])
def history():
    all_history = model.get_all_history()
    # return all_history
    return render_template('batch/history.html',all_history = all_history)
    # return redirect(request.referrer or '/')  # fallback to home if no referrer



@batches.route('/submit-history', methods=['POST'])
def submit_history():
    data = request.get_json()
    body = data.get('let_content')
    batch_id = data.get('batch_id')
    model.save_history(body,batch_id)


    return redirect(request.referrer or '/')  # fallback to home if no referrer

@batches.route('/show_history/<int:history_id>', methods=['POST','GET'])
def show_history(history_id):    
    history_cotent = model.get_history(history_id)
    return render_template('batch/generated_response_history.html',history_content = history_cotent)


@batches.route('/show_history_by_batch/<int:batch_id>', methods=['POST','GET'])
def show_history_by_batch(batch_id):    
    history_cotent = model.get_history_by_batch(batch_id)
    return render_template('batch/history.html',all_history = history_cotent)



@batches.route('/update/<int:batch_id>', methods=['GET', 'POST'])
def update_bat(batch_id):
    if request.method == 'POST':
        model.update_bat(
            # old_program_id=request.form['old_program_id'],
            # old_date_of_graduation=request.form['old_date_of_graduation'],
            # old_id=id,
            # new_program_id=request.form['program_id'],
            # new_date_of_graduation=request.form['date_of_graduation'],
            deficiency_recommendation=request.form['deficiency_recommendation'],
            deficiency_compliance=request.form['deficiency_compliance'],
            batch_id = batch_id
            # new_deficiency_date=request.form['deficiency_date'],
            # new_id=request.form['id']
        )
        session['swal_message'] = {
                'title': 'Removed!',
                'text': 'Applicant successfully removed from deficient list.',
                'icon': 'success'
            }
        # return [request.form['deficiency_recommendation'],request.form['deficiency_compliance'],batch_id]
        return redirect(request.referrer or '/')  # fallback to home if no referrer
        # return redirect(url_for('batches.index'))

    batch = model.get_batch(batch_id)
    return render_template('batch/form.html', batch=batch[0] if batch else None, programs = model.get_all_programs() )




@batches.route('/delete/<int:id>')
def delete(id):
    batch = model.get_batch(id)
    if batch:
        model.delete_batch(
            batch_id=batch[0]['id']
        )
    flash('Successful', 'success')    
    return redirect(url_for('batches.index'))
