import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import os

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="IMCG F-7/2 Girl Guides Selection Portal",
    page_icon="logo.png" if os.path.exists("logo.png") else "⚜️",
    layout="wide"
)

# Custom CSS to enforce clean, high-contrast inputs without black-box glitches
st.markdown("""
<style>
    /* Force canvas background */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* Maroon Banner Header */
    .header-box {
        background: linear-gradient(135deg, #5c1d2e 0%, #801b38 100%);
        border-radius: 16px;
        padding: 2.2rem;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(92, 29, 46, 0.3);
        margin-bottom: 2rem;
    }
    .header-box h1 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .header-box p {
        color: #f1f5f9 !important;
        font-size: 1.1rem;
        margin-bottom: 0;
    }

    /* Input & Select Box Overrides (Fixes Dark Mode Black Blocks) */
    div[data-baseweb="input"] > div, 
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    input, textarea {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }
    
    /* Radio Option Text Styling */
    div[role="radiogroup"] label {
        background-color: #ffffff;
        padding: 8px 14px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        color: #0f172a !important;
    }

    /* Section Cards */
    .css-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

ADMIN_PASS = "imcg_f72_admin"

# -----------------------------------------------------------------------------
# 2. SIDEBAR BRANDING & NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("### ⚜️ IMCG F-7/2 Portal")

if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)

portal_selection = st.sidebar.radio(
    "Navigate View:",
    ["🎓 Student Application", "📊 Admin Analytics Dashboard"]
)

# Initialize Google Sheets Connection
def load_gsheets_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=5)
        return conn, df
    except Exception:
        return None, pd.DataFrame()

# -----------------------------------------------------------------------------
# 3. STUDENT APPLICATION FORM VIEW
# -----------------------------------------------------------------------------
if portal_selection == "🎓 Student Application":

    # Header with Logo Centering
    if os.path.exists("logo.png"):
        col_l1, col_l2, col_l3 = st.columns([2, 1, 2])
        with col_l2:
            st.image("logo.png", use_container_width=True)

    st.markdown("""
    <div class="header-box">
        <h1>IMCG F-7/2 Girl Guides Selection Portal</h1>
        <p>Discover Your Leadership Persona • Join the Sisterhood</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_registration_form", clear_on_submit=False):

        # SECTION 1: IDENTITY & CONTACT
        st.subheader("📋 1. Student Identity & Contact Information")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *", placeholder="e.g., Ayesha Khan")
            roll_no = st.text_input("College Roll No / Student ID *", placeholder="e.g., 2024-BIO-101")
            class_sec = st.text_input("Class & Section *", placeholder="e.g., 2nd Year Pre-Medical A")
            phone_no = st.text_input("Contact Number *", placeholder="e.g., 0300-1234567")
        with col2:
            father_name = st.text_input("Father / Guardian Name *", placeholder="e.g., Muhammad Khan")
            cnic = st.text_input("Father CNIC / Form-B Number *", placeholder="e.g., 37405-XXXXXXX-X")
            address = st.text_area("Residential Address *", placeholder="House #, Street, Sector, City", height=105)

        consent = st.checkbox("I have parent/guardian consent for outdoor camps & Girl Guide activities *")

        st.divider()

        # SECTION 2: CAMPUS VERIFICATION UPLOADS
        st.subheader("🆔 2. Campus Verification Uploads")
        up1, up2 = st.columns(2)
        with up1:
            student_photo = st.file_uploader("Upload Student Passport Photo *", type=["jpg", "png", "jpeg"])
            college_id = st.file_uploader("Upload College ID Card (Front) *", type=["jpg", "png", "pdf", "jpeg"])
        with up2:
            bus_card = st.file_uploader("Upload College Bus Pass / ID (Optional)", type=["jpg", "png", "pdf", "jpeg"])
            consent_doc = st.file_uploader("Upload Signed Parent Consent Slip *", type=["jpg", "png", "pdf", "jpeg"])

        st.divider()

        # SECTION 3: ALL 15 SITUATIONAL QUESTIONS
        st.subheader("🧭 3. Situational Discovery Assessment")
        st.info("Answer all 15 scenarios to determine your Girl Guide leadership persona.")

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
            
            # Map selected option text to persona trait
            selected_trait = next(trait for text, trait in options if text == choice)
            trait_scores[selected_trait] += 1
            user_responses[f"Q{idx}"] = choice

        st.divider()
        submit_btn = st.form_submit_button("🚀 Submit Application & View Leadership Badge")

    if submit_btn:
        if not full_name or not roll_no or not class_sec or not father_name or not consent or not student_photo or not college_id:
            st.error("⚠️ Please fill in all required fields (*) and upload student photo & college ID!")
        else:
            # Determine Top Persona
            top_persona = max(trait_scores, key=trait_scores.get)
            
            # Save Record
            record = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Full Name": full_name,
                "Roll No": roll_no,
                "Class & Section": class_sec,
                "Phone": phone_no,
                "Father Name": father_name,
                "CNIC": cnic,
                "Address": address,
                "Assigned Persona": top_persona,
                "Photo Uploaded": student_photo.name if student_photo else "No",
                "ID Card Uploaded": college_id.name if college_id else "No",
                "Consent Slip Uploaded": consent_doc.name if consent_doc else "No"
            }
            # Append Q1-Q15 responses
            record.update(user_responses)

            # Try updating Google Sheets if configured
            conn, df_sheets = load_gsheets_data()
            if conn is not None:
                try:
                    updated_df = pd.concat([df_sheets, pd.DataFrame([record])], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success("Record synced with Google Sheets!")
                except Exception as e:
                    st.warning("Saved locally in session (Configure Google Sheets Secrets for persistence).")

            st.balloons()
            st.success(f"🎉 Application Successfully Submitted for **{full_name}**!")
            
            # Badge Award Card
            st.markdown(f"""
            <div style="background: #ffffff; padding: 1.5rem; border-radius: 12px; border: 2px solid #801b38; text-align: center;">
                <h2 style="color: #801b38; margin-bottom: 0;">🏅 Official Persona Badge: {top_persona}</h2>
                <p style="color: #475569;">IMCG F-7/2 Girl Guides Selection Board</p>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. ADMIN ANALYTICS DASHBOARD VIEW
# -----------------------------------------------------------------------------
else:
    st.title("🔒 Administration Analytics & Records")
    admin_input = st.text_input("Enter Admin Security Key:", type="password")

    if admin_input == ADMIN_PASS:
        st.success("Authenticated")

        conn, df = load_gsheets_data()

        # Fallback Mock Data for preview if Google Sheets is not yet populated
        if df.empty:
            st.info("Showing sample analytics data. Connect Google Sheets to view real-time submissions.")
            df = pd.DataFrame([
                {"Full Name": "Ayesha Khan", "Roll No": "101", "Class & Section": "2nd Year Pre-Med A", "Assigned Persona": "Expedition Leader", "Q1": "Reorganize tasks..."},
                {"Full Name": "Zainab Ahmed", "Roll No": "102", "Class & Section": "2nd Year Pre-Med B", "Assigned Persona": "Unity Builder", "Q1": "Gather everyone..."},
                {"Full Name": "Fatima Ali", "Roll No": "103", "Class & Section": "1st Year Pre-Eng A", "Assigned Persona": "Logistics Captain", "Q1": "Quickly organize..."},
                {"Full Name": "Maryam Bibi", "Roll No": "104", "Class & Section": "2nd Year Pre-Med A", "Assigned Persona": "Resource Innovator", "Q1": "Find natural trees..."},
                {"Full Name": "Sana Tariq", "Roll No": "105", "Class & Section": "1st Year Pre-Eng A", "Assigned Persona": "Expedition Leader", "Q1": "Reorganize tasks..."}
            ])

        st.subheader("📊 Leadership Persona Distribution")
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            # Pie Chart
            fig_pie = px.pie(
                df, 
                names="Assigned Persona", 
                title="Applicant Persona Breakdown",
                color_discrete_sequence=['#801b38', '#2e1065', '#0284c7', '#059669']
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_g2:
            # Bar Chart by Class
            fig_bar = px.histogram(
                df, 
                x="Class & Section", 
                color="Assigned Persona", 
                title="Applicants by Class & Section",
                barmode="stack",
                color_discrete_sequence=['#801b38', '#2e1065', '#0284c7', '#059669']
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()

        # Question-by-Question Poll Breakdown
        st.subheader("📈 Question Response Analytics")
        selected_q = st.selectbox("Select Assessment Question to View Responses:", [f"Q{i}" for i in range(1, 16)])
        
        if selected_q in df.columns:
            fig_q = px.bar(
                df[selected_q].value_counts().reset_index(),
                x="count",
                y=selected_q,
                orientation='h',
                title=f"Response Breakdown for {selected_q}",
                labels={"count": "Number of Students", selected_q: "Selected Option"},
                color_discrete_sequence=['#801b38']
            )
            st.plotly_chart(fig_q, use_container_width=True)

        st.divider()

        # Registered Data Table
        st.subheader("📄 Registered Applicants Database")
        st.dataframe(df, use_container_width=True)

    elif admin_input:
        st.error("Access Denied: Invalid Security Key")
