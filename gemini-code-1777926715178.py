import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. UI DESIGN & THEME ---
st.set_page_config(page_title="EduWave AI", page_icon="🌊", layout="centered")

st.markdown("""
    <style>
    /* Dark Mode Background */
    .stApp { background-color: #121212; color: #FFFFFF; }
    
    /* Vibrant Green Buttons */
    .stButton>button { 
        background-color: #A3E635 !important; 
        color: #000000 !important; 
        border-radius: 12px; 
        font-weight: 800;
        width: 100%;
        border: none;
        padding: 10px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #84CC16 !important;
        transform: scale(1.02);
    }
    
    /* Rounded Cards for Output */
    div[data-testid="stExpander"] {
        background-color: #1E1E1E;
        border-radius: 15px;
        border: 1px solid #333333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER ---
st.title("🌊 EduWave")
st.subheader("Let's Learn New Stuff!")
st.write("Upload your textbook chapter, and I'll generate a crash course.")

# --- 3. SECURE AI SETUP ---
# In production, we use 'secrets' so your key isn't stolen.
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    st.warning("⚠️ API Key missing! Please add it to Streamlit Secrets.")
    st.stop()

# --- 4. THE ENGINE ---
uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"])

if uploaded_file:
    with st.spinner("🧠 Reading your book and generating magic..."):
        try:
            # Safely extract text
            reader = PdfReader(uploaded_file)
            full_text = ""
            # Only read the first 15 pages to keep it fast for mobile
            for page in reader.pages[:15]: 
                text = page.extract_text()
                if text:
                    full_text += text
            
            # The AI Prompt
            prompt = f"""
            You are an expert tutor. Analyze the following text and provide:
            1. **Key Concepts:** 3-5 bullet points summarizing the core ideas.
            2. **High-Yield Exam:** 3 multiple-choice questions with the correct answers bolded.
            
            Text to analyze: {full_text[:12000]} 
            """
            
            response = model.generate_content(prompt)
            
            # --- 5. DISPLAY RESULTS ---
            st.success("✅ Analysis Complete!")
            
            with st.expander("📖 View Your Crash Course", expanded=True):
                st.markdown(response.text)
                
            if st.button("Generate More Puzzles"):
                st.info("Feature coming soon: Flashcards and Match-the-Term!")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")