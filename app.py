import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Girl Guides Selection Portal",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Gen-Z Styling & Light Theme Injection
st.markdown("""
<style>
    /* Force Light Canvas Theme */
    .stApp {
        background-color: #f4f7f6 !important;
        color: #2b2d42 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sleek Navigation Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Vibrant Gen-Z Banner */
    .genz-header {
        background: linear-gradient(135deg, #004b23 0%, #38b000 50%, #70e000 100%);
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(56, 176, 0, 0.2);
        margin-bottom: 2rem;
    }
    .genz-header h1 {
        color: #ffdd00 !important;
        font-weight: 800;
        font-size: 2.3rem;
        margin-bottom: 0.2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Elegant Cards */
    .form-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 1.8rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
    }
    
    /* Classy Gradient Divider */
    .classy-divider {
        height: 3px;
        background: linear-gradient(90deg, #38b000 0%, #ffdd00 50%, #38b000 100%);
        border-radius: 2px;
        margin: 2rem 0;
    }

    /* Badge Card Output */
    .badge-result {
        background: linear-gradient(135deg, #fff9db 0%, #fff3bf 100%);
        border: 2px solid #fab005;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 20px rgba(250, 176, 5, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Admin Credentials
ADMIN_PASS = "imcg_f72_admin"

# Sidebar Portal Switcher
st.sidebar.image("https://img.icons8.com/color/96/girl-scout.png", width=80)
st.sidebar.title("⚜️ Girl Guides Portal")
portal_selection = st.sidebar.radio("Navigate View:", ["🎓 Student Application", "📊 Admin Analytics Dashboard"])

# ==========================================
# VIEW 1: STUDENT APPLICATION PORTAL
# ==========================================
if portal_selection == "🎓 Student Application":
    
    # Hero Banner with Cartoon Girl Guide Visual
    st.markdown("""
    <div class="genz-header">
        <div style="font-size: 3.5rem; margin-bottom: -10px;">⚜️ 👧🏻🧕🏽👧🏼 ⚜️</div>
        <h1>IMCG F-7/2 Girl Guides Assessment</h1>
        <p style="font-size: 1.1rem; opacity: 0.95;">Discover Your Leadership Persona • Join the Sisterhood</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_form"):
        # Section 1
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.subheader("📋 1. Student Identity & Contact Information")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *")
            roll_no = st.text_input("College Roll No / Student ID *")
            class_sec = st.text_input("Class & Section (e.g., 2nd Year FSc Bio) *")
        with col2:
            father_name = st.text_input("Father / Guardian Name *")
            cnic = st.text_input("Father CNIC / Form-B Number *")
            consent = st.checkbox("I have parent/guardian consent for outdoor camps & activities *")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="classy-divider"></div>', unsafe_allow_html=True)

        # Section 2
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.subheader("🆔 2. Campus Verification Uploads")
        st.info("Upload scanned photos or clear phone pictures to verify student status.")
        
        c1, c2 = st.columns(2)
        with c1:
            student_photo = st.file_uploader("Upload Student Photo *", type=["jpg", "png", "jpeg"])
            college_id = st.file_uploader("Upload College ID Card *", type=["jpg", "png", "pdf", "jpeg"])
        with c2:
            bus_card = st.file_uploader("Upload College Bus Pass / ID *", type=["jpg", "png", "pdf", "jpeg"])
            guardian_consent_doc = st.file_uploader("Upload Signed Guardian Consent Slip *", type=["jpg", "png", "pdf", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="classy-divider"></div>', unsafe_allow_html=True)

        # Section 3: 15 Unlabeled Scenario Questions
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        st.subheader("🧭 3. Situational Discovery Assessment")
        st.write("Choose the option that reflects your natural reaction in each real-life scenario.")

        scenarios = [
            ("Q1. Heavy rain interrupts setting up camp. What is your immediate reaction?", [
                ("Reorganize tasks and give clear steps to keep shelter setup moving forward.", "Leader"),
                ("Gather everyone, ensure no one is cold, and keep team spirit high.", "Unity Builder"),
                ("Quickly organize tarps and move equipment to dry spots.", "Logistics"),
                ("Find natural trees/terrain to construct an improvised storm shield.", "Innovator")
            ]),
            ("Q2. A hesitant new student joins your unit. How do you help her fit in?", [
                ("Pair up with her immediately so she feels welcome.", "Unity Builder"),
                ("Explain the day's routine so she knows exactly what to expect.", "Logistics"),
                ("Assign her an active role so she feels included right away.", "Leader"),
                ("Start a friendly conversation about shared interests.", "Innovator")
            ]),
            ("Q3. Your community project is running behind schedule. What do you do?", [
                ("Adjust the task list and redirect team members to bottleneck areas.", "Logistics"),
                ("Give an encouraging pep talk to boost the team's speed.", "Unity Builder"),
                ("Set micro-goals and push the pace by leading from the front.", "Leader"),
                ("Find a simpler, faster way to complete the remaining tasks.", "Innovator")
            ]),
            ("Q4. Two members disagree on who leads a presentation. How do you handle it?", [
                ("Listen to both and guide them to a fair middle ground.", "Unity Builder"),
                ("Divide the presentation cleanly into two equal parts.", "Logistics"),
                ("Step in, make a clear decision, and assign specific topics.", "Leader"),
                ("Suggest an interactive dual-presenter format.", "Innovator")
            ]),
            ("Q5. On a trail walk, your map goes missing. How do you respond?", [
                ("Remain calm and guide the group using key landmarks.", "Leader"),
                ("Use natural signs like sun orientation and landscape features.", "Innovator"),
                ("Halt the team, inventory supplies, and plan a safe route back.", "Logistics"),
                ("Keep the group relaxed with upbeat conversation while assessing options.", "Unity Builder")
            ]),
            ("Q6. What role appeals to you most in an environmental campaign?", [
                ("Delivering awareness speeches and engaging the audience.", "Leader"),
                ("Managing schedule schedules, equipment, and venue setup.", "Logistics"),
                ("Connecting with community families to encourage participation.", "Unity Builder"),
                ("Designing posters, banners, and recycled display items.", "Innovator")
            ]),
            ("Q7. During a campus safety drill, which task do you volunteer for?", [
                ("Handling safety gear, knot lashings, or emergency kits.", "Innovator"),
                ("Narrating safety steps clearly to the audience.", "Leader"),
                ("Keeping attendance lists and managing group order.", "Logistics"),
                ("Ensuring everyone stays calm and moves safely.", "Unity Builder")
            ]),
            ("Q8. Unplanned cold weather sets in during an outdoor activity. You:", [
                ("Arrange hot drinks and ensure everyone stays warm.", "Unity Builder"),
                ("Build a windbreak barrier using available gear.", "Innovator"),
                ("Keep morale high through group songs and team games.", "Leader"),
                ("Adjust the timetable to finish key tasks early.", "Logistics")
            ]),
            ("Q9. Managing a limited event budget, you prefer to:", [
                ("Keep precise itemized records of every expense.", "Logistics"),
                ("Repurpose available materials into creative setups.", "Innovator"),
                ("Reach out to local sponsors for support.", "Unity Builder"),
                ("Coordinate team members to source materials efficiently.", "Leader")
            ]),
            ("Q10. Constructing a rope bridge across a small stream, you prefer to:", [
                ("Inspect structural lashings and knot security.", "Innovator"),
                ("Direct team positions for safe lifting and pulling.", "Leader"),
                ("Simplify the structure using existing bridge elements.", "Innovator"),
                ("Ensure safety guidelines are followed step-by-step.", "Logistics")
            ]),
            ("Q11. Representing your unit at college assembly, you:", [
                ("Deliver an inspiring speech on team achievements.", "Leader"),
                ("Present a detailed summary report of activities.", "Logistics"),
                ("Highlight how teamwork strengthened student bonds.", "Unity Builder"),
                ("Share practical skills learned during field training.", "Innovator")
            ]),
            ("Q12. During an unexpected first-aid drill, you:", [
                ("Step up and organize the response systematically.", "Leader"),
                ("Apply practical bandage and first-aid steps accurately.", "Innovator"),
                ("Delegate supply fetching and communication roles.", "Logistics"),
                ("Comfort the simulated patient and maintain calm.", "Unity Builder")
            ]),
            ("Q13. In a campus tree plantation drive, you choose to:", [
                ("Lead community outreach and planting teams.", "Leader"),
                ("Design creative signs and recycled pot planters.", "Innovator"),
                ("Track sapling distribution and inventory.", "Logistics"),
                ("Guide junior students through planting steps.", "Unity Builder")
            ]),
            ("Q14. What compliment best reflects your work style?", [
                ("'You kept the team united and supported.'", "Unity Builder"),
                ("'Your quick thinking solved an unexpected problem.'", "Innovator"),
                ("'Your leadership provided clear direction.'", "Leader"),
                ("'Your organization made everything run smoothly.'", "Logistics")
            ]),
            ("Q15. Which Girl Guide principle resonates most with you?", [
                ("Leading by example with courage and discipline.", "Leader"),
                ("Being a supportive sister to every guide.", "Unity Builder"),
                ("Being resourceful and inventive at all times.", "Innovator"),
                ("Maintaining order and duty with responsibility.", "Logistics")
            ])
        ]

        answers = []
        for idx, (q_text, opts) in enumerate(scenarios, start=1):
            st.write(f"**{q_text}**")
            opt_texts = [o[0] for o in opts]
            choice = st.radio(f"Select response for {idx}", opt_texts, index=0, key=f"q_{idx}", label_visibility="collapsed")
            trait = next(t for text, t in opts if text == choice)
            answers.append(trait)
            st.markdown("<div style='height:1px; background:#f0f0f0; margin:10px 0;'></div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        submit_btn = st.form_submit_button("⚜️ Complete Application & Generate Badge")

    if submit_btn:
        if not full_name or not roll_no or not student_photo or not college_id or not consent:
            st.error("⚠️ Please fill in all required fields (*) and upload student photo & college ID!")
        else:
            # Score Calculation
            scores = {"Leader": 0, "Unity Builder": 0, "Logistics": 0, "Innovator": 0}
            for a in answers:
                scores[a] = scores.get(a, 0) + 1
            
            top_persona = max(scores, key=scores.get)
            
            st.balloons()
            st.markdown(f"""
            <div class="badge-result">
                <span style="font-size: 3rem;">🏅</span>
                <h2 style="color: #004b23; margin:0;">Congratulations, {full_name}!</h2>
                <p style="color: #555; margin-bottom: 1rem;">Your Official Girl Guide Persona Badge is:</p>
                <h1 style="color: #d97706; font-size: 2.8rem; margin:0;">{top_persona}</h1>
                <div style="background:white; padding:1rem; border-radius:12px; margin-top:1.5rem; text-align:left;">
                    <p style="margin:4px 0;"><b>Roll No:</b> {roll_no}</p>
                    <p style="margin:4px 0;"><b>Class:</b> {class_sec}</p>
                    <p style="margin:4px 0;"><b>College:</b> IMCG F-7/2 Islamabad</p>
                    <p style="margin:4px 0;"><b>Date:</b> {datetime.now().strftime('%d %B %Y')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# VIEW 2: ADMIN ANALYTICS DASHBOARD
# ==========================================
else:
    st.title("🔒 Administration Analytics & Records")
    admin_input = st.text_input("Enter Admin Security Key:", type="password")
    
    if admin_input == ADMIN_PASS:
        st.success("Authenticated as IMCG F-7/2 College Administrator")
        st.markdown('<div class="classy-divider"></div>', unsafe_allow_html=True)

        # Mock Registered Dataset for Live Analytical View
        mock_data = {
            "Roll No": ["101", "102", "103", "104", "105", "106", "107", "108", "109", "110"],
            "Student Name": ["Ayesha Khan", "Zainab Ahmed", "Fatima Ali", "Anum Kaleem", "Maryam Tariq", "Sana Ahmed", "Hira Noor", "Zara Sheikh", "Laiba Malik", "Eman Khalid"],
            "Class": ["2nd Yr Bio", "1st Yr Pre-Med", "2nd Yr Cs", "2nd Yr Bio", "1st Yr Arts", "2nd Yr Bio", "1st Yr Pre-Med", "2nd Yr Cs", "1st Yr Pre-Med", "2nd Yr Bio"],
            "Assigned Persona": ["Leader", "Unity Builder", "Logistics", "Leader", "Innovator", "Unity Builder", "Leader", "Logistics", "Unity Builder", "Innovator"],
            "ID Verified": ["Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"]
        }
        df = pd.DataFrame(mock_data)

        # Top Metric Cards
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Total Applicants", len(df), delta="+10 Today")
        col_m2.metric("Target Quota", "100 Students", delta="10% Completed")
        col_m3.metric("Verified College IDs", "100%", delta="Secure")
        col_m4.metric("Leading Trait", "Leader (30%)")

        st.markdown("---")

        # Visual Graphs (Pie Chart & Bar Chart)
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("📊 Persona Distribution (%)")
            persona_counts = df["Assigned Persona"].value_counts().reset_index()
            persona_counts.columns = ["Persona", "Count"]
            
            fig_pie = px.pie(
                persona_counts, 
                values="Count", 
                names="Persona", 
                hole=0.4,
                color_discrete_sequence=["#38b000", "#ffdd00", "#0077b6", "#e76f51"]
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_chart2:
            st.subheader("🏫 Applicants by Department / Class")
            class_counts = df["Class"].value_counts().reset_index()
            class_counts.columns = ["Class", "Applicants"]
            
            fig_bar = px.bar(
                class_counts, 
                x="Class", 
                y="Applicants", 
                color="Class",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown('<div class="classy-divider"></div>', unsafe_allow_html=True)

        # Applicant Records Table
        st.subheader("📑 Registered Student Applications")
        st.dataframe(df, use_container_width=True)

    elif admin_input:
        st.error("Incorrect password key. Access denied.")
