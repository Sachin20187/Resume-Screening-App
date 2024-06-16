import os
import joblib
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from model import preprocess_text, extract_text_from_pdf, extract_info

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Update the SQLAlchemy database URI to connect to MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/resume_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_key'

db = SQLAlchemy(app)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False, unique=True)  # Ensure filename is unique
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    predicted_designation = db.Column(db.String(50), nullable=False)
    # job_suitability = db.Column(db.String(50), nullable=False)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load the model and vectorizer
model = joblib.load('logistic_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

users = {}

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
    if request.method == ['POST']:
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
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        job_role = request.form.get('job_role')

        if file and allowed_file(file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Extract text from the uploaded PDF
            resume_text = extract_text_from_pdf(file_path)
            if not resume_text:
                return 'No text found in the PDF. Please check the file content.'

            # Preprocess the resume text
            resume_text_processed = preprocess_text(resume_text)
            resume_vectorized = vectorizer.transform([resume_text_processed])

            # Predict the label of the resume
            predicted_label = model.predict(resume_vectorized)[0]

            info = extract_info(resume_text, job_role)
            info['Filename'] = file.filename

            suitability = "Suitable" if job_role.strip().lower() == predicted_label.strip().lower() else "Not Suitable"

            # Check for duplicates
            existing_resume = Resume.query.filter_by(filename=file.filename).first()
            if existing_resume:
                db.session.delete(existing_resume)
                db.session.commit()

            # Save to the database
            resume_entry = Resume(
                filename=file.filename,
                name=info.get('Name'),
                email=info.get('Email'),
                phone=info.get('Phone'),
                skills=', '.join(info.get('Skills', [])),
                predicted_designation=predicted_label,
                # job_suitability=suitability
            )
            db.session.add(resume_entry)
            db.session.commit()

            # Debug: Check if the info dictionary has the correct data
            print("Info dictionary:", info)
            print("Predicted label:", predicted_label)
            print("Suitability:", suitability)
            
            return render_template('result.html', label=predicted_label, info=info, suitability=suitability)
    return redirect(url_for('index'))

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin12345':
            session['username'] = username
            print("Admin logged in")  # Debug statement
            return redirect(url_for('admin_dashboard'))
        print("Invalid login attempt")  # Debug statement
        return render_template('admin_login.html', error="Invalid username or password")
    return render_template('admin_login.html')


# from sqlalchemy import desc
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' not in session or session['username'] != 'admin':
        print("Unauthorized access attempt to admin dashboard")  # Debug statement
        return redirect(url_for('admin_login'))
    resumes = Resume.query.order_by(desc(Resume.id)).all()  # Newest resumes first
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
        # resume.job_suitability = request.form['job_suitability']
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
