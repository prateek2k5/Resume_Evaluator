# 🤖 AI Resume Evaluator using Groq LLM

An AI-powered ATS Resume Screening System built using **Python, Streamlit, and Groq LLM** that intelligently analyzes job descriptions and resumes, ranks candidates, and provides recruiter-friendly hiring recommendations.

## 🌐 Live Demo

https://resumeevaluator-ff35egbk8egahvkrmpjfqo.streamlit.app/

---

## 📌 Overview

AI Resume Evaluator is a web-based application that automates the resume screening process using Large Language Models (LLMs). Instead of relying on simple keyword matching, the application understands the context of both the Job Description and Candidate Resume to perform intelligent candidate evaluation.

The system extracts structured information from uploaded resumes and job descriptions, compares skills, experience, education, and projects, calculates an ATS-style match score, and ranks candidates based on their suitability for the job role.

---

## ✨ Features

- Upload Job Description in PDF, DOCX, or TXT format
- Upload and evaluate multiple resumes simultaneously
- AI-powered Job Description Parsing
- AI-powered Resume Parsing
- ATS-style Resume Evaluation
- Candidate Match Score Calculation
- Matching Skills Detection
- Missing Skills Analysis
- Experience Verification
- Automatic Candidate Ranking
- Interactive Dashboard
- Download Evaluation Results as CSV

---

## 🛠️ Tech Stack

**Frontend**
- Streamlit

**Backend**
- Python

**AI Model**
- Groq API
- Llama 3.3 70B Versatile

**Libraries**
- Groq
- Streamlit
- Pandas
- Plotly
- Pydantic
- PyPDF
- Python-docx
- Python-dotenv

---

## 📂 Project Structure

```text
Resume_Evaluator/
│
├── app.py
├── Resume_Evaluator.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/prateek2k5/Resume_Evaluator.git
```

Navigate to the project directory

```bash
cd Resume_Evaluator
```

Install the required dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file and add your Groq API Key.

```env
GROQ_API_KEY=your_groq_api_key
```

For Streamlit Cloud deployment, add the following secret:

```toml
GROQ_API_KEY="your_groq_api_key"
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 📖 How It Works

1. Upload a Job Description.
2. Upload one or more candidate resumes.
3. The application extracts structured information from the Job Description using Groq LLM.
4. Each resume is parsed to identify candidate details, skills, education, experience, certifications, and projects.
5. The AI compares resume information with the job requirements.
6. A match score is generated along with matching skills, missing skills, experience evaluation, and hiring recommendation.
7. All candidates are ranked based on their scores.
8. Users can download the final evaluation report in CSV format.

---

## 📊 Output

The application provides the following information for every candidate:

- Candidate Name
- Resume Match Score
- Matching Skills
- Missing Skills
- Experience Status
- Final Hiring Recommendation
- Ranked Candidate List

---

## 🚀 Future Improvements

- Resume Improvement Suggestions
- AI Interview Question Generator
- Authentication System
- Resume History
- PDF Report Generation
- Email Report Sharing
- Multi-language Resume Support

---

## 👨‍💻 Author

**Prateek Kumar**

GitHub: https://github.com/prateek2k5

---

## 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project helpful, consider giving it a star on GitHub.
