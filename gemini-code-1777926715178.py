import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. UI DESIGN ---
st.set_page_config(page_title="EduWave", page_icon="🌊")
st.title("🌊 EduWave")
st.subheader("Let's Learn New Stuff!")

# --- 2. SECURE AI SETUP ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Setup Error: {e}")
    st.stop()

# --- 3. THE ENGINE ---
uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"])

if uploaded_file:
    with st.spinner("🧠 Analyzing your material..."):
        try:
            # Step A: Read PDF
            reader = PdfReader(uploaded_file)
            full_text = ""
            for page in reader.pages[:10]: 
                full_text += page.extract_text() or ""
            
            # Step B: Create Prompt
            prompt = f"""
            You are an expert tutor. Analyze the following text and provide:
            1. **Key Concepts:** 3-5 bullet points summarizing the core ideas.
            2. **High-Yield Exam:** 3 multiple-choice questions with the correct answers bolded.
            
            Text: {full_text[:15000]}
            """
            
            # Step C: Generate AI Response
            response = model.generate_content(prompt)
            
            # Step D: Display Results
            st.success("✅ Analysis Complete!")
            with st.expander("📖 View Your Crash Course", expanded=True):
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Error during analysis: {e}")
