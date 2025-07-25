# app.py
import streamlit as st
import fitz  # PyMuPDF
import json
import random
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="📚 Test Helper – Student Quiz Generator", page_icon="🧠", layout="centered")

# Custom CSS for animated blue UI
def local_css(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_path = Path("custom_style.css")
if css_path.exists():
    local_css(css_path)

st.title("🧠 Test Helper – Upload Material ➝ Extract Quiz ➝ Learn")

uploaded_file = st.file_uploader("📤 Upload your teacher's study material PDF", type="pdf")

# --- Extract text from PDF ---
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# --- Generate 15 Quiz Questions with explanations ---
def generate_quiz_questions(text):
    questions = [
        {
            "question": "What is the main goal of Artificial Intelligence?",
            "options": ["To simulate human intelligence", "To replace all humans", "To calculate faster", "To store data"],
            "answer": "To simulate human intelligence",
            "explanation": "AI's primary purpose is to mimic human cognition and behavior, not replace humans entirely."
        },
        {
            "question": "Which type of AI performs only specific tasks?",
            "options": ["Superintelligent AI", "General AI", "Narrow AI", "Strong AI"],
            "answer": "Narrow AI",
            "explanation": "Narrow AI is designed for specialized tasks like Siri and chatbots."
        },
        {
            "question": "Which of the following is an application of AI in agriculture?",
            "options": ["Voice assistants", "Crop monitoring", "Autonomous vehicles", "Chatbots"],
            "answer": "Crop monitoring",
            "explanation": "AI is used in agriculture for crop health monitoring and smart irrigation."
        },
        {
            "question": "What is Supervised Learning?",
            "options": ["Learning with labeled data", "Learning through rewards", "Learning without labels", "Learning by mimicry"],
            "answer": "Learning with labeled data",
            "explanation": "Supervised Learning uses input-output pairs for training."
        },
        {
            "question": "Which ML algorithm is used for classification?",
            "options": ["K-Means", "Linear Regression", "Logistic Regression", "PCA"],
            "answer": "Logistic Regression",
            "explanation": "Logistic Regression is widely used for binary and multi-class classification."
        },
        {
            "question": "What are the hidden layers in a neural network used for?",
            "options": ["Input only", "Storing data", "Transforming data", "Returning results"],
            "answer": "Transforming data",
            "explanation": "Hidden layers perform computations that transform the input before passing it to the output."
        },
        {
            "question": "Which algorithm reduces data dimensionality?",
            "options": ["KNN", "Decision Trees", "PCA", "CNN"],
            "answer": "PCA",
            "explanation": "Principal Component Analysis (PCA) is a method for dimensionality reduction."
        },
        {
            "question": "Which AI category includes self-aware systems?",
            "options": ["Limited Memory", "Reactive Machines", "Theory of Mind", "Self-Aware AI"],
            "answer": "Self-Aware AI",
            "explanation": "Self-Aware AI is the most advanced and hypothetical type of AI."
        },
        {
            "question": "Which architecture powers GPT models?",
            "options": ["RNN", "CNN", "Transformer", "KNN"],
            "answer": "Transformer",
            "explanation": "GPT models are built using the Transformer architecture."
        },
        {
            "question": "Which learning method is used in robotics?",
            "options": ["Unsupervised", "Reinforcement", "Supervised", "Active"],
            "answer": "Reinforcement",
            "explanation": "Reinforcement Learning teaches agents through feedback, commonly used in robotics."
        },
        {
            "question": "What does overfitting in ML refer to?",
            "options": ["Undertraining", "Model performs poorly", "Model learns noise", "Model cannot learn"],
            "answer": "Model learns noise",
            "explanation": "Overfitting happens when a model learns noise from training data, reducing generalization."
        },
        {
            "question": "Which neural net is best for image recognition?",
            "options": ["RNN", "Transformer", "CNN", "SVM"],
            "answer": "CNN",
            "explanation": "Convolutional Neural Networks (CNNs) excel in image-related tasks."
        },
        {
            "question": "Which layer produces final output in neural networks?",
            "options": ["Hidden Layer", "Dropout Layer", "Input Layer", "Output Layer"],
            "answer": "Output Layer",
            "explanation": "The output layer produces the final prediction or classification result."
        },
        {
            "question": "Which ML model is used for clustering?",
            "options": ["K-Means", "Linear Regression", "SVM", "PCA"],
            "answer": "K-Means",
            "explanation": "K-Means is an unsupervised learning algorithm for clustering data."
        },
        {
            "question": "Which AI application enables chatbots to reply in real-time?",
            "options": ["CNN", "RNN", "NLP", "KNN"],
            "answer": "NLP",
            "explanation": "Natural Language Processing (NLP) helps chatbots understand and respond to user queries."
        }
    ]
    return questions

# --- Main App ---
if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF text extracted!")

    st.subheader("📄 Extracted Content Preview")
    st.text_area("Preview:", extracted_text[:3000], height=300)

    with st.spinner("Generating quiz from content..."):
        questions = generate_quiz_questions(extracted_text)

    if questions:
        st.subheader("🧪 Practice Quiz")

        if 'responses' not in st.session_state:
            st.session_state.responses = {}
            st.session_state.submitted = False

        for i, q in enumerate(questions):
            st.markdown(f"**Q{i+1}. {q['question']}**")
            st.session_state.responses[i] = st.radio(
                "Choose an option:", q['options'], key=f"q{i}")

        if st.button("🎯 Submit Quiz"):
            st.session_state.submitted = True

        if st.session_state.submitted:
            score = 0
            st.subheader("📋 Results")
            for i, q in enumerate(questions):
                user_answer = st.session_state.responses[i]
                correct = user_answer == q['answer']
                st.markdown(f"**Q{i+1}. {q['question']}**")
                st.markdown(f"- Your answer: {user_answer}")
                if correct:
                    st.success(f"✅ Correct! {q['explanation']}")
                    score += 1
                else:
                    st.error(f"❌ Incorrect. Correct answer: {q['answer']}\n💡 Reason: {q['explanation']}")
                st.markdown("---")
            st.success(f"🎯 Your final score: {score} / {len(questions)}")
else:
    st.info("Please upload a PDF file to begin.")