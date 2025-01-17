import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Step 1: Load the Dataset
data = pd.read_csv("UpdatedResumeDataSet.csv")  # Replace with your dataset file
print("Dataset loaded!")

# Step 2: Preprocess the Text
def preprocess_text(text):
    import re
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer

    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and special characters
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    text = ' '.join(word for word in text.split() if word not in stop_words)
    # Stemming
    ps = PorterStemmer()
    text = ' '.join(ps.stem(word) for word in text.split())
    return text

# Create the 'Resume_Text' column by combining 'Experience' and 'Skills'
# data['Resume_Text'] = data['Experience'] + " " + data['Skills']

# Assuming 'data' contains 'Category' and 'Resume' columns
data['Resume_Text'] = data['Resume']  # Use 'Resume' directly as the text data

# Check if the 'Resume_Text' column is created correctly
print(data['Resume_Text'].head())

data['Resume_Text'] = data['Resume_Text'].apply(preprocess_text)
print("Text preprocessing completed!")

# Step 3: Convert Text to Numerical Features
vectorizer = TfidfVectorizer(max_features=5000)  # Use top 5000 features
X = vectorizer.fit_transform(data['Resume_Text'])
y = data['Category']

# Step 4: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split into training and testing sets!")

# Step 5: Train the SVM Model
svm_model = SVC(kernel='linear', probability=True, random_state=42)
svm_model.fit(X_train, y_train)
print("Model training completed!")

# Step 6: Evaluate the Model
y_pred = svm_model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Step 7: Save the Model and Vectorizer
joblib.dump(svm_model, "svm_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model and vectorizer saved!")
