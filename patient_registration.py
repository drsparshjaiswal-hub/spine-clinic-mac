import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Spine Clinic Registration", page_icon="🩺", layout="wide")

# Beautiful Medical CSS
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #f0f8fc 0%, #e3f2fd 100%)}
.stTextInput > div > div > input, .stNumberInput > div > div > input {border-radius: 12px; border: 2px solid #4CAF50}
.stTextArea > div > div > textarea {border-radius: 12px; border: 2px solid #4CAF50}
h1 {color: #2E7D32 !important; font-size: 3rem !important}
.success-box {background: #E8F5E8; padding: 20px; border-radius: 15px; border-left: 6px solid #4CAF50}
</style>
""", unsafe_allow_html=True)

# CSV Backend Setup
if not os.path.exists("patients.csv"):
    df = pd.DataFrame(columns=[
        "ID", "Name", "Age", "Sex", "Place", "Phone_No", "Alternate_Phone", 
        "Relative", "Category", "Reports_MRI", "Reports_CT", "Reports_Xray", 
        "Reports_Blood", "Reports_Other", "Lab_Name", "Old_Disease_DM", 
        "Old_Disease_HTN", "Old_Disease_Cardiac", "Old_Disease_Other",
        "Pain_Score", "Severity_Points", "Risk_Points", "Total_Points", 
        "Notes", "Date_Registered"
    ])
    df.to_csv("patients.csv", index=False)

st.title("🩺 Spine Clinic Registration")

# ✅ FIXED: ALL INPUTS + SUBMIT INSIDE ONE FORM
with st.form("complete_patient_form", clear_on_submit=True):
    st.markdown("---")
    
    # Row 1: Basic Info
    col1, col2, col3, col4 = st.columns(4)
    name = col1.text_input("**Name** *")
    age = col2.number_input("**Age**", min_value=1, max_value=120)
    sex = col3.selectbox("**Sex**", ["Male", "Female", "Other"])
    place = col4.text_input("**Place**")
    
    # Row 2: Contact
    col1, col2, col3 = st.columns(3)
    phone_no = col1.text_input("**Phone** *")
    alternate_phone = col2.text_input("Alternate Phone")
    relative = col3.text_input("Relative/Emergency")
    
    # Row 3: Medical
    col1, col2 = st.columns(2)
    category = col1.selectbox("**Category**", ["1. Surgery", "2. Injection", "3. Follow Up", "4. Others"])
    
    col1, col2, col3, col4 = st.columns(4)
    reports_mri = col1.checkbox("MRI")
    reports_ct = col2.checkbox("CT")
    reports_xray = col3.checkbox("X-ray") 
    reports_blood = col4.checkbox("Blood")
    
    # Row 4: Reports + Lab
    reports_other = st.text_input("Other Reports")
    lab_name = st.text_input("Lab Name")
    
    # Row 5: Medical History
    col1, col2, col3, col4 = st.columns(4)
    old_dm = col1.checkbox("Diabetes")
    old_htn = col2.checkbox("HTN") 
    old_cardiac = col3.checkbox("Cardiac")
    old_disease_other = col4.text_input("Other Disease")
    
    # Row 6: Notes
    notes = st.text_area("**Doctor Notes**", height=80, 
                        placeholder="Clinical findings, treatment plan, follow-up instructions...")
    
    # Row 7: Pain Scoring
    col1, col2, col3 = st.columns(3)
    pain_score = col1.slider("Pain (0-10)", 0, 10, 0)
    severity = col2.slider("Severity (0-10)", 0, 10, 0)
    risk = col3.slider("Risk (0-10)", 0, 10, 0)
    
    # ✅ SUBMIT BUTTON INSIDE FORM - THIS WORKS!
    submitted = st.form_submit_button("✅ REGISTER PATIENT", 
                                     use_container_width=True,
                                     type="primary")
    
    # Calculate total
    total_points = pain_score + severity + risk

# ✅ PROCESS SUBMISSION (runs when button clicked)
if submitted and name and phone_no:
    df = pd.read_csv("patients.csv")
    new_id = len(df) + 1
    
    new_patient = pd.DataFrame({
        "ID": [new_id], "Name": [name], "Age": [age], "Sex": [sex], 
        "Place": [place], "Phone_No": [phone_no], "Alternate_Phone": [alternate_phone],
        "Relative": [relative], "Category": [category],
        "Reports_MRI": [reports_mri], "Reports_CT": [reports_ct], 
        "Reports_Xray": [reports_xray], "Reports_Blood": [reports_blood],
        "Reports_Other": [reports_other], "Lab_Name": [lab_name],
        "Old_Disease_DM": [old_dm], "Old_Disease_HTN": [old_htn],
        "Old_Disease_Cardiac": [old_cardiac], "Old_Disease_Other": [old_disease_other],
        "Pain_Score": [pain_score], "Severity_Points": [severity],
        "Risk_Points": [risk], "Total_Points": [total_points],
        "Notes": [notes], "Date_Registered": [datetime.now().strftime("%Y-%m-%d %H:%M")]
    })
    
    # ✅ SAVES TO CSV BACKEND
    new_patient.to_csv("patients.csv", mode='a', header=False, index=False)
    
    st.success(f"🎉 **{name}** registered! ID: #{new_id}")
    st.balloons()

elif submitted:
    st.error("❌ Fill **Name** and **Phone**")

# Live Dashboard
st.markdown("---")
st.subheader("📊 All Patients")

try:
    df = pd.read_csv("patients.csv")
    st.dataframe(df, use_container_width=True, height=400)
    
    # CSV Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, "patients.csv", use_container_width=True)
    
except:
    st.info("👆 Register first patient to see dashboard")

st.caption("🩺 Spine Clinic System | 🔒 Data saved to patients.csv")
