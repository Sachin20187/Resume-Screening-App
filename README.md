🌟 Resume Screening Application 🌟
This application automates resume screening by extracting relevant information from resumes, predicting job roles, and determining suitability for a given position. It uses Machine Learning models and Natural Language Processing (NLP) techniques for text processing, feature extraction, and prediction.

🌟 Features
📄 Resume Parsing: Extracts text from resumes in PDF format using pdfplumber.             
🧠 Skill Extraction: Identifies skills like Python, Java, AWS, and more.           
🎯 Designation Prediction: Uses an SVM model to predict the most likely job designation.            
✅ Suitability Assessment: Compares the predicted designation with the desired job role.            
💾 Database Integration: Stores and retrieves resume data using a MySQL database.             
🛡️ Admin Dashboard: Manage all resumes with admin capabilities.          
🚀 Batch Processing: Upload multiple resumes and generate a consolidated CSV report.      

💻 Technologies Used
Backend: 🐍 Python, Flask, SQLAlchemy     
Database: 🛢️ MySQL      
Machine Learning: 🤖 Scikit-learn, joblib      
NLP Tools: 🔠 NLTK, spaCy, TfidfVectorizer      
Frontend: 🌐 HTML, CSS (Bootstrap)      
File Processing: 📂 pdfplumber      
Model: Support Vector Machine (SVM)        

🛠️ Setup Instructions
1. Clone the Repository
git clone https://github.com/Sachin20187/Resume-Screening-App.git
cd Resume-Screening-App

2. Install Dependencies
Ensure Python 3.8+ is installed. Run the following command:
pip install -r requirements.txt
python -m spacy download en_core_web_sm

3. Set Up MySQL Database
Create a MySQL database named resume_db.
Update app.config['SQLALCHEMY_DATABASE_URI'] in the Flask app with your MySQL credentials.

4. Initialize the Database
python app.py

5. Train the Model
To train the SVM model using UpdatedResumeDataSet.csv:
python main.py

6. Run the Application
Start the Flask application:
python app.py

Access the app at 🌐 http://127.0.0.1:5000.

📝 Usage
User Features
👤 Signup/Login: Create an account or log in to upload resumes.
📤 Resume Upload: Upload a single or multiple resumes with a desired job role.
📊 Results: View suitability results or download a batch CSV report.
Admin Features
🔑 Admin Login: Use username: admin, password: admin12345.
🛠️ Dashboard: View, edit, and delete uploaded resumes.

📂 Directory Structure
Resume-Screening-App/
│
├── app.py                # Main Flask application
├── main.py               # Script for training the SVM model
├── templates/            # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── result.html
│   ├── batch_result.html
│   ├── admin_dashboard.html
│   └── edit_resume.html
├── static/               # Static assets
├── uploads/              # Uploaded resumes
├── svm_model.pkl         # Trained SVM model
├── tfidf_vectorizer.pkl  # Trained TF-IDF vectorizer
├── UpdatedResumeDataSet.csv  # Training dataset
├── requirements.txt      # Python dependencies
└── README.md             # Documentation

🔄 Application Workflow
👥 User Login/Signup: Users log in or sign up.
📄 Resume Upload: Users upload resumes in PDF format.
🛠️ Data Processing: The app extracts and preprocesses text, then predicts the job designation.
📊 Results Display: Suitability is calculated and shown.
📑 Batch Processing: Multiple uploads generate a consolidated report.
🛡️ Admin Features: Admin manages uploaded resumes via the dashboard.
📸 Screenshots

🏠 Home Page
![Upload resume here](https://github.com/user-attachments/assets/ebb8e404-00cc-4b81-bb60-0ce9ac348e2f)

📊 Result Page
![Individual Resume Parsing](https://github.com/user-attachments/assets/63244426-8fee-433d-a4d0-276f28bffd02)
![Batch Resume Parsing](https://github.com/user-attachments/assets/caa695ca-8405-4952-8680-0dfeb37760f9)

🛡️ Admin Dashboard
![Admin Dashboard](https://github.com/user-attachments/assets/5b4dd025-b429-4bd4-884a-262f103a88f5)

🤝 Contributing
💡 Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

This README should provide clear instructions and an overview of your project. Let me know if you need further refinements!
