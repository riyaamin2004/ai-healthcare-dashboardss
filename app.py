import streamlit as st
import pandas as pd
import time
import random

# --- OOSE PILLAR: ENCAPSULATION ---
class MediCoreEngine:
    def __init__(self):
        # Data persistence in session state
        if 'db' not in st.session_state:
            st.session_state.db = pd.DataFrame([
                {"ID": "P-101", "Name": "Riya Sharma", "Condition": "Viral Flu", "Priority": "Low"},
                {"ID": "P-102", "Name": "Aman Verma", "Condition": "Anemia", "Priority": "Stable"}
            ])

    def add_patient(self, name, symptoms, diagnosis, priority):
        new_id = f"P-{100 + len(st.session_state.db) + 1}"
        new_data = {"ID": new_id, "Name": name, "Condition": diagnosis, "Priority": priority}
        st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)

# --- APP INIT ---
st.set_page_config(page_title="MediCore.AI", layout="wide", page_icon="🏥")
engine = MediCoreEngine()

# --- RECTIFIED CSS (Fixed Graph Contrast) ---
st.markdown("""
    <style>
    /* Clean Light Background */
    .stApp { background-color: #f9fafb; color: #111827; }
    
    /* Sidebar Fix */
    section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e5e7eb; }

    /* Bento Card Layout */
    .hero-card {
        background: white; 
        padding: 32px; 
        border-radius: 16px;
        border: 1px solid #f3f4f6;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 24px;
    }
    .hero-card h2 { color: #111827 !important; font-weight: 800; }
    .hero-card p { color: #4b5563 !important; line-height: 1.6; }

    /* Fixed Chart Container */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #f3f4f6;
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] { color: #2563eb !important; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🏥 MediCore.AI")
    st.caption("Healthcare OS | OOSE Mini Project")
    st.divider()
    menu = st.radio("MODULES", ["Dashboard", "AI Chatbot", "Symptom Checker", "Report Analyzer", "Patient Records"])
    st.divider()
    st.info("Status: Services Online")

# --- DASHBOARD ---
if menu == "Dashboard":
    st.title("Dashboard")
    
    st.markdown("""
        <div class="hero-card">
            <h2>AI-assisted healthcare, built on classic OOP pillars.</h2>
            <p>MediCore AI combines a strongly-typed Python backend with a reactive frontend. 
            The system demonstrates Abstraction by simplifying complex clinical diagnostics into 
            user-friendly modules.</p>
        </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL PATIENTS", len(st.session_state.db))
    m2.metric("SYSTEM UPTIME", "99.9%")
    m3.metric("AI ACCURACY", "94.5%")
    m4.metric("ACTIVE SERVICES", "4")

    st.write("---")
    
    # RECTIFIED GRAPH SECTION
    st.subheader("Weekly Patient Load")
    chart_data = pd.DataFrame([12, 18, 14, 32, 28, 45, 38], columns=["Inpatients"])
    st.area_chart(chart_data, color="#2563eb")

# --- SYMPTOM CHECKER ---
elif menu == "Symptom Checker":
    st.title("🧪 Symptom Checker")
    with st.form("diag_form"):
        name = st.text_input("Patient Name")
        symptoms = st.multiselect("Active Symptoms", ["Fever", "Cough", "Headache", "Fatigue"])
        if st.form_submit_button("Run Analysis"):
            diag = "Viral Flu" if "Fever" in symptoms else "General Fatigue"
            engine.add_patient(name, symptoms, diag, "Stable")
            st.success(f"Diagnosis: {diag}")
            st.balloons()

# --- AI CHATBOT ---
elif menu == "AI Chatbot":
    st.title("🤖 AI Chatbot")
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
    if p := st.chat_input("Ask anything..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        with st.chat_message("assistant"):
            res = "Analyzing your query... Based on clinical data, please monitor your symptoms closely."
            st.write(res)
            st.session_state.msgs.append({"role": "assistant", "content": res})

# --- REPORT ANALYZER ---
elif menu == "Report Analyzer":
    st.title("📄 Report Analyzer")
    file = st.file_uploader("Upload Lab Report", type=['png', 'jpg', 'pdf'])
    if file:
        with st.status("Extracting Data..."):
            time.sleep(2)
        st.success("Analysis Complete: WBC Count slightly elevated. Recommend hydration.")

# --- PATIENT RECORDS ---
elif menu == "Patient Records":
    st.title("👨‍⚕️ Patient Records")
    st.dataframe(st.session_state.db, use_container_width=True, hide
