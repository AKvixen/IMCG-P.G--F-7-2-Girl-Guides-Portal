import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & GEN-Z VIBRANT STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="IMCG F-7/2 Girl Guides Selection Portal",
    page_icon="logo.png" if os.path.exists("logo.png") else "✨",
    layout="wide"
)

# Gen-Z Vibrant CSS Theme (Burgundy, Fuchsia, Coral, Violet)
st.markdown("""
<style>
    /* Vibrant Canvas Background */
    .stApp {
        background: linear-gradient(135deg, #fdf2f8 0%, #f3e8ff 50%, #f0fdf4 100%) !important;
        color: #1e1b4b !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hero Banner Header */
    .genz-banner {
        background: linear-gradient(135deg, #701a75 0%, #801b38 50%, #c026d3 100%);
        border-radius: 24px;
        padding: 2.5rem 1.5rem;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 20px 30px -10px rgba(112, 26, 117, 0.3);
        margin-bottom: 2rem;
    }
    .genz-banner h1 {
        color: #ffffff !important;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .genz-banner p {
        color: #fbcfe8 !important;
        font-size: 1.2rem;
        font-weight: 500;
        margin: 0;
    }

    /* Section Cards */
    div[data-testid="stForm"] {
        background-color: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid #f472b6;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    }

    /* Vibrant Subheaders */
    h2, h3, .stSubheader {
        color: #701a75 !important;
        font-weight: 700 !important;
    }

    /* Form Input Fixes with Purple Accent */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #ffffff !important;
        color: #1e1b4b !important;
        border: 2px solid #e9d5ff !important;
        border-radius: 12px !important;
    }
    input, textarea {
        color: #1e1b4b !important;
        background-color: #ffffff !important;
    }

    /* Radio Button Custom Cards */
    div[role="radiogroup"] > label {
        background: #ffffff;
        border: 2px solid #f3e8ff;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
        color: #1e1b4b !important;
    }
    div[role="radiogroup"] > label:hover {
        border-color: #c026d3;
        background: #fdf4ff;
    }

    /* Divider Styling */
    hr {
        border-top: 3px solid #f472b6 !important;
        border-radius: 3px;
        opacity: 0.6;
    }
</style>
""", unsafe_allow_html=True)

ADMIN_PASS = "imcg_f72_admin"

# -----------------------------------------------------------------------------
# 2. SIDEBAR BRANDING
# -----------------------------------------------------------------------------
st.sidebar.markdown("# ⚜️ Girl Guides")
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
else:
    st.sidebar.markdown("### 🏆 IMCG F-7/2 Shield")

st.sidebar.markdown("---")
portal_selection = st.sidebar.radio(
    "✨ Select Portal View:",
    ["🎓 Student Application", "📊 Admin Analytics Dashboard"]
)

