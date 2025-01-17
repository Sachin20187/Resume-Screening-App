import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import string
import re
import joblib
import pdfplumber
import os
import spacy

# Download NLTK stopwords and spaCy model
nltk.download('stopwords')

# Initialize spaCy model
nlp = spacy.load('en_core_web_sm')

vectorizer = joblib.load('tfidf_vectorizer.pkl')
svm_model = joblib.load('svm_model.pkl')

# Function to preprocess text
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = re.sub(f'[{string.punctuation}]', '', text)
    text = re.sub(r'\d+', '', text)
    text = ' '.join([word for word in text.split() if word not in stop_words])
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text or "No text found in the PDF."

# Function to predict the category of a resume
def predict_designation(resume_text, vectorizer, svm_model):
    preprocessed_text = preprocess_text(resume_text)
    text_vectorized = vectorizer.transform([preprocessed_text])
    predicted_label = svm_model.predict(text_vectorized)[0]
    return predicted_label


# Function to extract key details from a resume
def extract_info(resume_text, job_role, vectorizer, svm_model):

    # Extract name using spaCy's named entity recognition (NER)
    doc = nlp(resume_text)
    name = next((ent.text for ent in doc.ents if ent.label_ == 'PERSON' and any(char.isalpha() or char.isspace() for char in ent.text)), None)


    # Extract email
    email = re.search(r'[\w\.-]+@[\w\.-]+', resume_text)
    email = email.group(0) if email else None

    # Extract phone number
    phone_pattern = re.compile(r'\+?\d{0,2}[\s-]?\d{0,2}[\s-]?\d{10}(?!\d)')
    phone_match = phone_pattern.search(resume_text)
    phone = phone_match.group(0) if phone_match else None

    # Predict designation
    predicted_designation = predict_designation(resume_text, vectorizer, svm_model)

        
    # Update the name extraction logic
    # name = next((
    #     ent.text for ent in doc.ents 
    #     if ent.label_ == 'PERSON' 
    #     and all(char.isalpha() or char.isspace() for char in ent.text)  # Only alphabetic or spaces
    #     and ent.text.lower() not in common_skills  # Exclude common skills
    #     and not re.search(r'\d', ent.text)  # Exclude any name containing digits
    # ), None)

    # Extract skills
    common_skills = {'python', 'java', 'c++', 'sql', 'javascript', 'html', 'css', 'react', 'django', 'flask', 'aws', 'docker'}
    detected_skills = {skill for skill in common_skills if skill.lower() in resume_text.lower()}

    # Determine suitability
    suitability = "Suitable" if job_role.lower() == predicted_designation.lower() else "Not Suitable"

    return {
        'Name': name,
        'Email': email,
        'Phone': phone,
        'Job Role': job_role,
        'Predicted Designation': predicted_designation,
        'Skills': list(detected_skills),
        'Suitability': suitability
    }

# Main program
def main():
    # Load dataset
    file_path = 'UpdatedResumeDataSet.csv'
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return
    
    df = pd.read_csv(file_path)

    # Check for required columns
    if 'Resume' not in df.columns or 'Category' not in df.columns:
        print("Dataset must contain 'Resume' and 'Category' columns.")
        return

    # Preprocess the text data
    df['Resume'] = df['Resume'].apply(preprocess_text)

    # Define features and labels
    X = df['Resume']
    y = df['Category']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Use TfidfVectorizer to transform text data into numerical data
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Train a Support Vector Machine model
    svm_model = SVC(kernel='linear', probability=True, random_state=42)
    svm_model.fit(X_train_vectorized, y_train)

    # Save the trained model and vectorizer for future use
    joblib.dump(svm_model, 'svm_model.pkl')
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

    # Make predictions on the test set
    y_pred = svm_model.predict(X_test_vectorized)

    # Evaluate the model's performance
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy * 100:.2f}%')
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

# Dynamic PDF handling
    resume_file_path = input("Enter the PDF file path for resume extraction: ")
    job_role = input("Enter the job role you want to compare with: ")

    if not os.path.exists(resume_file_path):
        print(f"Error: File '{resume_file_path}' does not exist.")
    else:
        resume_text = extract_text_from_pdf(resume_file_path)
        if resume_text == "No text found in the PDF.":
            print(resume_text)
        else:
            # Load trained model and vectorizer
            vectorizer = joblib.load('tfidf_vectorizer.pkl')
            svm_model = joblib.load('svm_model.pkl')

            # Extract and print information
            info = extract_info(resume_text, job_role, vectorizer, svm_model)
            print(info)

# Run the program
if __name__ == "__main__":
    main()
