import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import docx
import pandas as pd
import tempfile
import os
import json

# Configure page
st.set_page_config(
    page_title="StudySupport",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


def apply_custom_css():
    """Apply custom CSS for StudySupport design"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 1rem;
    }
    
    .logo {
        width: 60px;
        height: 60px;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        color: white;
    }
    
    .app-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .upload-section {
        background: rgba(255, 255, 255, 0.08);
        border: 2px dashed rgba(0, 210, 255, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: rgba(0, 210, 255, 0.6);
        background: rgba(255, 255, 255, 0.12);
    }
    
    .upload-title {
        color: #00d2ff;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    .success-banner {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .action-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .action-card {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .action-card:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 210, 255, 0.2);
    }
    
    .action-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
    }
    
    .action-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .action-title {
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .action-desc {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }
    
    .interface-section {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .section-title {
        color: #00d2ff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .answer-box {
        background: rgba(0, 210, 255, 0.1);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
    }
    
    .quiz-question {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #00d2ff;
    }
    
    .model-selector {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom button styles */
    .stButton > button {
        background: linear-gradient(45deg, #00d2ff, #3a7bd5);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 210, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

class SimpleStudyAssistant:
    def __init__(self):
        self.file_content = ""
        self.chunks = []
    
    def extract_text_from_file(self, uploaded_file):
        """Extract text from file"""
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        try:
            if file_extension == 'pdf':
                return self._extract_pdf_text(uploaded_file)
            elif file_extension == 'docx':
                return self._extract_docx_text(uploaded_file)
            elif file_extension == 'txt':
                return uploaded_file.read().decode('utf-8')
            elif file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
                return df.to_string()
            elif file_extension == 'json':
                data = json.load(uploaded_file)
                return json.dumps(data, indent=2)
            else:
                return uploaded_file.read().decode('utf-8')
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return ""
    
    def _extract_pdf_text(self, pdf_file):
        """Extract text from PDF"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(pdf_file.read())
            tmp_path = tmp.name
        
        doc = fitz.open(tmp_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text() + "\n"
        doc.close()
        os.unlink(tmp_path)
        return full_text
    
    def _extract_docx_text(self, docx_file):
        """Extract text from DOCX"""
        doc = docx.Document(docx_file)
        full_text = ""
        for paragraph in doc.paragraphs:
            full_text += paragraph.text + "\n"
        return full_text
    
    def chunk_text(self, text, chunk_size=1000):
        """Split text into chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks

# 🔴 API USAGE LOCATION 1: GEMINI API SETUP
def setup_gemini_api(api_key):
    """Setup Gemini API - THIS IS WHERE GEMINI API IS CONFIGURED"""
    try:
        genai.configure(api_key=api_key)
        # Fixed model name - use gemini-1.5-flash instead of gemini-pro
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f" API Error: {e}")
        return None

# 🔴 API USAGE LOCATION 2: GEMINI API FOR QUESTIONS
def ask_gemini_question(model, question, context):
    """Ask question using Gemini API - THIS IS WHERE GEMINI API IS CALLED"""
    try:
        prompt = f"""
        Based on the following context, answer the question clearly and accurately.
        
        Context: {context[:3000]}  # Limit context to avoid token limits
        
        Question: {question}
        
        Please provide a detailed and helpful answer based on the context provided.
        """
        
        # 🔴 THIS IS THE ACTUAL GEMINI API CALL
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error with Gemini API: {e}"

# 🔴 API USAGE LOCATION 3: GEMINI API FOR QUIZ GENERATION
def generate_quiz_with_gemini(model, context, num_questions=3):
    """Generating quiz"""
    try:
        prompt = f"""
You are a quiz master. Generate  MCQ quiz based on the following content.

Context:
{context}

Create {num_questions} multiple-choice questions. Each question should have 4 options (A, B, C, D), indicate the correct answer, and include a one-line explanation.

Output format:
Q1. Question text
A. Option A
B. Option B
C. Option C
D. Option D
Answer: A/B/C/D
Explanation: One-line explanation
"""
        response = model.generate_content(prompt)
        return response.text.strip()

        # 🔴 THIS IS THE ACTUAL GEMINI API CALL FOR QUIZ
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating quiz:"

# 🔴 API USAGE LOCATION 4: GEMINI API FOR SUMMARY
def generate_summary_with_gemini(model, context):
    """Generate summary using Gemini API - THIS IS WHERE GEMINI CREATES SUMMARY"""
    try:
        prompt = f"""
        Please provide a comprehensive summary of the following document. 
        Include the main topics, key points, and important details.
        Make the summary clear and well-organized.
        
        Document content: {context[:4000]}
        """
        
        # 🔴 THIS IS THE ACTUAL GEMINI API CALL FOR SUMMARY
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

# 🔴 API USAGE LOCATION 5: GEMINI API FOR STUDY NOTES
def generate_study_notes_with_gemini(model, context):
    """Generate study notes using Gemini API"""
    try:
        prompt = f"""
        Create detailed study notes from the following content. 
        Organize the notes with:
        - Main topics and subtopics
        - Key concepts and definitions  
        - Important facts and figures
        - Use bullet points and clear structure
        
        Content: {context[:3500]}
        """
        
        # 🔴 THIS IS THE ACTUAL GEMINI API CALL FOR STUDY NOTES
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating study notes: {e}"

def main():
    apply_custom_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📚 StudyMate</h1>
        <p style="font-size: 1.2rem; margin: 0;">AI-Powered Academic Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize assistant
    if 'assistant' not in st.session_state:
        st.session_state.assistant = SimpleStudyAssistant()
    
    assistant = st.session_state.assistant
    
    # 🔴 API CONFIGURATION SECTION - PUT YOUR API KEY HERE OR IN SIDEBAR
    
    # 🔴🔴 OPTION 1: PUT YOUR API KEY DIRECTLY HERE (REPLACE "your_api_key_here")
    gemini_api_key = "AIzaSyC2fgrvl4m0R2VvAH-i6WNsrNwtpUWXpaA"  # ← PUT YOUR API KEY HERE
    
    # 🔴🔴 OPTION 2: OR USE SIDEBAR INPUT (COMMENT OUT OPTION 1 IF USING THIS)
    with st.sidebar:
        
        # 🔴🔴 OPTION 3: OR PUT YOUR KEY DIRECTLY HERE FOR TESTING
        # Uncomment the line below and add your key:
       # gemini_api_key = "AIzaSyC2fgrvl4m0R2VvAH-i6WNsrNwtpUWXpaA"  # ← PUT YOUR ACTUAL API KEY HERE

        # Show API status
        if gemini_api_key:
            st.success(" API Ready!")
            st.info("💡 You can now use all features")
        else:
            st.warning(" API key required")
        
        
    
    # File Upload
    st.markdown("""
    <div class="upload-section">
        <h3>📁 Upload Your Study Material</h3>
        <p>Supported formats: PDF, DOCX, TXT, CSV, JSON</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx', 'txt', 'csv', 'json'],
        help="Upload your study materials to get started"
    )
    
    if uploaded_file:
        # st.markdown(f"""
        # <div class="success-box">
        #     ✅ File uploaded: <strong>{uploaded_file.name}</strong> ({uploaded_file.size} bytes)
        # </div>
        # """, unsafe_allow_html=True)
        
        if st.button("🚀 Process File", type="primary"):
            with st.spinner("Processing file..."):
                # Extract text
                text_content = assistant.extract_text_from_file(uploaded_file)
                
                if text_content:
                    assistant.file_content = text_content
                    assistant.chunks = assistant.chunk_text(text_content)
                    st.session_state.file_processed = True
                    
                    st.success(f"✅ File processed successfully!")
                    # st.info(f"📄 Extracted {len(text_content)} characters in {len(assistant.chunks)} chunks")
                    
                    # Show preview
                    with st.expander("📖 Content Preview"):
                        preview_text = text_content[:800] + "..." if len(text_content) > 800 else text_content
                        st.text_area("Document Preview:", preview_text, height=200)
    
    # Main Features
    if st.session_state.get('file_processed', False):
        st.markdown("---")
        
        # Feature tabs
        tab1, tab2, tab3, tab4 = st.tabs(["💬 Ask Questions", "📝 Generate Quiz", "📊 Summarize", "📖 Study Notes"])
        
        with tab1:
            st.subheader("💬 Ask Questions About Your Document")
            
            # Sample questions
            st.markdown("**💡 Try these sample questions:**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("What is the main topic?"):
                    st.session_state.sample_question = "What is the main topic of this document?"
                if st.button("List key points"):
                    st.session_state.sample_question = "What are the key points covered in this document?"
            with col2:
                if st.button("Explain the concept"):
                    st.session_state.sample_question = "Can you explain the main concept in simple terms?"
                if st.button("What should I remember?"):
                    st.session_state.sample_question = "What are the most important things I should remember from this document?"
            
            question = st.text_input(
                "Enter your question:",
                value=st.session_state.get('sample_question', ''),
                help="Ask anything about your uploaded document"
            )
            
            if question and st.button("🔍 Get Answer", key="ask_btn"):
                if not gemini_api_key:
                    st.error("🔴 Please provide your  API key in the sidebar")
                else:
                    with st.spinner("🔴 Analyzing document with  AI..."):
                        # 🔴 HERE'S WHERE WE USE THE GEMINI API FOR QUESTIONS
                        gemini_model = setup_gemini_api(gemini_api_key)
                        if gemini_model:
                            answer = ask_gemini_question(
                                gemini_model, 
                                question, 
                                assistant.file_content
                            )
                            
                            st.markdown(f"""
                            <div class="answer-box">
                                <h4>🤖  AI Answer:</h4>
                                <p>{answer}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Clear sample question
                            if 'sample_question' in st.session_state:
                                del st.session_state.sample_question
        
        with tab2:
            st.subheader("📝 Generate Quiz Questions")
            
            col1, col2 = st.columns(2)
            with col1:
                num_questions = st.slider("Number of Questions:", 1, 10, 5)
            with col2:
                quiz_difficulty = st.selectbox("Difficulty Level:", ["Easy", "Medium", "Hard"])
            
            if st.button("📝 Generate Quiz", key="quiz_btn"):
                if not gemini_api_key:
                    st.error("🔴 Please provide your API key for quiz generation")
                else:
                    with st.spinner("🔴 Creating quiz questions ..."):
                        # 🔴 HERE'S WHERE WE USE GEMINI API FOR QUIZ GENERATION
                        gemini_model = setup_gemini_api(gemini_api_key)
                        if gemini_model:
                            quiz_content = generate_quiz_with_gemini(
                                gemini_model, 
                                assistant.file_content, 
                                num_questions
                            )
                            
                            st.markdown(f"""
                            <div class="answer-box">
                                <h4>📝 Generated Quiz ({quiz_difficulty} Level):</h4>
                                <pre style="white-space: pre-wrap; font-family: inherit;">{quiz_content}</pre>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Download option
                            st.download_button(
                                label="💾 Download Quiz",
                                data=quiz_content,
                                file_name=f"quiz_{uploaded_file.name}_{num_questions}q.pdf",
                                mime="text/plain"
                            )
        
        with tab3:
            st.subheader("📊 Document Summary")
            
            summary_type = st.radio(
                "Summary Type:",
                ["📋 General Summary", "🎯 Key Points Only", "📈 Detailed Analysis"],
                horizontal=True
            )
            
            if st.button("📊 Generate Summary", key="summary_btn"):
                if not gemini_api_key:
                    st.error("🔴 Please provide your  API key for summary generation")
                else:
                    with st.spinner("🔴 Creating summary ..."):
                        # 🔴 HERE'S WHERE WE USE GEMINI API FOR SUMMARY
                        gemini_model = setup_gemini_api(gemini_api_key)
                        if gemini_model:
                            summary = generate_summary_with_gemini(
                                gemini_model,
                                assistant.file_content
                            )
                            
                            st.markdown(f"""
                            <div class="answer-box">
                                <h4>📊 Document Summary ({summary_type}):</h4>
                                <p>{summary}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Download option
                            st.download_button(
                                label="💾 Download Summary",
                                data=summary,
                                file_name=f"summary_{uploaded_file.name}.txt",
                                mime="text/plain"
                            )
        
        with tab4:
            st.subheader("📖 Generate Study Notes")
            
            note_style = st.selectbox(
                "Note Style:",
                ["📝 Bullet Points", "📚 Structured Outline", "🎓 Study Guide Format"]
            )
            
            if st.button("📖 Generate Study Notes", key="notes_btn"):
                if not gemini_api_key:
                    st.error("🔴 Please provide your API key for study notes generation")
                else:
                    with st.spinner("🔴 Creating study notes ..."):
                        # 🔴 HERE'S WHERE WE USE GEMINI API FOR STUDY NOTES
                        gemini_model = setup_gemini_api(gemini_api_key)
                        if gemini_model:
                            study_notes = generate_study_notes_with_gemini(
                                gemini_model,
                                assistant.file_content
                            )
                            
                            st.markdown(f"""
                            <div class="answer-box">
                                <h4>📖 Study Notes ({note_style}):</h4>
                                <div style="white-space: pre-wrap;">{study_notes}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Download option
                            st.download_button(
                                label="💾 Download Study Notes",
                                data=study_notes,
                                file_name=f"study_notes_{uploaded_file.name}.txt",
                                mime="text/plain"
                            )
    
    else:
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0; color: #64748b;">
            <h3>👆 Upload a file to get started</h3>
            <p>Upload your study materials and unlock AI-powered learning features!</p>
            <div style="margin: 2rem 0;">
                <h4>🚀 Features Available:</h4>
                <p>✅ Question Answering • ✅ Quiz Generation • ✅ Document Summarization • ✅ Study Notes</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()