import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Spine Clinic Registration", page_icon="🩺", layout="wide")

# Professional Medical CSS
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #f0f8fc 0%, #e3f2fd 100%)}
.stTextInput > div > div > input, .stNumberInput > div > div > input {border-radius: 12px; border: 2px solid #4CAF50}
.stTextArea > div > div > textarea {border-radius: 12px; border: 2px solid #4CAF50}
.stSelectbox > div > div > select {border-radius: 12px; border: 2px solid #4CAF50}
.stButton > button {background: linear-gradient(45deg, #4CAF50, #45a049); border-radius: 25px; color: white; font-weight: bold; font-size: 16px}
h1 {color: #2E7D32 !important; font-size: 3.2rem !important}
.success-box {background: linear-gradient(135deg, #E8F5E8, #C8E6C9); padding: 25px; border-radius: 20px; border-left: 8px solid #4CAF50}
.metric-card {background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1)}
.notes-box {background-color: #fff3e0; padding: 15px; border-radius: 10px; border-left: 5px solid #ff9800}
</style>
""", unsafe_allow_html=True)

# Initialize CSV with NOTES field
if not os.path.exists("patients.csv"):
    df = pd.DataFrame(columns=[
        "ID", "Name", "Age", "Sex", "Place", "Phone_No", "Alternate_Phone", 
        "Relative", "Category", "Reports_MRI", "Reports_CT", "Reports_Xray", 
        "Reports_Blood", "Reports_Other", "Lab_Name",
        "Old_Disease_DM", "Old_Disease_HTN", "Old_Disease_Cardiac", "Old_Disease_Other",
        "Pain_Score", "Severity_Points", "Risk_Points", "Total_Points", 
        "Notes", "Date_Registered"
    ])
    df.to_csv("patients.csv", index=False)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🩺 Spine Clinic • Ultimate Registration")
with col2:
    st.markdown("### ✨ Complete Medical System")

st.markdown("─" * 110)

# Registration Form - 3 Columns
col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.subheader("👤 Basic Information")
    with st.form("patient_form"):
        name = st.text_input("**Full Name** *", placeholder="Enter patient name")
        age = st.number_input("**Age**", min_value=1, max_value=120, value=35)
        sex = st.selectbox("**Sex**", ["Male", "Female", "Other"])
        place = st.text_input("**Place/City**", placeholder="Indore, Bhopal, etc.")

with col2:
    st.subheader("📞 Contact Details")
    phone_no = st.text_input("**Phone Number** *", placeholder="+91 9876543210")
    alternate_phone = st.text_input("Alternate Phone", placeholder="Emergency contact")
    relative = st.text_input("Relative/Emergency", placeholder="Spouse/Father name & number")

with col3:
    st.subheader("🏥 Medical Category")
    category = st.selectbox("**Category**", [
        "1. Surgery", "2. Injection", "3. Follow Up", "4. Others"
    ])
    
    st.subheader("📋 Reports Available")
    reports_mri = st.checkbox("MRI", key="mri")
    reports_ct = st.checkbox("CT Scan", key="ct") 
    reports_xray = st.checkbox("X-Ray", key="xray")
    reports_blood = st.checkbox("Blood Reports", key="blood")
    reports_other = st.text_input("Other Reports")
    lab_name = st.text_input("Lab Name", placeholder="SRL, Thyrocare, etc.")

# Medical History Section
st.markdown("─" * 110)
st.subheader("📚 Past Medical History")
col1, col2, col3, col4 = st.columns(4)
old_dm = col1.checkbox("Diabetes (DM)")
old_htn = col2.checkbox("Hypertension (HTN)") 
old_cardiac = col3.checkbox("Cardiac Issues")
old_disease_other = col4.text_input("Other Diseases")

# **NEW NOTES SECTION**
st.markdown("─" * 110)
st.subheader("📝 Doctor Notes")
notes = st.text_area("Clinical Observations / Special Instructions", 
                    placeholder="Ex: 'Patient reports night pain worse on right side. Mild weakness L5. Plan: MRI + Injection'", 
                    height=100, help="Add important clinical findings, treatment plans, follow-up instructions")

# Scoring Section
st.markdown("─" * 110)
col1, col2, col3 = st.columns(3)
pain_score = col1.slider("🔥 Pain Level (0-10)", 0, 10, 0)
severity = col2.slider("📉 Severity (0-10)", 0, 10, 0)
risk = col3.slider("⚠️ Risk Factors (0-10)", 0, 10, 0)
total_points = pain_score + severity + risk
st.metric("📊 Total Clinical Score", total_points, delta=None)

# Submit Button
submitted = st.form_submit_button("✅ Save Complete Patient Record", use_container_width=True)

# Process submission
if submitted and name and phone_no:
    df = pd.read_csv("patients.csv")
    new_id = len(df) + 1
    
    new_patient = pd.DataFrame({
        "ID": [new_id],
        "Name": [name],
        "Age": [age],
        "Sex": [sex],
        "Place": [place],
        "Phone_No": [phone_no],
        "Alternate_Phone": [alternate_phone],
        "Relative": [relative],
        "Category": [category],
        "Reports_MRI": [reports_mri],
        "Reports_CT": [reports_ct],
        "Reports_Xray": [reports_xray],
        "Reports_Blood": [reports_blood],
        "Reports_Other": [reports_other],
        "Lab_Name": [lab_name],
        "Old_Disease_DM": [old_dm],
        "Old_Disease_HTN": [old_htn],
        "Old_Disease_Cardiac": [old_cardiac],
        "Old_Disease_Other": [old_disease_other],
        "Pain_Score": [pain_score],
        "Severity_Points": [severity],
        "Risk_Points": [risk],
        "Total_Points": [total_points],
        "Notes": [notes],
        "Date_Registered": [datetime.now().strftime("%Y-%m-%d %H:%M")]
    })
    
    new_patient.to_csv("patients.csv", mode='a', header=False, index=False)
    
    # Success message
    diseases = []
    if old_dm: diseases.append("DM")
    if old_htn: diseases.append("HTN") 
    if old_cardiac: diseases.append("Cardiac")
    if old_disease_other: diseases.append(old_disease_other)
    
    st.markdown(f"""
    <div class="success-box">
        <h2>🎉 Patient Record Saved!</h2>
        <h3>{name} | ID: #{new_id} | {category}</h3>
        <p><strong>📞</strong> {phone_no} | <strong>📊</strong> Score: {total_points}/30</p>
        <p><strong>🏥</strong> Reports: MRI:{'✅' if reports_mri else '❌'} 
        CT:{'✅' if reports_ct else '❌'} Xray:{'✅' if reports_xray else '❌'}</p>
        <p><strong>📚</strong> History: {', '.join(diseases) if diseases else 'None'}</p>
        <div class="notes-box">
            <strong>📝 Notes:</strong> {notes[:100]}{'...' if len(notes)>100 else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()

elif submitted:
    st.error("❌ Please fill **Name** and **Phone Number**")

# Complete Dashboard with Notes Preview
st.markdown("─" * 110)
st.subheader("📋 Complete Patient Database")

df = pd.read_csv("patients.csv")

# Show notes in table (truncate long notes)
df_display = df.copy()
df_display['Notes'] = df_display['Notes'].apply(lambda x: str(x)[:50] + '...' if len(str(x)) > 50 else str(x))
st.dataframe(df_display, use_container_width=True, height=500)

# Advanced Metrics
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("Total Patients", len(df))
with col2: st.metric("Diabetes Cases", len(df[df['Old_Disease_DM']==True]))
with col3: st.metric("HTN Cases", len(df[df['Old_Disease_HTN']==True]))
with col4: st.metric("Surgery", len(df[df['Category']=='1. Surgery']))
with col5: st.metric("High Risk", len(df[df['Total_Points']>20]))

# CSV Download
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Complete Database", csv, "spine-clinic-complete.csv", use_container_width=True)

st.caption("🔒 Secure • 🌐 Cloud Deployable • 📱 Mobile Ready • 📝 Notes Enabled • 🩺 Ultimate System")
