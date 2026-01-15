import streamlit as st
import pandas as pd
from datetime import datetime
import os
import webbrowser

st.set_page_config(page_title="Spine Clinic", page_icon="🩺", layout="wide")

# CSS
st.markdown("""
<style>
.stTabs [data-baseweb="tab"] {background-color: #4CAF50; color: white; border-radius: 10px;}
h1 {color: #2E7D32 !important; font-size: 2.5rem !important}
.whatsapp-btn {background-color: #25D366 !important; color: white !important}
</style>
""", unsafe_allow_html=True)

# CSV Backend
if not os.path.exists("patients.csv"):
    df = pd.DataFrame(columns=[
        "ID", "Name", "Age", "Sex", "Place", "Phone_No", "Alternate_Phone", 
        "Relative", "Category", "Payment_Amount", "Payment_Mode_Cash", 
        "Payment_Mode_QR", "Paid_To_Vishnu", "Clinical_Notes", "Date_Registered"
    ])
    df.to_csv("patients.csv", index=False)

st.title("🩺 Spine Clinic + 📱 WhatsApp Button")
st.markdown("---")

# TABS
tab1, tab2 = st.tabs(["📝 Register Patient", "📊 Database + WhatsApp"])

with tab1:
    with st.form("patient_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        name = col1.text_input("**Name** *")
        age = col2.number_input("**Age**")
        sex = col3.selectbox("**Sex**", ["Male", "Female", "Other"])
        place = col4.text_input("**Place**")
        
        col1, col2, col3 = st.columns(3)
        phone_no = col1.text_input("**Phone** *")
        category = col2.selectbox("**Category**", ["1. Surgery", "2. Injection", "3. Follow Up", "4. Others"])
        relative = col3.text_input("Relative")
        
        # Payment
        col1, col2 = st.columns(2)
        payment_amount = col1.number_input("**Amount ₹**", format="%.0f")
        paid_to_vishnu = col2.selectbox("Paid To", ["Vishnu", "Reception"])
        
        col1, col2 = st.columns(2)
        payment_cash = col1.checkbox("💵 Cash")
        payment_qr = col2.checkbox("📱 QR")
        
        notes = st.text_area("**Notes**", height=70)
        submitted = st.form_submit_button("✅ Register Patient", use_container_width=True)
    
    if submitted and name and phone_no:
        df = pd.read_csv("patients.csv")
        new_id = len(df) + 1
        
        new_patient = pd.DataFrame({
            "ID": [new_id], "Name": [name], "Age": [age], "Sex": [sex],
            "Place": [place], "Phone_No": [phone_no], "Relative": [relative],
            "Category": [category], "Payment_Amount": [payment_amount],
            "Payment_Mode_Cash": [payment_cash], "Payment_Mode_QR": [payment_qr],
            "Paid_To_Vishnu": [paid_to_vishnu], "Clinical_Notes": [notes],
            "Date_Registered": [datetime.now().strftime("%Y-%m-%d %H:%M")]
        })
        new_patient.to_csv("patients.csv", mode='a', header=False, index=False)
        st.success(f"🎉 **{name}** registered! ID: #{new_id}")
        st.balloons()

with tab2:
    st.header("📋 Patient Database")
    
    try:
        df = pd.read_csv("patients.csv")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Patients", len(df))
        col2.metric("Total Revenue", f"₹{df['Payment_Amount'].sum():.0f}")
        col3.metric("Vishnu Payments", len(df[df['Paid_To_Vishnu']=='Vishnu']))
        
        st.markdown("---")
        
        # ✅ WHATSAPP BUTTON FOR EACH PATIENT
        st.subheader("👆 Click WhatsApp Button for Any Patient")
        for index, row in df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**ID #{row['ID']}** - {row['Name']}")
                    st.caption(f"{row['Category']} | ₹{row['Payment_Amount']} | {row['Phone_No']}")
                
                with col2:
                    st.caption(f"Paid to: {row['Paid_To_Vishnu']} | {row['Date_Registered']}")
                
                with col3:
                    # ✅ WHATSAPP BUTTON - ONE CLICK!
                    if st.button(f"📱 WhatsApp", key=f"whatsapp_{row['ID']}", 
                               help=f"Send details to {row['Phone_No']}"):
                        
                        phone = str(row['Phone_No']).lstrip('+91')
                        whatsapp_number = f"https://wa.me/91{phone}"
                        
                        message = f"""🩺 *SPINE CLINIC RECORD*

*Patient:* {row['Name']}
*ID:* #{row['ID']}
*Category:* {row['Category']}
*Amount:* ₹{row['Payment_Amount']:,}
*Paid to:* {row['Paid_To_Vishnu']}
*Date:* {row['Date_Registered']}

{row['Clinical_Notes'][:100]}..."""

                        # Create WhatsApp link
                        encoded_message = message.replace(" ", "%20").replace("\n", "%0A")
                        full_link = f"{whatsapp_number}?text={encoded_message}"
                        
                        # Open WhatsApp automatically
                        st.markdown(f"[**📱 OPEN WHATSAPP**]({full_link})")
                        webbrowser.open(full_link)
                        st.success(f"✅ WhatsApp opened for {row['Name']}!")
        
        # CSV Download
        st.markdown("---")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "clinic-data.csv", use_container_width=True)
        
    except:
        st.info("👆 Register first patient!")

st.caption("🩺 Complete System | 📱 One-Click WhatsApp | 💰 Payments")
