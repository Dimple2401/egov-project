import streamlit as st
import random
import time

# Page Config
st.set_page_config(page_title="E-Governance Portal", page_icon="🏛️", layout="wide")

# Custom CSS for Animations & UI Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #ff9933;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e68a00;
        transform: scale(1.02);
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State for Authentication & Database Mock
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "applications" not in st.session_state:
    st.session_state.applications = {
        "GOV-12345": {"name": "Dimple Sanjay Parihar", "type": "Birth Certificate", "status": "Approved & Verified"},
        "GOV-98765": {"name": "Rahul Sharma", "type": "Income Certificate", "status": "Under District Officer Verification"},
    }
if "grievances" not in st.session_state:
    st.session_state.grievances = {
        "GRV-11111": {"name": "Dimple Sanjay Parihar", "category": "Street Lights", "status": "In Progress"}
    }

# App Header
st.markdown("<h1 style='text-align: center; color: #1f4e78;'>🏛️ Digital Citizen E-Governance Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Secure, Transparent, and Fast Public Services</p>", unsafe_allow_html=True)
st.divider()

# Authentication Sidebar / Login Gate
st.sidebar.markdown("### 🔐 Citizen Portal Login")
if not st.session_state.logged_in:
    with st.sidebar.form("login_form"):
        entered_id = st.text_input("Citizen ID / Login Number", placeholder="e.g. CITIZEN-01")
        entered_pass = st.text_input("Access PIN / Password", type="password", placeholder="e.g. 1234")
        login_btn = st.form_submit_button("Login to Portal")
        
        if login_btn:
            # Validating specific IDs
            valid_users = {"CITIZEN-01": "1234", "CITIZEN-02": "5678", "ADMIN": "admin123"}
            if entered_id in valid_users and valid_users[entered_id] == entered_pass:
                st.session_state.logged_in = True
                st.session_state.user_id = entered_id
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("❌ Invalid Citizen ID or PIN! (Try ID: CITIZEN-01, PIN: 1234)")
    
    st.sidebar.info("💡 **Demo Login Credentials:**\n- ID: `CITIZEN-01` | PIN: `1234`")
    menu = "Home"