# -----------------------------------------------------------------------------
# 3. STUDENT APPLICATION VIEW
# -----------------------------------------------------------------------------
if portal_selection == "🎓 Student Application":

    # Centered Logo Display
    col_l1, col_l2, col_l3 = st.columns([2, 1, 2])
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center;'>⚜️</h1>", unsafe_allow_html=True)

    # Hero Banner
    st.markdown("""
    <div class="genz-banner">
        <h1>IMCG F-7/2 Girl Guides Selection Portal</h1>
        <p>🌟 Discover Your Leadership Persona • Join the Sisterhood 🏕️</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_registration_form", clear_on_submit=False):

        # SECTION 1: IDENTITY & CONTACT
        st.subheader("📋 1. Student Identity & Contact Details")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *", placeholder="e.g., Ayesha Khan")
            roll_no = st.text_input("College Roll No / Student ID *", placeholder="e.g., 2024-BIO-101")
            class_sec = st.text_input("Class & Section *", placeholder="e.g., 2nd Year Pre-Medical A")
            phone_no = st.text_input("Contact / WhatsApp Number *", placeholder="e.g., 0300-1234567")
        with col2:
            father_name = st.text_input("Father / Guardian Name *", placeholder="e.g., Muhammad Khan")
            cnic = st.text_input("Father CNIC / Form-B Number *", placeholder="e.g., 37405-XXXXXXX-X")
            address = st.text_area("Residential Address *", placeholder="House #, Street, Sector, City", height=105)

        consent = st.checkbox("I have parent/guardian consent for outdoor camps & Girl Guide activities *")

        st.divider()

        # SECTION 2: CAMPUS VERIFICATION & CERTIFICATE UPLOADS
        st.subheader("🆔 2. Campus Verification & Certificate Uploads")
        st.caption("Upload clear photos or PDFs for administrative validation.")
        
        up1, up2 = st.columns(2)
        with up1:
            student_photo = st.file_uploader("Upload Student Passport Photo *", type=["jpg", "png", "jpeg"])
            college_id = st.file_uploader("Upload College ID Card (Front) *", type=["jpg", "png", "pdf", "jpeg"])
            bus_card = st.file_uploader("Upload College Bus Pass / ID (Optional)", type=["jpg", "png", "pdf", "jpeg"])
        with up2:
            consent_doc = st.file_uploader("Upload Signed Parent Consent Slip *", type=["jpg", "png", "pdf", "jpeg"])
            certificates = st.file_uploader("Upload Extracurricular / Prior Achievement Certificates *", type=["jpg", "png", "pdf", "jpeg"], accept_multiple_files=True)

        st.divider()

        # SECTION 3: ALL 15 SITUATIONAL QUESTIONS
        st.subheader("🧭 3. Situational Discovery Assessment")
        st.info("Answer all 15 scenarios below to uncover your unique leadership badge!")

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
            ]),
            ("Q6. What role appeals to you most in an environmental awareness campaign?", [
                ("Designing creative posters, recycling ideas, and campaign concepts.", "Resource Innovator"),
                ("Coordinating booth schedules and managing logistics.", "Logistics Captain"),
                ("Leading speeches and rallying student volunteers.", "Expedition Leader"),
                ("Welcoming visitors and ensuring all volunteers feel supported.", "Unity Builder")
            ]),
            ("Q7. During a community drive, food/water supplies run low. What is your move?", [
                ("Audit current stock and establish an exact rationing plan.", "Logistics Captain"),
                ("Inquire with nearby partners or innovate solutions with available supplies.", "Resource Innovator"),
                ("Share your own supplies to ensure everyone stays fed and happy.", "Unity Builder"),
                ("Take charge to request emergency restocking from central command.", "Expedition Leader")
            ]),
            ("Q8. A peer gets minor injuries on a trek. What is your immediate action?", [
                ("Deliver swift first aid while maintaining group order.", "Expedition Leader"),
                ("Comfort her, hold her hand, and reduce her anxiety.", "Unity Builder"),
                ("Retrieve the first-aid kit systematically and record the incident.", "Logistics Captain"),
                ("Improvise a comfortable splint/cushion using available clothing.", "Resource Innovator")
            ]),
            ("Q9. Your unit is tasking you to host a flag-hoisting ceremony. Where do you start?", [
                ("Create a detailed timeline, checklist, and item placement list.", "Logistics Captain"),
                ("Brief team leads on protocol and march discipline.", "Expedition Leader"),
                ("Focus on team coordination so everyone feels confident in their role.", "Unity Builder"),
                ("Design unique stage decor using hand-crafted regional motifs.", "Resource Innovator")
            ]),
            ("Q10. Your group must present project findings to the principal. What is your role?", [
                ("Deliver the primary opening speech and executive summary.", "Expedition Leader"),
                ("Build an engaging visual slide deck with interactive diagrams.", "Resource Innovator"),
                ("Organize all data tables, handouts, and backup notes.", "Logistics Captain"),
                ("Ensure every teammate gets an equal opportunity to speak.", "Unity Builder")
            ]),
            ("Q11. Assigned night guard duty at camp. How do you stay alert and keep order?", [
                ("Follow a strict perimeter schedule and perform timed checks.", "Logistics Captain"),
                ("Keep patrol watch with high vigilance and leadership readiness.", "Expedition Leader"),
                ("Keep quiet watch while creating fun night-time signaling hacks.", "Resource Innovator"),
                ("Pair up with a partner so both stay awake and safe together.", "Unity Builder")
            ]),
            ("Q12. A tent pole breaks in strong winds. How do you tackle the issue?", [
                ("Use a sturdy branch and rope to craft an emergency support splint.", "Resource Innovator"),
                ("Direct team members on holding structure while repairing it.", "Expedition Leader"),
                ("Safely move contents to an alternate tent according to camp contingency.", "Logistics Captain"),
                ("Reassure tent occupants and keep morale calm.", "Unity Builder")
            ]),
            ("Q13. Team is exhausted on a steep walk and wants to stop. How do you motivate them?", [
                ("Start a rhythmic marching song to lift energy levels.", "Unity Builder"),
                ("Remind everyone of the objective and lead from the front.", "Expedition Leader"),
                ("Schedule a structured 5-minute rest stop with scheduled hydration.", "Logistics Captain"),
                ("Introduce short rest games or point out interesting landmarks.", "Resource Innovator")
            ]),
            ("Q14. Teaching junior guides a knot-tying/first-aid module. How do you teach?", [
                ("Demonstrate step-by-step with clear, structured repetitions.", "Logistics Captain"),
                ("Turn learning into an energetic team game or contest.", "Unity Builder"),
                ("Show inventive real-life scenarios where each knot is useful.", "Resource Innovator"),
                ("Set high standards and test their mastery firmly.", "Expedition Leader")
            ]),
            ("Q15. Planning a cultural campfire night. What is your main contribution?", [
                ("Host the ceremony and guide the event flow smoothly.", "Expedition Leader"),
                ("Perform in group skits and make sure everyone participates.", "Unity Builder"),
                ("Manage seating, campfire safety gear, and sound equipment.", "Logistics Captain"),
                ("Write original campfire songs, plays, or creative props.", "Resource Innovator")
            ])
        ]

        user_responses = {}
        trait_scores = {"Expedition Leader": 0, "Unity Builder": 0, "Logistics Captain": 0, "Resource Innovator": 0}

        for idx, (q_text, options) in enumerate(scenarios, start=1):
            st.write(f"**{q_text}**")
            opt_texts = [o[0] for o in options]
            choice = st.radio(f"Select option for Q{idx}", opt_texts, key=f"q_{idx}")
            
            selected_trait = next(trait for text, trait in options if text == choice)
            trait_scores[selected_trait] += 1
            user_responses[f"Q{idx}"] = choice

        st.divider()
        submit_btn = st.form_submit_button("🔥 Submit Application & Reveal Badge")

    if submit_btn:
        if not full_name or not roll_no or not class_sec or not father_name or not consent or not student_photo or not college_id:
            st.error("⚠️ Please fill in all required fields (*) and upload student photo & college ID!")
        else:
            top_persona = max(trait_scores, key=trait_scores.get)
            st.balloons()
            st.success(f"🎉 Application Successfully Submitted for **{full_name}** ({roll_no})!")
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fdf4ff 0%, #f0fdf4 100%); border: 3px solid #c026d3; border-radius: 20px; padding: 2rem; text-align: center; margin-top: 1rem;">
                <h3 style="color: #701a75; margin: 0;">🎉 Congratulations!</h3>
                <p style="color: #475569; margin-bottom: 0.5rem;">Your Assigned Girl Guide Persona Badge is:</p>
                <h1 style="color: #c026d3; font-size: 2.5rem; margin: 0;">🏅 {top_persona}</h1>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. ADMIN ANALYTICS DASHBOARD VIEW
# -----------------------------------------------------------------------------
else:
    st.title("🔒 Administration Analytics & Polls")
    st.caption("Enter administrative credentials to view live metrics and graphs.")
    
    admin_input = st.text_input("Enter Admin Passcode:", type="password")

    if admin_input == ADMIN_PASS:
        st.success("Authenticated as IMCG F-7/2 Administrator")

        # Mock applicant dataset for analytics visualization
        df = pd.DataFrame([
            {"Full Name": "Ayesha Khan", "Roll No": "101", "Class & Section": "2nd Year Bio A", "Assigned Persona": "Expedition Leader", "Q1": "Reorganize tasks..."},
            {"Full Name": "Zainab Ahmed", "Roll No": "102", "Class & Section": "2nd Year Bio B", "Assigned Persona": "Unity Builder", "Q1": "Gather everyone..."},
            {"Full Name": "Fatima Ali", "Roll No": "103", "Class & Section": "1st Year Pre-Eng A", "Assigned Persona": "Logistics Captain", "Q1": "Quickly organize..."},
            {"Full Name": "Maryam Bibi", "Roll No": "104", "Class & Section": "2nd Year Bio A", "Assigned Persona": "Resource Innovator", "Q1": "Find natural trees..."},
            {"Full Name": "Sana Tariq", "Roll No": "105", "Class & Section": "1st Year Pre-Eng A", "Assigned Persona": "Expedition Leader", "Q1": "Reorganize tasks..."}
        ])

        # Overview Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Submissions", len(df), "+5 Today")
        m2.metric("Top Persona", "Expedition Leader", "40%")
        m3.metric("Certificates Uploaded", "100%", "Verified")

        st.divider()

        # Graphs
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.subheader("📊 Persona Distribution Pie Chart")
            fig_pie = px.pie(
                df, 
                names="Assigned Persona", 
                title="Applicant Persona Breakdown",
                color_discrete_sequence=['#701a75', '#c026d3', '#0284c7', '#059669']
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_g2:
            st.subheader("🏫 Applicants by Class")
            fig_bar = px.histogram(
                df, 
                x="Class & Section", 
                color="Assigned Persona", 
                title="Submissions by Class & Department",
                barmode="stack",
                color_discrete_sequence=['#701a75', '#c026d3', '#0284c7', '#059669']
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        # Question Poll Analytics
        st.subheader("📈 Question Poll Analytics")
        selected_q = st.selectbox("Select Assessment Question to View Poll Results:", [f"Q{i}" for i in range(1, 16)])
        
        if selected_q in df.columns:
            fig_q = px.bar(
                df[selected_q].value_counts().reset_index(),
                x="count",
                y=selected_q,
                orientation='h',
                title=f"Response Poll for {selected_q}",
                labels={"count": "Student Count", selected_q: "Selected Option"},
                color_discrete_sequence=['#701a75']
            )
            st.plotly_chart(fig_q, use_container_width=True)

        st.divider()

        st.subheader("📄 Registered Applicants Table")
        st.dataframe(df, use_container_width=True)

    elif admin_input:
        st.error("Access Denied: Invalid Security Passcode")
