import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Page Configuration
st.set_page_config(
    page_title="IMCG F-7/2 Girls Guide Portal",
    page_icon="logo.png" if os.path.exists("logo.png") else "🏕️",
    layout="wide"
)

# Custom Styling Fix for Light Mode Inputs
st.markdown("""
<style>
    /* Force text and background defaults */
    body, .stApp {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    
    /* Input Boxes Styling Fix */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    
    input {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }

    /* Custom Header Banner */
    .header-box {
        background: linear-gradient(135deg, #5c1d2e 0%, #801b38 100%);
        border-radius: 16px;
        padding: 2rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-box h1 {
        color: #ffffff !important;
        margin-bottom: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Admin Security Key
ADMIN_PASS = "imcg_f72_admin"

# Sidebar Setup
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)

st.sidebar.title("IMCG F-7/2 Portal")
portal_selection = st.sidebar.radio("Navigate View:", ["🎓 Student Application", "📊 Admin Analytics Dashboard"])

if portal_selection == "🎓 Student Application":
    
    # Logo Display in Header
    if os.path.exists("logo.png"):
        col_a, col_b, col_c = st.columns([2, 1, 2])
        with col_b:
            st.image("logo.png", use_column_width=True)

    st.markdown("""
    <div class="header-box">
        <h1>IMCG F-7/2 Girls Guide Assessment</h1>
        <p>Discover Your Leadership Persona • Join the Sisterhood</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_form"):
        st.subheader("📋 1. Student Identity & Contact Information")
        
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *")
            roll_no = st.text_input("College Roll No / Student ID *")
            class_sec = st.text_input("Class & Section *")
        with col2:
            father_name = st.text_input("Father / Guardian Name *")
            cnic = st.text_input("Father CNIC / Form-B Number *")
            consent = st.checkbox("I have parent/guardian consent for outdoor activities *")

        st.divider()

        st.subheader("🆔 2. Campus Verification Uploads")
        c1, c2 = st.columns(2)
        with c1:
            student_photo = st.file_uploader("Upload Student Photo *", type=["jpg", "png", "jpeg"])
            college_id = st.file_uploader("Upload College ID Card *", type=["jpg", "png", "pdf", "jpeg"])
        with c2:
            bus_card = st.file_uploader("Upload College Bus Pass / ID *", type=["jpg", "png", "pdf", "jpeg"])
            guardian_consent_doc = st.file_uploader("Upload Signed Guardian Consent Slip *", type=["jpg", "png", "pdf", "jpeg"])

        st.divider()

        st.subheader("🧭 3. Situational Discovery Assessment")

        scenarios = [
            ("Q1. Heavy rain interrupts setting up camp. What is your immediate reaction?", [
                ("Reorganize tasks and give clear steps to keep shelter setup moving forward.", "Expedition Leader"),
                ("Gather everyone, ensure no one is cold, and keep team spirit high.", "Unity Builder"),
                ("Quickly organize tarps and move equipment to dry spots.", "Logistics Captain"),
                ("Find natural trees/terrain to construct an improvised storm shield.", "Resource Innovator")
            ]),
            ("Q2. A hesitant new student joins your unit. How do you help her fit in?", [
                ("Pair up with her immediately so she feels welcome.", "Unity Builder"),
                ("Explain the day's routine so she knows exactly what to expect.", "Logistics Captain"),
                ("Assign her an active role so she feels included right away.", "Expedition Leader"),
                ("Start a friendly conversation about shared interests.", "Resource Innovator")
            ]),
            ("Q3. Your community project is running behind schedule. What do you do?", [
                ("Adjust the task list and redirect team members to bottleneck areas.", "Logistics Captain"),
                ("Give an encouraging pep talk to boost the team's speed.", "Unity Builder"),
                ("Set micro-goals and push the pace by leading from the front.", "Expedition Leader"),
                ("Find a simpler, faster way to complete the remaining tasks.", "Resource Innovator")
            ]),
            ("Q4. Two members disagree on who leads a presentation. How do you handle it?", [
                ("Listen to both and guide them to a fair middle ground.", "Unity Builder"),
                ("Divide the presentation cleanly into two equal parts.", "Logistics Captain"),
                ("Step in, make a clear decision, and assign specific topics.", "Expedition Leader"),
                ("Suggest an interactive dual-presenter format.", "Resource Innovator")
            ]),
            ("Q5. On a trail walk, your map goes missing. How do you respond?", [
                ("Remain calm and guide the group using key landmarks.", "Expedition Leader"),
                ("Use natural signs like sun orientation and landscape features.", "Resource Innovator"),
                ("Halt the team, inventory supplies, and plan a safe route back.", "Logistics Captain"),
                ("Keep the group relaxed with upbeat conversation while assessing options.", "Unity Builder")
            ])
        ]

        answers = []
        for idx, (q_text, opts) in enumerate(scenarios, start=1):
            st.write(f"**{q_text}**")
            opt_texts = [o[0] for o in opts]
            choice = st.radio(f"Select response for Q{idx}", opt_texts, key=f"q_{idx}")
            trait = next(t for text, t in opts if text == choice)
            answers.append(trait)

        submit_btn = st.form_submit_button("Submit Application & View Persona Badge")

    if submit_btn:
        if not full_name or not roll_no or not student_photo or not college_id or not consent:
            st.error("⚠️ Please fill in all required fields (*) and upload student photo & college ID!")
        else:
            scores = {t: answers.count(t) for t in set(answers)}
            top_persona = max(scores, key=scores.get) if scores else "Expedition Leader"
            
            st.success(f"Application Submitted! Assigned Badge: **{top_persona}**")

else:
    st.title("🔒 Administration Analytics & Records")
    admin_input = st.text_input("Enter Admin Security Key:", type="password")
    
    if admin_input == ADMIN_PASS:
        st.success("Authenticated")
        mock_data = {
            "Roll No": ["101", "102", "103"],
            "Student Name": ["Ayesha Khan", "Zainab Ahmed", "Fatima Ali"],
            "Assigned Persona": ["Expedition Leader", "Unity Builder", "Logistics Captain"]
        }
        df = pd.DataFrame(mock_data)
        st.dataframe(df)
    elif admin_input:
        st.error("Access Denied")
