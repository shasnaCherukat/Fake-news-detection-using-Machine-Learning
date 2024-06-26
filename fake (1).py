import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# Read the datasets
train = pd.read_csv(r"C:\Users\rohan\Downloads\mini\train.csv")
test = pd.read_csv(r"C:\Users\rohan\Downloads\mini\test.csv")

# Shuffle the dataset
shuftr = train.sample(frac=1).reset_index(drop=True)
shufte = test.sample(frac=1).reset_index(drop=True)

# Text preprocessing function
def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

# Apply text preprocessing
train["text"] = train["text"].apply(wordopt)
test["text"] = test["text"].apply(wordopt)

# Define dependent and independent variables
x_train = train["text"]
x_train_class = train["label"]
x_test = test['text']
x_test_class = test["label"]

# Vectorize the text data with n-grams
vectorizer = TfidfVectorizer(ngram_range=(1, 2))  # Using bigrams
vectx = vectorizer.fit_transform(x_train)
vectxt = vectorizer.transform(x_test)

# Initialize Passive Aggressive Classifier
pac = PassiveAggressiveClassifier(max_iter=20)

try:
    pac = joblib.load('improved1.pkl')
    print("Model loaded successfully!")
except FileNotFoundError:
    # Train the voting classifier
    pac.fit(vectx, x_train_class)
    # Save the trained model
    joblib.dump(pac, 'save3.pkl')
    print("Model trained and saved successfully!")

# Make predictions
predictions = pac.predict(vectxt)

# Evaluate the model
print("Passive Aggressive classifier performance:")
print(classification_report(x_test_class, predictions))
conf_matrix = confusion_matrix(x_test_class, predictions)

# Plot confusion matrix as heatmap
'''
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()'''
'''
# Identify misclassified samples
misclassified_indices = (predictions == 0) & (x_test_class == 1)
misclassified_samples = x_test[misclassified_indices]

# Augment training data by adding misclassified samples with correct labels
augmented_train = pd.concat([train, pd.DataFrame({"text": misclassified_samples, "label": np.ones(len(misclassified_samples))})])

# Apply text preprocessing to the augmented training data
augmented_train["text"] = augmented_train["text"].apply(wordopt)

# Define dependent and independent variables for augmented training data
x_augmented_train = augmented_train["text"]
x_augmented_train_class = augmented_train["label"]

# Vectorize the text data with n-grams for augmented training data
vect_augmented_train = vectorizer.transform(x_augmented_train)

# Retrain the model using augmented training data
pac.fit(vect_augmented_train, x_augmented_train_class)

# Make predictions
predictions = pac.predict(vectxt)
joblib.dump(pac, 'improved1.pkl')
print("Improved model is saved")

# Evaluate the model
print("Updated Passive Aggressive classifier performance:")
print(classification_report(x_test_class, predictions))
'''
def fetch_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract article text based on the HTML structure of the website
    article_text = ""
    for paragraph in soup.find_all('p'):
        article_text += paragraph.get_text() + " "
    return article_text
    
def url_enter(url):
    parsed_url = urlparse(url)
    
    # Extract the netloc which contains the domain name
    domain = parsed_url.netloc
    
    # Remove www. if present
    domain = domain.replace("www.", "")
    
    # Split the domain to extract just the source name
    source_name_parts = domain.split('.')
    
    # Check for specific cases and handle them
    
    source_name = source_name_parts[0]
    if source_name in ["bbc", "edition", "nbcnews", "cbsnews", "npr", "apnews", "reuters", "pbs", "theguardian", "nytimes", "timesofindia", "thehindu","hindustantimes", "indianexpress", "ndtv", "wsj", "washingtonpost", "economist", "newyorker", "bloomberg", "theatlantic","deccanchronicle"]:
        return "True news(credible source)"
    else:
        news=fetch_article_text(url)
        print(news)
        r=manual_testing(news)
        return r 



# Function for manual testing
def manual_testing(news):
    news = wordopt(news)
    # Vectorize the testing news
    new_x_test = vectorizer.transform([news])
    # Predict using the model
    prediction = pac.predict(new_x_test)
    if prediction[0] == 0:
        print("fake")
        return "fake news"
    else:
        print("true")
        return "true news"
