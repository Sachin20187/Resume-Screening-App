import os
import joblib
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import pandas as pd
from new_model import preprocess_text, extract_text_from_pdf, extract_info

app = Flask(__name__, template_folder='templates')

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Imhere%404ualways@localhost/resume_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key'

# Database setup
db = SQLAlchemy(app)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    predicted_designation = db.Column(db.String(50), nullable=False)

# Load the SVM model and vectorizer
svm_model = joblib.load('svm_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Helper functions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# In-memory user storage for simplicity
users = {}

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error="Username already exists")
        users[username] = password
        session['username'] = username
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get the list of uploaded files and job role
        files = request.files.getlist('file')
        job_role = request.form.get('job_role')

        if not files or not job_role:
            return redirect(request.url)

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        all_info = []
        # Process each uploaded file
        for file in files:
            if file and allowed_file(file.filename):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)

                resume_text = extract_text_from_pdf(file_path)
                if not resume_text:
                    continue  # Skip if no text found in the resume

                resume_text_processed = preprocess_text(resume_text)
                resume_vectorized = vectorizer.transform([resume_text_processed])
                predicted_label = svm_model.predict(resume_vectorized)[0]

                info = extract_info(resume_text, job_role, vectorizer, svm_model)
                info['Filename'] = file.filename
                suitability = "Suitable" if job_role.strip().lower() == predicted_label.strip().lower() else "Not Suitable"

                # Save resume info into the database
                existing_resume = Resume.query.filter_by(filename=file.filename).first()
                if existing_resume:
                    db.session.delete(existing_resume)
                    db.session.commit()

                skills_list = info.get('Skills', [])
                cleaned_skills = [skill.strip() for skill in skills_list if skill.strip()]  # Remove extra spaces and empty strings
                info['Skills'] = ', '.join(cleaned_skills)

                # info['Skills'] = ', '.join(info.get('Skills', []))  # Ensure skills is a string

                resume_entry = Resume(
                    filename=file.filename,
                    name=info.get('Name'),
                    email=info.get('Email'),
                    phone=info.get('Phone'),
                    skills=info['Skills'],  # Use the processed string
                    predicted_designation=predicted_label,
                )
                db.session.add(resume_entry)
                db.session.commit()

                info['Suitability'] = suitability
                all_info.append(info)

        # Save data to session for persistence
        session['job_role'] = job_role
        session['all_info'] = all_info

        # If multiple files are uploaded, save the results to a CSV and render batch_result.html
        if len(files) > 1:
            if all_info:
                df = pd.DataFrame(all_info)
                csv_filename = 'batch_results.csv'
                session['csv_filename'] = csv_filename  # Save filename in session
                df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], csv_filename), index=False)
                return render_template('batch_result.html', csv_filename=csv_filename, info=all_info, job_role = job_role)

        # If only one file is uploaded, render result.html for a single result
        elif len(files) == 1 and all_info:
            session['predicted_label'] = predicted_label  # Save label in session
            session['single_info'] = all_info[0]  # Save single result info in session
            return render_template('result.html', label=predicted_label, info=all_info[0], suitability=all_info[0]['Suitability'])

    return redirect(url_for('index'))

@app.route('/batch_result', methods=['GET'])
def batch_result():
    job_role = session.get('job_role', 'Not Provided')
    all_info = session.get('all_info', [])
    csv_filename = session.get('csv_filename', None)
    return render_template('batch_result.html', job_role=job_role, info=all_info, csv_filename=csv_filename)

@app.route('/result', methods=['GET'])
def result():
    predicted_label = session.get('predicted_label', 'N/A')
    single_info = session.get('single_info', {})
    suitability = single_info.get('Suitability', 'Unknown')
    return render_template('result.html', label=predicted_label, info=single_info, suitability=suitability)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin12345':
            session['username'] = username
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error="Invalid username or password")
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('admin_login'))
    resumes = Resume.query.order_by(desc(Resume.id)).all()
    return render_template('admin_dashboard.html', resumes=resumes)

@app.route('/edit_resume/<int:resume_id>', methods=['GET', 'POST'])
def edit_resume(resume_id):
    resume = Resume.query.get(resume_id)
    if not resume:
        return "Resume not found", 404
    if request.method == 'POST':
        resume.name = request.form['name']
        resume.email = request.form['email']
        resume.phone = request.form['phone']
        resume.skills = request.form['skills']
        resume.predicted_designation = request.form['predicted_designation']
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_resume.html', resume=resume)

@app.route('/delete_resume/<int:resume_id>')
def delete_resume(resume_id):
    resume = Resume.query.get(resume_id)
    if not resume:
        return "Resume not found", 404
    db.session.delete(resume)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_logout')
def admin_logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/download_csv/<filename>')
def download_csv(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

