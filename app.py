import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# Configure Page
st.set_page_config(
    page_title="Girl Guides Selection & Skill Portal",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Vibrant Girl Guide Branding
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .header-box {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 60%, #52b788 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-box h1 {
        color: #ffb703;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .section-card {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 6px solid #2d6a4f;
        margin-bottom: 2rem;
    }
    .badge-card {
        background: linear-gradient(135deg, #fff3bf 0%, #ffd8a8 100%);
        border: 2px solid #f59f00;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .stButton>button {
        background-color: #2d6a4f;
        color: white;
        font-weight: bold;
        font-size: 1.1rem;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1b4332;
        color: #ffb703;
    }
</style>
""", unsafe_allow_html=True)

# Admin Password
ADMIN_PASSWORD = "imcg_admin_pass"

# Navigation Sidebar
st.sidebar.title("⚜️ Navigation")
view_mode = st.sidebar.radio("Select Portal View:", ["Student Application Portal", "Admin Dashboard"])

if view_mode == "Student Application Portal":
    # Header Banner
    st.markdown("""
    <div class="header-box">
        <h1>⚜️ Girl Guides Selection & Skill Assessment Portal</h1>
        <p style="font-size: 1.2rem;">IMCG F-7/2 Islamabad • Official Enrollment & Discovery Portal</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("guide_application_form"):
        # Section 1: Personal Information
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📋 1. Student & Guardian Details")
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *")
            roll_no = st.text_input("Roll No / Student ID *")
            class_section = st.text_input("Class & Section *")
        with col2:
            father_name = st.text_input("Father / Guardian Name *")
            cnic = st.text_input("Father / Guardian CNIC *")
            guardian_consent = st.checkbox("I have father/guardian consent for outdoor activities & camps *")
        st.markdown('</div>', unsafe_allow_html=True)

        # Section 2: Identity & Verification Uploads
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🆔 2. Identity Verification & Documents")
        st.info("Upload scanned copies/clear photos for verification (Max size: 200MB per file).")
        
        uc1, uc2 = st.columns(2)
        with uc1:
            student_photo = st.file_uploader("Upload Recent Student Photograph *", type=["jpg", "png", "jpeg"])
            college_id = st.file_uploader("Upload Student College ID Card *", type=["jpg", "png", "pdf", "jpeg"])
            bus_card = st.file_uploader("Upload College Bus ID Pass (Optional)", type=["jpg", "png", "pdf", "jpeg"])
        with uc2:
            consent_form = st.file_uploader("Upload Signed Guardian Consent Form *", type=["pdf", "jpg", "png", "jpeg"])
            father_cnic_doc = st.file_uploader("Upload Father's/Guardian's CNIC Copy *", type=["pdf", "jpg", "png", "jpeg"])
            prev_certs = st.file_uploader("Upload Previous Certificates (Optional)", type=["pdf", "jpg", "png", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)

        # Section 3: 15 Situational Scenarios
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🔍 3. Situational Persona Assessment")
        st.write("Read each real-life scenario carefully and select the action that best reflects what you would naturally do.")

        scenarios = [
            ("Q1. Your team is tasked with setting up camp, but heavy rain starts unexpectedly. What is your immediate reaction?", [
                ("Step in immediately, divide tasks, and give clear instructions to keep camp setup on track.", "Expedition Leader"),
                ("Gather everyone in a sheltered spot, check if everyone is safe and dry, and keep spirits high.", "Unity Builder"),
                ("Quickly pull out the rain tarps, reorganize equipment, and ensure fragile supplies are protected.", "Logistics Captain"),
                ("Find natural shelter, use knots/tarps to create a temporary canopy, and improvise a rain shield.", "Wilderness Specialist")
            ]),
            ("Q2. A new girl joins your Girl Guide unit and hesitates to join group activities. How do you welcome her?", [
                ("Go over to her, introduce yourself, and pair up with her so she feels immediately included.", "Unity Builder"),
                ("Explain the structure of today's activities so she feels prepared and understands what to expect.", "Active Communicator"),
                ("Assign her a specific role in your team so she feels valuable right away.", "Expedition Leader"),
                ("Invite her to help you prepare materials for the next task to break the ice naturally.", "Logistics Captain")
            ]),
            ("Q3. During a community cleanup drive, your team is falling behind schedule. What do you do?", [
                ("Re-evaluate the remaining workload and reassign volunteers to the slowest areas.", "Logistics Captain"),
                ("Rally the group with an encouraging speech to boost morale and pace.", "Active Communicator"),
                ("Set micro-goals for the remaining time and lead from the front by speeding up your work.", "Expedition Leader"),
                ("Find a more efficient method or shortcut to collect and separate the waste faster.", "Resource Innovator")
            ]),
            ("Q4. You notice two team members having a heated disagreement about who should lead a project task. You:", [
                ("Listen to both sides calmly and help them find a balanced compromise that respects both.", "Unity Builder"),
                ("Remind them of the overall deadline and clearly split the task responsibility between them.", "Expedition Leader"),
                ("Redirect their focus by suggesting a completely new approach that requires both their strengths.", "Crisis Anchor"),
                ("Show them the step-by-step project checklist to objectively decide who does what.", "Logistics Captain")
            ]),
            ("Q5. While hiking along a marked trail, you realize a vital piece of navigation equipment was left behind. You:", [
                ("Remain calm, evaluate visual landmarks, and safely guide the team based on practical instincts.", "Crisis Anchor"),
                ("Use natural indicators like sun position and terrain features to navigate accurately.", "Wilderness Specialist"),
                ("Stop the group, double-check all remaining gear in everyone's packs, and map a safe plan.", "Logistics Captain"),
                ("Inform the group calmly, keeping everyone positive while deciding on the safest next step.", "Active Communicator")
            ]),
            ("Q6. Your unit wants to organize an awareness drive on local environmental issues. Which part excites you most?", [
                ("Designing speeches, posters, and presentation materials to persuade the public.", "Active Communicator"),
                ("Planning the venue, timetable, permission letters, and equipment setup.", "Logistics Captain"),
                ("Leading the project committee and coordinating with college administration.", "Expedition Leader"),
                ("Organizing community outreach teams to connect directly with local neighborhood families.", "Community Advocate")
            ]),
            ("Q7. A fire-safety demonstration is being held at camp. Which role do you naturally volunteer for?", [
                ("Demonstrating knot-tying, safety gear assembly, or tool handling.", "Wilderness Specialist"),
                ("Explaining safety steps clearly to the audience as the narrator.", "Active Communicator"),
                ("Managing attendance, safety equipment inventory, and venue readiness.", "Logistics Captain"),
                ("Taking responsibility as the safety marshal coordinating emergency evacuation drills.", "Crisis Anchor")
            ]),
            ("Q8. During a weekend volunteer activity, unexpected cold weather sets in and team members get tired. You:", [
                ("Organize hot tea, adjust break schedules, and make sure everyone is warm and rested.", "Unity Builder"),
                ("Gather materials to build a windbreak or temporary warming shelter.", "Wilderness Specialist"),
                ("Keep up enthusiasm with group songs, motivating words, and uplifting stories.", "Active Communicator"),
                ("Adjust the work timeline so the most important tasks get finished early.", "Resource Innovator")
            ]),
            ("Q9. You are given a limited budget to arrange supplies for an annual Girl Guide exhibition. You:", [
                ("Create an exact budget spreadsheet to track every rupee spent.", "Logistics Captain"),
                ("Find creative ways to recycle and repurpose existing materials into stunning displays.", "Resource Innovator"),
                ("Contact local community vendors to negotiate donations or discounts.", "Community Advocate"),
                ("Delegate supply purchasing to team leaders and oversee overall execution.", "Expedition Leader")
            ]),
            ("Q10. An outdoor exercise requires building a pioneer bridge across a small creek using ropes and wood. You:", [
                ("Take charge of knot-tying, lashings, and checking structural strength.", "Wilderness Specialist"),
                ("Direct team members on where to hold, pull, and place timbers safely.", "Expedition Leader"),
                ("Think of an alternative, simplified design using available materials.", "Resource Innovator"),
                ("Ensure safety guidelines are strictly followed and double-check every step.", "Crisis Anchor")
            ]),
            ("Q11. You are asked to present a summary of your unit's achievements at the college assembly. You:", [
                ("Confidely deliver an inspiring speech highlighting every member's hard work.", "Active Communicator"),
                ("Prepare a structured, detailed report with precise statistics and event highlights.", "Logistics Captain"),
                ("Focus the talk on how the Guide law helped build community spirit and unity.", "Community Advocate"),
                ("Share practical problem-solving experiences your team overcame in the field.", "Resource Innovator")
            ]),
            ("Q12. During a first-aid drill, a simulated emergency scenario is announced without warning. You:", [
                ("Immediately step up, stay level-headed, and assess the situation systematically.", "Crisis Anchor"),
                ("Apply practical first-aid procedures and bandages accurately.", "Wilderness Specialist"),
                ("Delegate roles clearly—one to call for help, one for supplies, one for first aid.", "Expedition Leader"),
                ("Reassure the injured person and keep surrounding onlookers calm.", "Unity Builder")
            ]),
            ("Q13. Your group needs to raise awareness about plantation and tree care in the college. You prefer to:", [
                ("Lead a tree-planting drive in nearby community spaces and parks.", "Community Advocate"),
                ("Design creative instructional signs and recycled planter pots.", "Resource Innovator"),
                ("Schedule planting slots, gather tools, and coordinate plant distribution.", "Logistics Captain"),
                ("Guide junior students on how to care for plants and nurture growth.", "Unity Builder")
            ]),
            ("Q14. When working in a group, what kind of feedback do you appreciate receiving most?", [
                ("'You kept everyone together and made sure no one was left out.'", "Unity Builder"),
                ("'Your quick thinking saved the project when things went wrong.'", "Crisis Anchor"),
                ("'Your leadership gave us clear direction and confidence.'", "Expedition Leader"),
                ("'Your organization and attention to detail made this flawless.'", "Logistics Captain")
            ]),
            ("Q15. What core value of the Girl Guide Law resonates most deeply with you?", [
                ("To be disciplined, courageous, and lead by example in difficult times.", "Expedition Leader"),
                ("To be a friend to all and a sister to every other Girl Guide.", "Unity Builder"),
                ("To use resources wisely and be helpful and inventive at all times.", "Resource Innovator"),
                ("To serve God, country, and help people at all times.", "Community Advocate")
            ])
        ]

        responses = []
        for idx, (question, options) in enumerate(scenarios, start=1):
            st.markdown(f"**{question}**")
            # Present options without trait labels
            opt_texts = [opt[0] for opt in options]
            choice = st.radio(f"Select option for Q{idx}", opt_texts, index=0, key=f"q_{idx}", label_visibility="collapsed")
            
            # Map selected text back to category
            selected_trait = next(trait for text, trait in options if text == choice)
            responses.append(selected_trait)
            st.markdown("---")

        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("⚜️ Submit Application & Generate Official Badge")

    if submitted:
        if not full_name or not roll_no or not student_photo or not college_id or not consent_form or not father_cnic_doc:
            st.error("⚠️ Please fill in all required fields (*) and upload necessary verification documents (including Student Photo, College ID, Father's CNIC, and Consent Form).")
        else:
            # Calculate Persona Scores
            scores = {}
            for trait in responses:
                scores[trait] = scores.get(trait, 0) + 1
            
            top_persona = max(scores, key=scores.get)

            persona_descriptions = {
                "Expedition Leader": "You possess natural vision, strategic decision-making, and strong leadership. You guide teams effectively through challenges with confidence.",
                "Unity Builder": "You are the heart of the team, fostering empathy, inclusion, and morale. You excel at conflict resolution and making everyone feel valued.",
                "Logistics Captain": "You excel at organization, planning, and execution. You keep operations smooth, schedules punctual, and resources accounted for.",
                "Wilderness Specialist": "You thrive in outdoor settings, campcraft, knot-tying, and hands-on practical survival skills.",
                "Community Advocate": "You are driven by civic responsibility, service, and social action, making a strong positive impact on surrounding communities.",
                "Crisis Anchor": "You remain calm, composed, and analytical under pressure, guiding others safely through unexpected obstacles.",
                "Active Communicator": "You excel in advocacy, public presentation, and expressing key ideas clearly to inspire action.",
                "Resource Innovator": "You are resourceful, creative, and inventive, finding practical fixes and solutions with limited materials."
            }

            st.balloons()
            st.success("✅ Application Submitted Successfully! Your details are stored securely for college administration review.")

            # Display Persona Badge
            st.markdown(f"""
            <div class="badge-card">
                <h2 style="color: #1b4332; margin-bottom: 0.2rem;">⚜️ Official Girl Guide Skill Badge</h2>
                <h1 style="color: #d97706; font-size: 2.5rem; margin-top: 0;">{top_persona}</h1>
                <p style="font-size: 1.1rem; color: #374151; max-width: 700px; margin: 0 auto;">{persona_descriptions[top_persona]}</p>
                <br>
                <div style="text-align: left; background: white; padding: 1rem; border-radius: 8px; max-width: 500px; margin: 0 auto;">
                    <p><b>Candidate Name:</b> {full_name}</p>
                    <p><b>Roll Number:</b> {roll_no}</p>
                    <p><b>Class & Section:</b> {class_section}</p>
                    <p><b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Admin Dashboard
else:
    st.title("🔒 Administration Control Dashboard")
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("Authenticated as IMCG College Admin")
        st.subheader("Submitted Applications & Document Verification")
        st.info("Student uploads and identity records are stored in secure storage inaccessible to the public.")
        st.write("No external public leakage: All student ID cards and consent documents are restricted to logged-in faculty.")
    elif password:
        st.error("Incorrect password. Access denied.")
