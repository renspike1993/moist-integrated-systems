from flask import Flask
from routes.applicant_routes import applicants
# from routes.batches import applicants
# from routes.applicant_deficiency_routes import app_def
# from routes.examinee_routes import questions_bp
from routes.auth import auth_bp
# from routes.exam_answers import answers_bp
from routes.batches import batches
import models.batch as mbatch
import hashlib
from flask_cors import CORS
app = Flask(__name__)
CORS(app) 
app.secret_key = 'your_secret_key'

@app.template_filter('sha256')
def sha256_filter(value):
    return hashlib.sha256(str(value).encode()).hexdigest()[:7]

@app.template_filter('cnt_attempts')
def count_attempts(value):        
    return len(mbatch.get_history_by_batch(value))

app.register_blueprint(batches, url_prefix='/batches')
# app.register_blueprint(auth_bp,url_prefix='/auth')

app.register_blueprint(applicants,url_prefix='/applicants')
# app.register_blueprint(app_def)
# app.register_blueprint(questions_bp, url_prefix='/questions')
# app.register_blueprint(auth_bp,url_prefix='/auth')
# app.register_blueprint(answers_bp,url_prefix='/answers')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded = True)
