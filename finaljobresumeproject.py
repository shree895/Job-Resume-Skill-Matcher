# ----------------------------------------------------------
# JOB–RESUME SKILL MATCHER (Professional GUI Version)
# Using Python, Tkinter, NLTK, Pandas, NumPy, Scikit-learn
# ----------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, messagebox, Text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np 
import nltk
from nltk.corpus import stopwords
import re
import PyPDF2

# Download stopwords if not already downloaded
nltk.download('stopwords')

# -----------------------------------------------------------
# Text Extraction and Cleaning
# -----------------------------------------------------------
def extract_text(file_path):
    text = ""
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    return text

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
    return text

# -----------------------------------------------------------
# Skill Extraction
# -----------------------------------------------------------
predefined_skills = [
    'python', 'java', 'c++', 'sql', 'excel', 'data analysis', 'machine learning',
    'communication', 'leadership', 'project management', 'html', 'css', 'javascript',
    'nlp', 'deep learning', 'pandas', 'numpy', 'teamwork', 'critical thinking'
]

def extract_skills(text):
    found = []
    for skill in predefined_skills:
        if skill.lower() in text.lower():
            found.append(skill)
    return found

# -----------------------------------------------------------
# Matching Algorithm
# -----------------------------------------------------------
def calculate_similarity(resume_text, job_text):
    corpus = [resume_text, job_text]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(similarity * 100, 2)

# -----------------------------------------------------------
# Recommended Skills
# -----------------------------------------------------------
def recommend_skills(resume_skills, job_skills):
    missing = [skill for skill in job_skills if skill not in resume_skills]
    return missing if missing else ["Your resume already covers all key skills."]

# -----------------------------------------------------------
# GUI Functions
# -----------------------------------------------------------
def upload_resume():
    global resume_path
    resume_path = filedialog.askopenfilename(filetypes=[("PDF or TXT Files", "*.pdf *.txt")])
    if resume_path:
        resume_label.config(text=f"Resume: {resume_path.split('/')[-1]}")

def upload_job():
    global job_path
    job_path = filedialog.askopenfilename(filetypes=[("PDF or TXT Files", "*.pdf *.txt")])
    if job_path:
        job_label.config(text=f"Job Description: {job_path.split('/')[-1]}")

def match_skills():
    try:
        resume_text = clean_text(extract_text(resume_path))
        job_text = clean_text(extract_text(job_path))

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_text)

        similarity = calculate_similarity(resume_text, job_text)
        missing = recommend_skills(resume_skills, job_skills)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Resume–Job Match Score: {similarity}%\n\n")
        result_text.insert(tk.END, f"Skills in Resume: {', '.join(resume_skills) if resume_skills else 'None found'}\n\n")
        result_text.insert(tk.END, f"Skills Required for Job: {', '.join(job_skills) if job_skills else 'None found'}\n\n")
        result_text.insert(tk.END, f"Recommended Skills to Add: {', '.join(missing)}\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# -----------------------------------------------------------
# GUI Design (Professional Theme)
# -----------------------------------------------------------
root = tk.Tk()
root.title("Job–Resume Skill Matcher")
root.geometry("800x620")
root.config(bg="#E8EEF1")

# Title Section
title_label = tk.Label(root, text="Job–Resume Skill Matcher", 
                       font=("Segoe UI", 20, "bold"), bg="#2C3E50", fg="white", padx=10, pady=10)
title_label.pack(fill="x")

subtitle_label = tk.Label(root, text="AI-based Resume Analyzer using NLP & Machine Learning",
                          font=("Segoe UI", 12), bg="#E8EEF1", fg="#333333")
subtitle_label.pack(pady=10)

# Upload Section
frame = tk.Frame(root, bg="#E8EEF1")
frame.pack(pady=10)

resume_btn = tk.Button(frame, text="Upload Resume", font=("Segoe UI", 11, "bold"), bg="#2980B9", fg="white",
                       width=20, command=upload_resume, relief="flat", padx=5, pady=5)
resume_btn.grid(row=0, column=0, padx=10, pady=5)

resume_label = tk.Label(frame, text="No Resume Uploaded", bg="#E8EEF1", fg="#555")
resume_label.grid(row=0, column=1)

job_btn = tk.Button(frame, text="Upload Job Description", font=("Segoe UI", 11, "bold"), bg="#27AE60", fg="white",
                    width=20, command=upload_job, relief="flat", padx=5, pady=5)
job_btn.grid(row=1, column=0, padx=10, pady=5)

job_label = tk.Label(frame, text="No Job Description Uploaded", bg="#E8EEF1", fg="#555")
job_label.grid(row=1, column=1)

# Match Button
match_btn = tk.Button(root, text="Run Skill Match Analysis", font=("Segoe UI", 12, "bold"), 
                      bg="#34495E", fg="white", width=30, command=match_skills, relief="flat", pady=5)
match_btn.pack(pady=15)

# Results Display
result_text = Text(root, height=15, width=90, bg="#F8F9F9", fg="#222", wrap="word", font=("Consolas", 11))
result_text.pack(padx=15, pady=10)

# Footer
footer_label = tk.Label(root, text="Developed by Shree Sinha | Powered by Python, NLTK, Pandas, NumPy, Scikit-learn",
                        bg="#2C3E50", fg="white", font=("Segoe UI", 10), pady=6)
footer_label.pack(fill="x", side="bottom")

root.mainloop()