else:
    st.sidebar.success(f"Logged in as: **{st.session_state.user_id}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.rerun()
    
    # Sidebar Navigation after login
    menu = st.sidebar.radio("Navigation", ["Home", "Apply for Certificate", "Track Application", "File Grievance", "My Dashboard"])

# 1. Home Section
if menu == "Home":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Services", value="12+", delta="2 New")
    with col2:
        st.metric(label="Processed Applications", value="1,482", delta="+12 today")
    with col3:
        st.metric(label="Grievance Resolution", value="98.4%", delta="+0.5%")
    
    st.subheader("Welcome to Digital Governance")
    st.markdown("""
    <div class='card'>
    <h3>🌟 Key Services Offered:</h3>
    <ul>
        <li><b>Certificates:</b> Instant application for Birth, Income, and Caste certificates.</li>
        <li><b>Identity Updates:</b> Seamless Aadhar and PAN card linkage support.</li>
        <li><b>Public Grievances:</b> Quick redressal tracking for civic infrastructure issues.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        st.warning("⚠️ Please log in using the sidebar (Demo ID: `CITIZEN-01`, PIN: `1234`) to access application forms and tracking features.")

# 2. Apply for Certificate
elif menu == "Apply for Certificate":
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login first from the sidebar to submit applications.")
    else:
        st.subheader("📝 Citizen Certificate Application Portal")
        st.write("Fill out the official form below. All entries are verified against official records.")
        
        with st.form("cert_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name (as per ID)")
                father_name = st.text_input("Father's / Husband's Name")
            with col2:
                mobile = st.text_input("Mobile Number", placeholder="10-digit number")
                cert_type = st.selectbox("Select Certificate Type", ["Birth Certificate", "Income Certificate", "Caste Certificate", "Domicile Certificate"])
            
            address = st.text_area("Residential Address")
            declaration = st.checkbox("I hereby declare that the information provided is true and correct.")
            
            submitted = st.form_submit_button("Submit Application")
            
            if submitted:
                if not name or not address or not mobile:
                    st.error("❌ Please fill in all mandatory fields (Name, Mobile, Address).")
                elif not declaration:
                    st.error("❌ You must accept the declaration checkbox before submitting.")
                elif len(mobile) != 10 or not mobile.isdigit():
                    st.error("❌ Please enter a valid 10-digit mobile number.")
                else:
                    with st.spinner("Encrypting and submitting to server..."):
                        time.sleep(1.5)
                    app_id = f"GOV-{random.randint(10000, 99999)}"
                    st.session_state.applications[app_id] = {
                        "name": name,
                        "type": cert_type,
                        "status": "Pending Verification"
                    }
                    st.balloons()
                    st.success(f"🎉 Application submitted successfully! Your Application ID is: **{app_id}**")
                    st.info("Save this ID to track your application status.")
                    
                    # Download Receipt Button
                    receipt_text = f"E-GOVERNANCE PORTAL RECEIPT\nApplication ID: {app_id}\nName: {name}\nType: {cert_type}\nStatus: Pending Verification"
                    st.download_button("📥 Download Official Receipt", receipt_text, file_name=f"{app_id}_receipt.txt")

# 3. Track Application Status
elif menu == "Track Application":
    st.subheader("🔍 Track Your Application Status")
    st.write("Enter your registered Application ID (e.g., `GOV-12345` or a newly generated one).")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        track_id = st.text_input("Application ID", placeholder="GOV-XXXXX")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        check_btn = st.button("Check Status")
    
    if check_btn:
        if not track_id:
            st.warning("⚠️️ Please enter an Application ID.")
        else:
            with st.spinner("Searching government database..."):
                time.sleep(1)
            
            # Validating if ID exists in system records
            if track_id in st.session_state.applications:
                app_info = st.session_state.applications[track_id]
                st.success(f"✅ Record Found for **{track_id}**")
                st.markdown(f"""
                <div class='card'>
                <h4>Application Details:</h4>
                <p><b>Applicant Name:</b> {app_info['name']}</p>
                <p><b>Service Type:</b> {app_info['type']}</p>
                <p><b>Current Status:</b> <span style='color: green; font-weight: bold;'>{app_info['status']}</span></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ **Invalid Application ID:** `{track_id}` was not found in the e-governance database. Please verify your ID or try the demo ID: `GOV-12345`.")

# 4. File Grievance / Complaint
elif menu == "File Grievance":
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login first from the sidebar to lodge grievances.")
    else:
        st.subheader("📢 Public Grievance Redressal Portal")
        st.write("Report civic issues (potholes, water supply, street lights) directly to municipal authorities.")
        
        with st.form("grievance_form"):
            col1, col2 = st.columns(2)
            with col1:
                g_name = st.text_input("Your Name")
                g_contact = st.text_input("Contact Number")
            with col2:
                issue_category = st.selectbox("Category", ["Street Lights", "Water Supply", "Road/Potholes", "Sanitation", "Garbage Collection"])
                location = st.text_input("Area / Landmark")
            
            g_desc = st.text_area("Describe the Issue in Detail")
            
            g_submitted = st.form_submit_button("Lodge Complaint")
            
            if g_submitted:
                if not g_name or not g_desc or not g_contact:
                    st.error("❌ Please fill out all required details (Name, Contact, Description).")
                elif len(g_contact) != 10 or not g_contact.isdigit():
                    st.error("❌ Please enter a valid 10-digit contact number.")
                else:
                    with st.spinner("Submitting complaint ticket..."):
                        time.sleep(1)
                    ref_id = f"GRV-{random.randint(10000, 99999)}"
                    st.session_state.grievances[ref_id] = {
                        "name": g_name,
                        "category": issue_category,
                        "status": "Registered & Assigned to Officer"
                    }
                    st.snow()
                    st.success(f"✅ Grievance registered successfully! Reference ID: **{ref_id}**")
                    st.info("You can track this complaint using your Reference ID.")

# 5. My Dashboard
elif menu == "My Dashboard":
    st.subheader(f"📊 Dashboard for User: {st.session_state.user_id}")
    st.markdown("Here is the summary of all activities linked with your account:")
    
    st.markdown("### 📝 Your Submitted Applications")
    if st.session_state.applications:
        for aid, info in st.session_state.applications.items():
            st.markdown(f"- **{aid}**: {info['type']} ({info['name']}) — Status: *{info['status']}*")
    else:
        st.info("No applications submitted yet.")
        
    st.markdown("### 📢 Your Filed Grievances")
    if st.session_state.grievances:
        for gid, ginfo in st.session_state.grievances.items():
            st.markdown(f"- **{gid}**: {ginfo['category']} — Status: *{ginfo['status']}*")
    else:
        st.info("No grievances filed yet.")
    
    if st.button("🔄 Reset / Clear Session Data"):
        st.session_state.applications = {}
        st.session_state.grievances = {}
        st.success("Session data cleared successfully!")
        st.rerun()
