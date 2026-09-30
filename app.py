import streamlit as st
import random

# Page Config
st.set_page_config(page_title="E-Governance Portal", page_icon="🏛️", layout="centered")

# App Header
st.title("🏛️ Digital Citizen E-Governance Portal")
st.write("A simple Python-based portal for citizen services, status tracking, and public grievances.")

# Sidebar Navigation
menu = st.sidebar.selectbox("Navigation", ["Home", "Apply for Certificate", "Track Application", "File Grievance"])

# 1. Home Section
if menu == "Home":
    st.subheader("Welcome to Digital Governance")
    st.markdown("""
    ### Services Offered:
    - **Certificates:** Birth, Income, and Caste certificates.
    - **Identity Updates:** Aadhar and PAN card assistance.
    - **Public Grievances:** Quick redressal for civic issues.
    """)

# 2. Apply for Certificate
elif menu == "Apply for Certificate":
    st.subheader("📝 Citizen Certificate Application")
    
    with st.form("cert_form"):
        name = st.text_input("Full Name")
        father_name = st.text_input("Father's / Husband's Name")
        cert_type = st.selectbox("Select Certificate Type", ["Birth Certificate", "Income Certificate", "Caste Certificate"])
        address = st.text_area("Residential Address")
        
        submitted = st.form_submit_button("Submit Application")
        
        if submitted:
            if name and address:
                app_id = f"GOV-{random.randint(10000, 99999)}"
                st.success(f"Application submitted successfully! Your Application ID is: **{app_id}**")
            else:
                st.error("Please fill in all mandatory fields.")

# 3. Track Application Status
elif menu == "Track Application":
    st.subheader("🔍 Track Your Application")
    track_id = st.text_input("Enter Application ID (e.g., GOV12345)")
    
    if st.button("Check Status"):
        if track_id:
            st.info(f"Status for **{track_id}**: Currently under verification by the District Revenue Officer. Expected completion in 3 working days.")
        else:
            st.warning("Please enter a valid Application ID.")

# 4. File Grievance / Complaint
elif menu == "File Grievance":
    st.subheader("📢 Public Grievance Redressal")
    
    with st.form("grievance_form"):
        g_name = st.text_input("Your Name")
        g_contact = st.text_input("Contact Number")
        issue_category = st.selectbox("Category", ["Street Lights", "Water Supply", "Road/Potholes", "Sanitation"])
        g_desc = st.text_area("Describe the Issue")
        
        g_submitted = st.form_submit_button("Lodge Complaint")
        
        if g_submitted:
            if g_name and g_desc:
                ref_id = f"GRV-{random.randint(10000, 99999)}"
                st.success(f"Grievance registered successfully! Reference ID: **{ref_id}**")
            else:
                st.error("Please fill out all required details.")