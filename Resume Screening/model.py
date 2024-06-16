import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import string
import re
import pdfplumber
import spacy
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity

# Download the stopwords from NLTK
nltk.download('stopwords')

# Initialize spaCy model
nlp = spacy.load('en_core_web_sm')

# Function to preprocess text
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower()  # Convert text to lowercase
    text = re.sub(f'[{string.punctuation}]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove digits
    text = ' '.join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Keep only alphabets  
    return text

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# Function to predict designation
def predict_designation(resume_text):
    # Preprocess the resume text
    preprocessed_text = preprocess_text(resume_text)

    # Transform the preprocessed text using the vectorizer
    text_vectorized = vectorizer.transform([preprocessed_text])

    # Predict the label using the trained model
    predicted_label = model.predict(text_vectorized)[0]

    return predicted_label

# Load data from CSV file
file_path = 'data.csv'
df = pd.read_csv(file_path)
print("Columns in the dataset:", df.columns)

# Assuming the CSV has columns 'Resume' and 'Category'
text_column = 'Resume'
label_column = 'Category'

df[text_column] = df[text_column].apply(preprocess_text)

# Convert text data to numeric data using CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df[text_column])

# Extract labels
y = df[label_column]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# Train a Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the model and vectorizer
joblib.dump(model, 'logistic_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

# Make predictions
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Function to extract information from resume text
def extract_info(text, job_role, job_description=None):
    # Remove bullets and other unexpected characters
    text = re.sub(r'[•➢]', '', text)
    
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    
    # Updated phone number regex pattern to handle country codes and various formats
    phone_pattern = re.compile(r'\+?\d{0,2}[\s-]?\d{0,2}[\s-]?\d{10}(?!\d)')
    phone_match = phone_pattern.search(text)
    phone = phone_match.group(0) if phone_match else None

    email = email.group(0) if email else None

    doc = nlp(text)
    
    # Define a set of common skills including Python frameworks
    common_skills = {'python', 'java', 'c++', 'sql', 'javascript', 'html', 'css', 'react', 'node.js', 'angular', 
                     'excel', 'powerpoint', 'word', 'c', 'github', 'dbms', 'problem-solving', 'leadership', 'teamwork', 
                     'time management','programming', 'adaptability', 'dsa', 'sdlc', 'oops', 'rdbms', 'typescript', 'swift', 'kotlin', 
                     'php', 'ruby', 'go', 'scala', 'perl', 'bash', 'linux', 'docker', 'kubernetes', 'aws', 'azure', 
                     'gcp', 'tensorflow', 'pytorch', 'machine learning', 'deep learning', 'data analysis', 'nlp', 'artificial intelligence',
                     # Adding popular Python frameworks
                     'django', 'flask', 'fastapi', 'pyramid', 'tornado', 'dash', 'bottle', 'falcon', 'web2py', 'cherrypy'}
    
    # Predict the designation
    predicted_designation = predict_designation(text)
    
    # Extract name and filter out any that match skill names
    name = next((ent.text for ent in doc.ents if ent.label_ == 'PERSON' and any(char.isalpha() or char.isspace() for char in ent.text)), None)

    # Extract skills - match tokens against the common skills set
    skills = set()
    for token in doc:
        token_text = token.text.lower()
        if token_text in common_skills:
            skills.add(token.text)
    
    # Convert skills set to sorted list
    skills = sorted(skills)

        # Determine suitability based on job role and predicted designation
    suitability = "Suitable" if job_role.strip().lower() == predicted_designation.strip().lower() else "Not Suitable"

    return {
        'Job Role': job_role,
        'Predicted Designation': predicted_designation,
        'Email': email,
        'Phone': phone,
        'Name': name,
        'Skills': skills,
        'Suitability for Job': suitability,
        # 'Similarity Score': similarity_score,
    }

# Example usage
# file_path = 'UpdatedResume2.pdf'
# job_role = "Software Engineer"
# job_description = "Looking for a data scientist proficient in Python, SQL, and machine learning."

# # Verify if the file exists
# if not os.path.exists(file_path):
#     print(f"Error: The file at path {file_path} does not exist.")
# else:
#     text = extract_text_from_pdf(file_path)
#     info = extract_info(text, job_role, job_description)
#     print(info)
