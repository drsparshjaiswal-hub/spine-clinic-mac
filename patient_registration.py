import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Spine Clinic", page_icon="🩺", layout="wide")

# Medical CSS
st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] {gap: 10px;}
.stTabs [data-baseweb="tab"] {
    background-color: #4CAF50; color: white; border-radius: 10px; 
    padding: 10px 20px; font-weight: bold;
}
.stTextInput > div > div > input {border-radius: 12px; border: 2px solid #4CAF50}
h1 {color: #2E7D32 !important; font-size: 2.5rem !important}
</style>
""", unsafe_allow_html=True)

# CSV Backend with PAYMENT fields
if not os.path.exists("patients.csv"):
    df = pd.DataFrame(columns=[
        "ID", "Name", "Age", "Sex", "Place", "Phone_No", "Alternate_Phone", 
        "Relative", "Category", "Reports_MRI", "Reports_CT", "Reports_Xray", 
        "Reports_Blood", "Reports_Other", "Lab_Name", "Old_Disease_DM", 
        "Old_Disease_HTN", "Old_Disease_Cardiac", "Old_Disease_Other",
        "Payment_Amount", "Payment_Mode_Cash", "Payment_Mode_QR", 
        "Paid_To_Vishnu", "Payment_Notes", "Clinical_Notes", 
        "Pain_Score", "Severity_Points", "Risk_Points", "Total_Points", 
        "Date_Registered"
    ])
    df.to_csv("patients.csv", index=False)

# Header
st.title("🩺 Spine Clinic Management System")
st.markdown("---")

# TABS: Registration | View CSV
tab1, tab2 = st.tabs(["📝 Patient Registration", "📊 View CSV & Download"])

with tab1:
    with st.form("patient_form", clear_on_submit=True):
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
        relative = col3.text_input("Relative")
        
        # Row 3: Medical Category + Reports
        col1, col2 = st.columns([1,2])
        category = col1.selectbox("**Category**", ["1. Surgery", "2. Injection", "3. Follow Up", "4. Others"])
        
        col1, col2, col3, col4 = st.columns(4)
        reports_mri = col1.checkbox("MRI")
        reports_ct = col2.checkbox("CT")
        reports_xray = col3.checkbox("X-ray")
        reports_blood = col4.checkbox("Blood")
        
        # Row 4: Reports + Medical History
        col1, col2, col3 = st.columns(3)
        reports_other = col1.text_input("Other Reports")
        lab_name = col2.text_input("Lab Name")
        
        col1, col2, col3, col4 = st.columns(4)
        old_dm = col1.checkbox("Diabetes")
        old_htn = col2.checkbox("HTN")
        old_cardiac = col3.checkbox("Cardiac")
        old_disease_other = col4.text_input("Other Disease")
        
        # Row 5: NEW PAYMENT SECTION
        st.subheader("💰 Payment Details")
        col1, col2, col3, col4 = st.columns(4)
        payment_amount = col1.number_input("**Amount (₹)**", min_value=0.0, format="%.0f")
        
        col1, col2 = st.columns(2)
        payment_cash = col1.checkbox("💵 Cash")
        payment_qr = col2.checkbox("📱 QR")
        
        paid_to_vishnu = st.selectbox("Paid To", ["Vishnu", "Reception", "Doctor", "Other"])
        payment_notes = st.text_input("Payment Notes", placeholder="Advance, Balance, Full paid...")
        
        # Row 6: Notes + Scoring
        col1, col2 = st.columns(2)
        clinical_notes = col1.text_area("**Clinical Notes**", height=70, 
                                       placeholder="Clinical findings, treatment plan...")
        total_points = 0  # Simplified
        
        col1, col2, col3 = st.columns(3)
        pain_score = col1.slider("Pain (0-10)", 0, 10, 0)
        severity = col2.slider("Severity (0-10)", 0, 10, 0)
        risk = col3.slider("Risk (0-10)", 0, 10, 0)
        total_points = pain_score + severity + risk
        
        # SUBMIT BUTTON
        submitted = st.form_submit_button("✅ Register & Save Payment", use_container_width=True)
    
    # Handle submission
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
            "Payment_Amount": [payment_amount],
            "Payment_Mode_Cash": [payment_cash],
            "Payment_Mode_QR": [payment_qr],
            "Paid_To_Vishnu": [paid_to_vishnu],
            "Payment_Notes": [payment_notes],
            "Clinical_Notes": [clinical_notes],
            "Pain_Score": [pain_score], "Severity_Points": [severity],
            "Risk_Points": [risk], "Total_Points": [total_points],
            "Date_Registered": [datetime.now().strftime("%Y-%m-%d %H:%M")]
        })
        
        new_patient.to_csv("patients.csv", mode='a', header=False, index=False)
        st.success(f"🎉 **{name}** registered! ID: #{new_id} | ₹{payment_amount} | {paid_to_vishnu}")
        st.balloons()

    elif submitted:
        st.error("❌ Fill Name and Phone")

with tab2:
    st.header("📋 Complete Database + Payments")
    
    try:
        df = pd.read_csv("patients.csv")
        
        # Payment Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Patients", len(df))
        col2.metric("Total Revenue", f"₹{df['Payment_Amount'].sum():.0f}")
        col3.metric("Cash Payments", len(df[df['Payment_Mode_Cash']==True]))
        col4.metric("QR Payments", len(df[df['Payment_Mode_QR']==True]))
        col5.metric("Vishnu Received", len(df[df['Paid_To_Vishnu']=='Vishnu']))
        
        st.markdown("---")
        st.subheader("📊 Full Patient + Payment Database")
        st.dataframe(df, use_container_width=True, height=500)
        
        # Download Buttons
        csv = df.to_csv(index=False).encode('utf-8')
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Full Database CSV", csv, "spine-clinic-complete.csv", use_container_width=True)
        with col2:
            st.download_button("💰 Payments CSV", csv, f"payments-{datetime.now().strftime('%Y%m%d')}.csv", use_container_width=True)
            
    except:
        st.warning("👆 Register first patient!")

st.markdown("---")
st.caption("🩺 Complete Clinic System | 💰 Payment Tracking | 📱 Mobile Ready")
