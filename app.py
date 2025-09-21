import streamlit as st
import pandas as pd

# ---- Page Config ----
st.set_page_config(page_title="InternMatch: Smart Internship Recommender", page_icon="🎯", layout="centered")

# ---- Sample Internship Data ----
internships = [
    {"title": "💻 Web Development Intern", "sector": "IT", "skills": "Programming", "location": "Delhi"},
    {"title": "🏥 Healthcare Assistant Intern", "sector": "Healthcare", "skills": "Data Entry", "location": "Mumbai"},
    {"title": "📚 Teaching Volunteer Intern", "sector": "NGO", "skills": "Teaching", "location": "Rural/Local"},
    {"title": "🌱 Agriculture Data Intern", "sector": "Agriculture", "skills": "Programming", "location": "Bangalore"},
    {"title": "🎨 Graphic Design Intern", "sector": "IT", "skills": "Design", "location": "Mumbai"},
]
df = pd.DataFrame(internships)

# ---- Session State ----
if "page" not in st.session_state:
    st.session_state.page = "choice"
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# ---- CSS ----
st.markdown("""
    <style>
    .title { text-align: center; font-size: 32px !important; color: #2C3E50; font-weight: bold; margin-bottom: 5px;}
    .subtitle { text-align: center; font-size: 18px !important; color: #7F8C8D; margin-bottom:20px;}
    .card { 
        background: black; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 3px 3px 15px rgba(0,0,0,0.15); 
        margin-bottom: 20px; 
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .card:hover { 
        transform: scale(1.03); 
        box-shadow: 5px 5px 25px rgba(0,0,0,0.2); 
        border-left: 5px solid #2980B9;
    }
    .card h4 { color: #2980B9; margin-bottom: 10px; font-size: 22px;}
    .reason { font-style: italic; color: #27AE60; }
    </style>
""", unsafe_allow_html=True)

# ---- Page Functions ----
def page_choice():
    st.markdown('<p class="title">🎯 InternMatch: Smart Internship Recommender</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Choose an option to continue</p>', unsafe_allow_html=True)
    choice = st.radio("Select an option:", ["📄 Upload Resume", "✍️ Fill Manual Form"])
    if st.button("Next"):
        st.session_state.form_data["choice"] = choice
        if choice == "✍️ Fill Manual Form":
            st.session_state.page = "manual_form"
        else:
            st.session_state.page = "resume_upload"

def page_manual_form():
    st.markdown('<p class="title">✍️ Enter Your Details</p>', unsafe_allow_html=True)
    st.write("---")
    
    name = st.text_input("Full Name")
    location = st.selectbox("Location", ["Delhi", "Mumbai", "Bangalore", "Rural/Local"])
    education = st.selectbox("Education", ["Diploma", "Undergraduate", "Postgraduate"])
    experience = st.selectbox("Experience (in years)", ["0-1", "1-2", "2-3", "3+"])
    skills = st.selectbox("Skills", ["Programming", "Teaching", "Data Entry", "Design", "Management"])
    interest = st.selectbox("Area of Interest", ["IT", "Healthcare", "NGO", "Agriculture", "Design"])
    
    if st.button("Submit"):
        st.session_state.form_data.update({
            "name": name,
            "location": location,
            "education": education,
            "experience": experience,
            "skills": skills,
            "interest": interest
        })
        st.session_state.page = "results"

def page_resume_upload():
    st.markdown('<p class="title">📄 Upload Your Resume</p>', unsafe_allow_html=True)
    st.write("---")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        st.success(f"✅ Resume '{uploaded_file.name}' uploaded successfully!")
        if st.button("Submit"):
            st.session_state.form_data["uploaded_file"] = uploaded_file
            st.session_state.page = "results"

def page_results():
    st.markdown('<p class="title">🔎 Recommended Internships</p>', unsafe_allow_html=True)
    st.write("---")
    
    form_data = st.session_state.form_data
    choice = form_data.get("choice")
    df_copy = df.copy()

    if choice == "✍️ Fill Manual Form":
        skills = form_data.get("skills")
        interest = form_data.get("interest")
        location = form_data.get("location")

        def match_score(row):
            score = 0
            reasons = []
            if row["skills"] == skills:
                score += 1
                reasons.append("Skill match")
            if row["sector"] == interest:
                score += 1
                reasons.append("Sector match")
            if row["location"] == location:
                score += 1
                reasons.append("Location match")
            return pd.Series([score, ", ".join(reasons)])
        
        df_copy[["score", "reason"]] = df_copy.apply(match_score, axis=1)
        matches = df_copy.sort_values(by="score", ascending=False).head(3)

        if matches["score"].sum() == 0:
            matches["reason"] = "Closest match"
        else:
            matches = matches[matches["score"] > 0]
    else:
        matches = df_copy.sample(3)
        matches["reason"] = "Resume based recommendation"

    if not matches.empty:
        for _, row in matches.iterrows():
            st.markdown(f"""
                <div class="card">
                    <h4>{row['title']}</h4>
                    <b>🏢 Sector:</b> {row['sector']} <br>
                    <b>🛠 Skills:</b> {row['skills']} <br>
                    <b>📍 Location:</b> {row['location']} <br>
                    <b>🎓 Education:</b> {form_data.get("education","-")} <br>
                    <b>⏱ Experience:</b> {form_data.get("experience","-")} <br>
                    <span class="reason">✅ Why Recommended: {row['reason']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No matching internships found.")

    if st.button("⬅️ Back to Start"):
        st.session_state.page = "choice"
        st.session_state.form_data = {}

# ---- Page Logic ----
if st.session_state.page == "choice":
    page_choice()
elif st.session_state.page == "manual_form":
    page_manual_form()
elif st.session_state.page == "resume_upload":
    page_resume_upload()
elif st.session_state.page == "results":
    page_results()
