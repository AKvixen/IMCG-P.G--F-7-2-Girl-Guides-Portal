import streamlit as st
import pandas as pd

st.set_page_config(page_title="Girl Guides Selection Portal", page_icon="⚜️", layout="wide")

if 'applications' not in st.session_state:
    st.session_state['applications'] = []

st.sidebar.title("⚜️ Navigation")
mode = st.sidebar.radio("Select View:", ["Student Application Portal", "Admin Dashboard"])

# ==========================================
# STUDENT APPLICATION PORTAL
# ==========================================
if mode == "Student Application Portal":
    st.title("⚜️ Girl Guides Selection & Skill Assessment Portal")
    st.write("Complete your registration, upload documents, and take the self-discovery assessment to reveal your Girl Guide Persona Badge!")
    st.markdown("---")

    with st.form("application_form", clear_on_submit=False):
        # 1. Student Info
        st.subheader("1. Student & Guardian Information")
        col1, col2 = st.columns(2)
        with col1:
            student_name = st.text_input("Full Name *")
            roll_no = st.text_input("Roll No / Student ID *")
            class_sec = st.text_input("Class & Section *")
        with col2:
            father_name = st.text_input("Father's / Guardian's Name *")
            father_cnic_no = st.text_input("Father's CNIC Number *")
            outdoor_consent = st.checkbox("I have father/guardian consent for outdoor activities & camps *")

        st.markdown("---")
        # 2. Document Uploads
        st.subheader("2. Document Uploads")
        dcol1, dcol2 = st.columns(2)
        with dcol1:
            student_photo = st.file_uploader("Upload Student Photo *", type=['jpg', 'jpeg', 'png'])
            father_cnic_doc = st.file_uploader("Upload Father's CNIC Copy *", type=['pdf', 'jpg', 'png'])
        with dcol2:
            consent_form = st.file_uploader("Upload Signed Father Consent Form *", type=['pdf', 'jpg', 'png'])
            certificates = st.file_uploader("Upload Previous Certificates (Optional)", type=['pdf', 'jpg', 'png'], accept_multiple_files=True)

        st.markdown("---")
        # 3. Assessment Questionnaire
        st.subheader("3. Self-Discovery & Persona Assessment")

        q1 = st.radio(
            "Q1. Self-Discovery Preference: When working on a project, I feel most comfortable when I...",
            [
                "👑 Lead the vision, delegate tasks, and guide others to the finish line. (Leadership)",
                "🤝 Keep everyone involved, resolve disagreements, and ensure no one feels left out. (Teamwork & Inclusion)",
                "📋 Create detailed planning, manage time schedules, and organize resources. (Organization)",
                "🏔️ Adapt quickly, stay calm when plans fail, and figure out practical fixes. (Problem Solving & Resilience)"
            ]
        )

        q2 = st.radio(
            "Q2. Scenario Validation: Your unit is running a community drive, but tasks are falling behind schedule. What is your reaction?",
            [
                "Step up immediately, reorganize team roles, and keep everyone accountable. (Leadership - Expedition Leader)",
                "Listen to team members' concerns, encourage everyone kindly, and maintain unity. (Teamwork - Unity Builder)",
                "Adjust the timetable, make a checklist of remaining items, and track progress closely. (Organization - Logistics Captain)",
                "Find creative shortcuts and remain calm despite unexpected changes. (Problem Solver - Wilderness Resource)"
            ]
        )

        q3 = st.radio(
            "Q3. Inclusive Mindset: A new girl joins your team and seems hesitant to participate. You:",
            [
                "Welcome her warmly, assign her a buddy, and make sure she feels valued. (Inclusive Mindset)",
                "Explain the project structure clearly so she knows exactly what to do. (Organization)",
                "Ask her directly what role she would like to take in leading a sub-task. (Leadership)",
                "Encourage her to share her creative ideas with the whole group. (Active Communicator)"
            ]
        )

        q4 = st.radio(
            "Q4. Civic & Ethical Drive: On a camping trip or community activity, which task excites you most?",
            [
                "Leading environmental conservation drives and community volunteerism. (Community-Minded)",
                "Upholding the Girl Guide Law, ensuring honesty, fairness, and mutual respect. (Principled)",
                "Setting up tents, knot-tying, and managing equipment. (Wilderness Resource)",
                "Coordinating logistics, attendance records, and meal schedules. (Logistics Captain)"
            ]
        )

        q5 = st.radio(
            "Q5. Adaptability & Resilience: Outdoor weather suddenly turns bad during a campus activity. How do you respond?",
            [
                "Remain calm, stay positive, and quickly figure out a safe alternative plan. (Resilient & Adaptable)",
                "Communicate instructions clearly and guide team members to safety. (Active Communicator)",
                "Ensure every girl is safe, comfortable, and accounted for. (Inclusive & Caretaker)",
                "Organize supplies and protect equipment from getting damaged. (Logistics Captain)"
            ]
        )

        submit_btn = st.form_submit_button("Submit Application & Generate Badge")

    # Processing Submission
    if submit_btn:
        if not student_name or not roll_no or not father_cnic_no or not outdoor_consent or not student_photo or not consent_form:
            st.error("⚠️ Please complete all required student fields and upload mandatory documents.")
        else:
            # Trait Scoring System
            scores = {
                "Leadership (Expedition Leader)": 0,
                "Teamwork & Communication (Unity Builder)": 0,
                "Organization (Logistics Captain)": 0,
                "Problem Solving (Wilderness Resource)": 0,
                "Civic & Ethical (Community & Principled)": 0
            }

            total_points = 0

            # Q1
            if "👑" in q1: scores["Leadership (Expedition Leader)"] += 20; total_points += 20
            elif "🤝" in q1: scores["Teamwork & Communication (Unity Builder)"] += 20; total_points += 20
            elif "📋" in q1: scores["Organization (Logistics Captain)"] += 20; total_points += 20
            elif "🏔️" in q1: scores["Problem Solving (Wilderness Resource)"] += 20; total_points += 20

            # Q2
            if "Expedition Leader" in q2: scores["Leadership (Expedition Leader)"] += 20; total_points += 20
            elif "Unity Builder" in q2: scores["Teamwork & Communication (Unity Builder)"] += 20; total_points += 20
            elif "Logistics Captain" in q2: scores["Organization (Logistics Captain)"] += 20; total_points += 20
            elif "Wilderness Resource" in q2: scores["Problem Solving (Wilderness Resource)"] += 20; total_points += 20

            # Q3
            if "Inclusive Mindset" in q3: scores["Teamwork & Communication (Unity Builder)"] += 20; total_points += 20
            elif "Organization" in q3: scores["Organization (Logistics Captain)"] += 18; total_points += 18
            elif "Leadership" in q3: scores["Leadership (Expedition Leader)"] += 20; total_points += 20
            elif "Active Communicator" in q3: scores["Teamwork & Communication (Unity Builder)"] += 18; total_points += 18

            # Q4
            if "Community-Minded" in q4: scores["Civic & Ethical (Community & Principled)"] += 20; total_points += 20
            elif "Principled" in q4: scores["Civic & Ethical (Community & Principled)"] += 20; total_points += 20
            elif "Wilderness Resource" in q4: scores["Problem Solving (Wilderness Resource)"] += 18; total_points += 18
            elif "Logistics Captain" in q4: scores["Organization (Logistics Captain)"] += 18; total_points += 18

            # Q5
            if "Resilient & Adaptable" in q5: scores["Problem Solving (Wilderness Resource)"] += 20; total_points += 20
            elif "Active Communicator" in q5: scores["Teamwork & Communication (Unity Builder)"] += 18; total_points += 18
            elif "Inclusive" in q5: scores["Teamwork & Communication (Unity Builder)"] += 18; total_points += 18
            elif "Logistics Captain" in q5: scores["Organization (Logistics Captain)"] += 18; total_points += 18

            percentage = min(total_points, 100)

            # Determine Qualification Status
            if percentage >= 70:
                status = "Qualified for Interview (>= 70%)"
                badge_type = "🥇 High Potential Guide Candidate"
            elif 50 <= percentage < 70:
                status = "Negotiable / Secondary Review (50% - 69%)"
                badge_type = "🥈 Developing Candidate"
            else:
                status = "Non-Negotiable / Below Threshold (< 50%)"
                badge_type = "🥉 Non-Selected"

            # Determine Persona
            top_persona = max(scores, key=scores.get)

            # Save Application Record
            st.session_state['applications'].append({
                "Roll No": roll_no,
                "Name": student_name,
                "Class": class_sec,
                "Father Name": father_name,
                "CNIC": father_cnic_no,
                "Score (%)": percentage,
                "Status": status,
                "Primary Persona": top_persona,
                "Father Consent": "Yes" if outdoor_consent else "No"
            })

            st.markdown("---")
            st.subheader("🎉 Your Assessment Results & Guide Persona Badge")

            if percentage >= 70:
                st.success(f"**Status: {status}**")
            elif percentage >= 50:
                st.warning(f"**Status: {status}**")
            else:
                st.error(f"**Status: {status}**")

            bcol1, bcol2 = st.columns(2)
            with bcol1:
                st.metric("Total Qualification Score", f"{percentage}%")
                st.subheader(f"Assigned Persona:")
                st.info(f"**{top_persona}**")
                st.write(f"**Guide Level Badge:** {badge_type}")

            with bcol2:
                st.write("### Attribute Breakdown")
                df_attr = pd.DataFrame(list(scores.items()), columns=["Attribute / Persona Dimension", "Score Contribution"])
                st.dataframe(df_attr, use_container_width=True)

# ==========================================
# ADMIN DASHBOARD
# ==========================================
else:
    st.title("🔒 Admin Candidate Management Dashboard")
    st.write("View submitted applications, filter candidates, and download full records.")

    if len(st.session_state['applications']) == 0:
        st.info("No applications submitted yet.")
    else:
        df_all = pd.DataFrame(st.session_state['applications'])

        # Metrics Overview
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Applicants", len(df_all))
        m2.metric("Qualified (>=70%)", len(df_all[df_all["Score (%)"] >= 70]))
        m3.metric("Negotiable (50-69%)", len(df_all[(df_all["Score (%)"] >= 50) & (df_all["Score (%)"] < 70)]))
        m4.metric("Non-Negotiable (<50%)", len(df_all[df_all["Score (%)"] < 50]))

        st.markdown("---")
        st.dataframe(df_all, use_container_width=True)

        # Export CSV
        csv_data = df_all.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Candidate Records (CSV)",
            data=csv_data,
            file_name="girl_guide_applicants.csv",
            mime="text/csv"
        )
