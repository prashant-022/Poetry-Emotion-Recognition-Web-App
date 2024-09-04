import streamlit as st
import joblib
import numpy as np
import matplotlib.pyplot as plt

# Load the trained SVM model and TF-IDF vectorizer
svm_model = joblib.load('svm_model_tfidf.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Define the emotion labels
emotion_labels = ['anger', 'courage', 'fear', 'hate', 'joy', 'love', 'peace', 'sad', 'surprise']

# Function to predict emotion and get probabilities
def predict_emotion(text):
    text_tfidf = tfidf_vectorizer.transform([text]).toarray()
    probabilities = svm_model.decision_function(text_tfidf)
    sorted_indices = np.argsort(probabilities[0])[::-1]
    top_3_indices = sorted_indices[:3]
    return probabilities[0], top_3_indices

# Streamlit app title and input
st.title('Poetry Emotion Recognition')
user_input = st.text_area('Enter a poem to analyze its emotion:')

if st.button('Predict'):
    if user_input:
        # Get prediction and probabilities
        probabilities, top_3_indices = predict_emotion(user_input)
        
        # Display top 3 predicted labels
        st.write("### Top 3 Predicted Emotions:")
        for idx in top_3_indices:
            st.write(f"{emotion_labels[idx]}: {probabilities[idx]:.2f}")
        
        # Plotting the probabilities for all labels
        st.write("### Emotion Probabilities:")
        plt.figure(figsize=(8, 4))
        plt.barh(emotion_labels, probabilities, color='skyblue')
        plt.xlabel('Probability')
        plt.ylabel('Emotion')
        plt.title('Emotion Prediction Probabilities')
        st.pyplot(plt)
    else:
        st.write('Please enter a poem.')
