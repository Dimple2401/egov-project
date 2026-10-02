import streamlit as st
import random
import time

# Page Config
st.set_page_config(page_title="E-Governance Portal", page_icon="🏛️", layout="wide")

# Custom CSS for High Contrast UI, Government Aesthetic & Animations
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
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
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        color: #2c3e50 !important;
    }
    .card h3, .card h4, .card p, .card li {
        color: #2c3e50 !important;
    }
    /* Official Government Certificate Box Style */
    .certificate-box {
        border: 5px double #1f4e78;
        padding: 30px;
        border-radius: 15px;
        background-color: #fffdf9;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        color: #1a1a1a;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper Function for Glowing Falling Stars Effect (Replacing Snow Animation)
def glowing_falling_stars():
    st.markdown("""
        <style>
        @keyframes fallStar {
            0% { transform: translateY(-10px) translateX(0); opacity: 1; filter: drop-shadow(0 0 6px #ffD700); }
            100% { transform: translateY(80vh) translateX(50px); opacity: 0; filter: drop-shadow(0 0 12px #ff9933); }
        }
        .glowing-star {
            position: fixed;
            width: 6px;
            height: 6px;
            background: #fff;
            box-shadow: 0 0 10px #ffD700, 0 0 20px #ff9933, 0 0 30px #ffcc00;
            animation: fallStar 2.5s linear infinite;
            z-index: 99999;
            border-radius: 50%;
        }
        </style>
        <div style="position:fixed;top:10vh;left:0;width:100vw;height:70vh;pointer-events:none;overflow:hidden;z-index:99998;">
            <div class="glowing-star" style="left: 10%; animation-duration: 2.1s; animation-delay: 0.1s;"></div>
            <div class="glowing-star" style="left: 25%; animation-duration: 2.6s; animation-delay: 0.4s;"></div>
            <div class="glowing-star" style="left: 40%; animation-duration: 1.8s; animation-delay: 0.2s;"></div>
            <div class="glowing-star" style="left: 55%; animation-duration: 2.3s; animation-delay: 0.5s;"></div>
            <div class="glowing-star" style="left: 70%; animation-duration: 2.0s; animation-delay: 0.15s;"></div>
            <div class="glowing-star" style="left: 85%; animation-duration: 2.4s; animation-delay: 0.3s;"></div>
            <div class="glowing-star" style="left: 15%; animation-duration: 1.9s; animation-delay: 0.6s;"></div>
            <div class="glowing-star" style="left: 50%; animation-duration: 2.2s; animation-delay: 0.25s;"></div>
            <div class="glowing-star" style="left: 80%; animation-duration: 2.5s; animation-delay: 0.45s;"></div>
        </div>
    """, unsafe_allow_html=True)

# Initialize Session State for Database Mock & User Data
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None
if "last_app_id" not in st.session_state:
    st.session_state.last_app_id = None
if "applications" not in st.session_state:
    st.session_state.applications = {
        "GOV-12345": {"name": "Dimple Sanjay Parihar", "type": "Birth Certificate", "status": "Approved & Verified", "address": "Pune, Maharashtra"},
        "GOV-98765": {"name": "Rahul Sharma", "type": "Income Certificate", "status": "Under District Officer Verification", "address": "Mumbai, Maharashtra"},
    }
if "grievances" not in st.session_state:
    st.session_state.grievances = {
        "GRV-11111": {"name": "Dimple Sanjay Parihar", "contact": "9876543210", "category": "Street Lights", "desc": "Non-working street light near main square.", "status": "In Progress (Assigned to Municipal Engineer)"}
    }

# App Header
st.markdown("<h1 style='text-align: center; color: #1f4e78;'>🏛️ Digital Citizen E-Governance Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555555; font-weight: bold;'>Secure, Transparent, and Fast Public Services</p>", unsafe_allow_html=True)
st.divider()

# Authentication Sidebar / Login Gate
st.sidebar.markdown("### 🔐 Citizen Portal Login")
if not st.session_state.logged_in:
    with st.sidebar.form("login_form"):
        entered_id = st.text_input("Citizen ID / Login Number", placeholder="e.g. CITIZEN-01")
        entered_pass = st.text_input("Access PIN / Password", type="password", placeholder="e.g. 1234")
        login_btn = st.form_submit_button("Login to Portal")
        
        if login_btn:
            valid_users = {"CITIZEN-01": "1234", "CITIZEN-02": "5678", "ADMIN": "admin123"}
            if entered_id in valid_users and valid_users[entered_id] == entered_pass:
                st.session_state.logged_in = True
                st.session_state.user_id = entered_id
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("❌ Invalid ID or PIN! (Try ID: CITIZEN-01, PIN: 1234)")
    
    st.sidebar.info("💡 **Demo Login Credentials:**\n- ID: `CITIZEN-01` | PIN: `1234`")
    menu = "Home"
else:
    st.sidebar.success(f"Logged in as: **{st.session_state.user_id}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.session_state.last_receipt = None
        st.session_state.last_app_id = None
        st.rerun()
    
    menu = st.sidebar.radio("Navigation", ["Home", "Apply for Certificate", "Track Application", "Download Certificates", "File Grievance", "My Dashboard"])

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
        <li><b>Certificates:</b> Instant application and digital issuance for Birth, Income, and Caste certificates.</li>
        <li><b>Identity Updates:</b> Seamless Aadhar and PAN card linkage support.</li>
        <li><b>Public Grievances:</b> Quick redressal tracking for civic infrastructure issues.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        st.warning("⚠️ Please log in using the sidebar (Demo ID: `CITIZEN-01`, PIN: `1234`) to access application forms and tracking features.")

# 2. Apply for Certificate (Triggers Native Balloons)
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
                    app_id = f"GOV-{random.randint(10000, 99999)}"
                    st.session_state.applications[app_id] = {
                        "name": name,
                        "type": cert_type,
                        "status": "Approved & Verified",
                        "address": address
                    }
                    st.session_state.last_app_id = app_id
                    st.session_state.last_receipt = f"E-GOVERNANCE PORTAL RECEIPT\nApplication ID: {app_id}\nName: {name}\nType: {cert_type}\nStatus: Approved & Verified"
        
        if st.session_state.last_receipt and st.session_state.last_app_id:
            st.balloons()  # Preserved native balloon animation here
            st.success(f"🎉 Application approved successfully! Your Application ID is: **{st.session_state.last_app_id}**")
            st.download_button("📥 Download Official Receipt", st.session_state.last_receipt, file_name=f"{st.session_state.last_app_id}_receipt.txt")

# 3. Track Application Status
elif menu == "Track Application":
    st.subheader("🔍 Universal Status Tracker")
    st.write("Enter either your **Certificate Application ID** (e.g., `GOV-12345`) or **Grievance Reference ID** (e.g., `GRV-11111`).")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_id = st.text_input("Enter Tracking / Reference ID", placeholder="GOV-XXXXX or GRV-XXXXX")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        check_btn = st.button("Check Status")
    
    if check_btn:
        if not search_id:
            st.warning("⚠ Please enter a valid ID.")
        else:
            if search_id in st.session_state.applications:
                app_info = st.session_state.applications[search_id]
                st.success(f"✅ Certificate Record Found for **{search_id}**")
                st.markdown(f"""
                <div class='card'>
                <h4>Certificate Application Details:</h4>
                <p><b>Applicant Name:</b> {app_info['name']}</p>
                <p><b>Service Type:</b> {app_info['type']}</p>
                <p><b>Current Status:</b> <span style='color: #27ae60; font-weight: bold;'>{app_info['status']}</span></p>
                </div>
                """, unsafe_allow_html=True)
            elif search_id in st.session_state.grievances:
                g_info = st.session_state.grievances[search_id]
                st.success(f"✅ Grievance Record Found for **{search_id}**")
                st.markdown(f"""
                <div class='card'>
                <h4>Grievance Ticket Details:</h4>
                <p><b>Complainant Name:</b> {g_info['name']}</p>
                <p><b>Issue Category:</b> {g_info['category']}</p>
                <p><b>Description:</b> {g_info['desc']}</p>
                <p><b>Current Status:</b> <span style='color: #d35400; font-weight: bold;'>{g_info['status']}</span></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ **Invalid ID:** `{search_id}` was not found in the e-governance database. Please verify your ID.")

# 4. Download Digital Certificates (Triggers Stars replacing Snow)
elif menu == "Download Certificates":
    st.subheader("📜 Official Digital Certificate Issuance")
    st.write("Enter your verified Application ID (e.g., `GOV-12345`) to view and download your government-issued digital certificate.")
    
    cert_search = st.text_input("Enter Approved Application ID", placeholder="GOV-XXXXX")
    
    if st.button("Generate & View Certificate"):
        if not cert_search:
            st.warning("⚠️ Please enter an Application ID.")
        elif cert_search in st.session_state.applications:
            app_data = st.session_state.applications[cert_search]
            if "Approved" in app_data['status']:
                glowing_falling_stars()  # Custom stars animation replacing snow here
                st.success("✅ Certificate verified successfully!")
                
                cert_html = f"""
                <div class="certificate-box">
                    <div style="text-align: center;">
                        <h3><b>GOVERNMENT OF INDIA / STATE ADMINISTRATION</b></h3>
                        <h4><b>Department of Civil Services & Revenue</b></h4>
                        <hr style="border: 1px solid #1f4e78;">
                        <h2 style="color: #b8860b; margin-top: 15px;">🌟 CERTIFICATE OF {app_data['type'].upper()} 🌟</h2>
                        <p style="font-size: 14px; color: gray;">[Issued under the Digital Citizen E-Governance Act]</p>
                    </div>
                    <br>
                    <p style="font-size: 16px; line-height: 1.8;">
                        This is to certify that <b>{app_data['name']}</b>, resident of <b>{app_data.get('address', 'Registered District')}</b>, has been duly verified and registered under our database for the issuance of <b>{app_data['type']}</b>.
                    </p>
                    <br>
                    <table style="width: 100%; font-size: 14px; margin-top: 20px;">
                        <tr>
                            <td><b>Certificate ID:</b> CERT-{cert_search}</td>
                            <td style="text-align: right;"><b>Issue Date:</b> October 2, 2026</td>
                        </tr>
                        <tr>
                            <td><b>Verification Status:</b> <span style="color: green;">AUTHENTIC & VALID</span></td>
                            <td style="text-align: right;"><b>Authorized Signatory:</b> District Revenue Officer ✒️</td>
                        </tr>
                    </table>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
                
                cert_file_text = f"--- GOVERNMENT OF INDIA DIGITAL CERTIFICATE ---\nType: {app_data['type']}\nID: CERT-{cert_search}\nName: {app_data['name']}\nStatus: Authentic & Verified\nDate: 2026-10-02"
                st.download_button("📥 Download Official Digital Certificate (TXT/PDF)", cert_file_text, file_name=f"{cert_search}_Certificate.txt")
            else:
                st.warning(f"⚠️ Application `{cert_search}` is still pending verification. Certificates can only be downloaded once approved.")
        else:
            st.error(f"❌ Invalid Application ID `{cert_search}`. Try using the demo ID: `GOV-12345`.")

# 5. File Grievance / Complaint
elif menu == "File Grievance":
    if not st.session_state.logged_in:
        st.warning("⚠️ Please login first from the sidebar to lodge grievances.")
    else:
        st.subheader("📢 Public Grievance Redressal Portal")
        st.write("Report civic issues (potholes, water supply, street lights) directly to municipal authorities. Data is saved securely.")
        
        with st.form("grievance_form"):
            col1, col2 = st.columns(2)
            with col1:
                g_name = st.text_input("Your Name")
                g_contact = st.text_input("Contact Number", placeholder="10-digit number")
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
                    ref_id = f"GRV-{random.randint(10000, 99999)}"
                    st.session_state.grievances[ref_id] = {
                        "name": g_name,
                        "contact": g_contact,
                        "category": issue_category,
                        "desc": g_desc,
                        "status": "Registered & Forwarded to Department"
                    }
                    st.success(f"✅ Grievance registered and saved successfully! Reference ID: **{ref_id}**")
                    st.info("You can use this Reference ID anytime in the tracking section.")

# 6. My Dashboard
elif menu == "My Dashboard":
    st.subheader(f"📊 Dashboard for User: {st.session_state.user_id}")
    st.markdown("Here is the summary of all applications and filed complaints linked with your session:")
    
    st.markdown("### 📝 Your Submitted Applications")
    if st.session_state.applications:
        for aid, info in st.session_state.applications.items():
            st.markdown(f"- **{aid}**: {info['type']} ({info['name']}) — Status: *{info['status']}*")
    else:
        st.info("No applications submitted yet.")
        
    st.markdown("### 📢 Your Filed Grievances & Complaints")
    if st.session_state.grievances:
        for gid, ginfo in st.session_state.grievances.items():
            st.markdown(f"- **{gid}** [{ginfo['category']}]: {ginfo['desc']} — Status: *{ginfo['status']}*")
    else:
        st.info("No grievances filed yet.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset / Clear Session Data"):
        st.session_state.applications = {}
        st.session_state.grievances = {}
        st.session_state.last_receipt = None
        st.session_state.last_app_id = None
        st.success("Session data cleared successfully!")
        st.rerun()
