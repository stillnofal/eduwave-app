# --- 3. SECURE AI SETUP ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Use 'gemini-1.5-flash' - this is the most current stable name
    model = genai.GenerativeModel('gemini-1.5-flash')
    
except Exception: # Missing the 'as e' part!
    st.error(f"Setup Error: {e}")
    st.stop()
# --- 4. THE ENGINE ---
uploaded_file = st.file_uploader("Drop your PDF here", type=["pdf"])

if uploaded_file:
    with st.spinner("🧠 Analyzing your material..."):
        try:
            reader = PdfReader(uploaded_file)
            full_text = ""
            for page in reader.pages[:10]: 
                full_text += page.extract_text() or ""
            
            # This is the part from your screenshot!
            prompt = f"""
            You are an expert tutor. Analyze the following text and provide:
            1. **Key Concepts:** 3-5 bullet points summarizing the core ideas.
            2. **High-Yield Exam:** 3 multiple-choice questions with the correct answers bolded.
            
            Text: {full_text[:15000]}
            """
            
            # Using a more robust generation call
            response = model.generate_content(prompt)
            
            st.success("✅ Analysis Complete!")
            with st.expander("📖 View Your Crash Course", expanded=True):
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")
