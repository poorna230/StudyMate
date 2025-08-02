# StudyMate
# 📚 StudyMate: AI-Powered PDF-Based Q&A System

**StudyMate** is an AI-powered academic assistant that allows you to upload study materials (PDF, DOCX, TXT, CSV, JSON) and perform advanced operations like:
- ❓ **Ask Contextual Questions**
- 📝 **Generate Quizzes (MCQs)**
- 📊 **Summarize Documents**
- 📖 **Create Structured Study Notes**

Powered by **Google Gemini API (1.5-Flash)** and built using **Streamlit**.

---

## 🚀 Features
- **File Upload**: Upload PDF, DOCX, TXT, CSV, JSON files.
- **Ask Questions**: Context-aware Q&A based on uploaded material.
- **Quiz Generator**: Auto-generate Multiple Choice Questions (MCQs) with explanations.
- **Document Summarization**: AI-based concise summaries.
- **Study Notes Creator**: Auto-generated bullet-pointed study notes.
- **Downloadable Results**: Download quizzes, summaries, and notes.

---

## 🛠️ Tech Stack
- **Python 3.8+**
- **Streamlit**
- **Google Generative AI (Gemini API)**
- **PyMuPDF (fitz)**
- **python-docx**
- **pandas**
- **JSON handling**

---

## 📦 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/studymate-ai.git
   cd studymate-ai
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   conda create -n studymate python=3.8
   conda activate studymate
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App**:
   ```bash
   streamlit run app2.py
   ```

---

## 🔑 Google Gemini API Key Setup
1. Get a Gemini API Key from [Google AI Studio](https://makersuite.google.com/app/apikey).
2. Open `app2.py` and replace:
   ```python
   gemini_api_key = "YOUR_API_KEY_HERE"
   ```
3. Or, you can input it in the **Streamlit sidebar** when the app is running.

---

## 🖥️ Usage Guide
1. **Upload Study Material** (PDF/DOCX/TXT/CSV/JSON).
2. Click **Process File**.
3. Use tabs to:
   - **Ask Questions**
   - **Generate Quiz**
   - **Summarize**
   - **Create Study Notes**
4. Download results as **TXT/PDF files**.

---

## 🖌️ Custom UI Styling
The app uses custom CSS for an aesthetic dark-themed gradient layout with modern UI cards, buttons, and interactive upload zones.

---

## 📁 Folder Structure
```
├── app2.py                # Main Streamlit Application
├── requirements.txt        # Python Dependencies
└── README.md               # (This File)



