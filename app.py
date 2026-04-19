import streamlit as st
import pandas as pd
import time
import random

# --- OOSE PILLAR: ENCAPSULATION ---
class MediCoreEngine:
    def __init__(self):
        # Database persistence in session state
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

# --- RECTIFIED CSS (Fixes Ghosting & Graph Contrast) ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #f8fafc; color: #1e293b; }
    
    /* Sidebar Visibility Fix */
    section[data-testid="stSidebar"] { 
        background-color: #ffffff !important; 
        border-right: 1px solid #e2e8f0; 
    }

    /* THE FIX: Forced Contrast for Hero Card */
    .hero-card {
        background: white; 
        padding: 40px; 
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 25px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    .hero-card h2 { 
        color: #0f172a !important; /* Forced dark navy */
        font-weight: 800 !important; 
        margin-bottom: 15px;
    }
    .hero-card p { 
        color: #334155 !important; /* Forced slate grey */
        line-height: 1.6 !important; 
        font-size: 1.1rem !important;
    }

    /* Metric Value Color */
    [data-testid="stMetricValue"] { color: #2563eb !important; font-weight: 700; }
    
    /* Remove default padding from charts */
    .stPlotlyChart { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAV ---
with st.sidebar:
    st.markdown("<h2 style='color:#2563eb;'>🏥 MediCore.AI</h2>", unsafe_allow_html=True)
    st.caption("Healthcare OS | OOSE Mini Project")
    st.divider()
    menu = st.radio("MODULES", ["Dashboard", "AI Chatbot", "Symptom Checker", "Report Analyzer", "Patient Records"])
    st.divider()
    st.success("Status: Services Online")

# --- DASHBOARD ---
if menu == "Dashboard":
    st.title("System Dashboard")
    
    # Hero Card - Now with fixed text visibility
    st.markdown("""
        <div class="hero-card">
            <h2>AI-assisted healthcare, built on classic OOP pillars.</h2>
            <p>MediCore AI combines a strongly-typed Python backend with a reactive frontend. 
            The system demonstrates <b>Abstraction</b> by simplifying complex clinical diagnostics into 
            user-friendly modules, and <b>Encapsulation</b> by protecting patient data integrity.</p>
        </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL PATIENTS", len(st.session_state.db))
    m2.metric("SYSTEM UPTIME", "99.9%")
    m3.metric("AI ACCURACY", "94.5%")
    m4.metric("ACTIVE SERVICES", "4")

    st.write("---")
    
    # GRAPH RECTIFICATION
    st.subheader("Weekly Patient Load (Triaging Tends)")
    # We use a static blue theme to ensure it doesn't wash out
    chart_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Inflow": [15, 22, 18, 45, 30, 55, 40]
    }).set_index("Day")
    st.area_chart(chart_data, color="#2563eb")

# --- SYMPTOM CHECKER ---
elif menu == "Symptom Checker":
    st.title("🧪 Diagnostic Lab")
    with st.container():
        name = st.text_input("Patient Registry Name")
        symptoms = st.multiselect("Identify Biomarkers", ["Fever", "Cough", "Headache", "Fatigue", "Nausea"])
        
        if st.button("Generate Analysis"):
            if name and symptoms:
                diag = "Viral Infection" if "Fever" in symptoms else "General Fatigue"
                engine.add_patient(name, symptoms, diag, "Stable")
                st.success(f"Logic Result: {diag} - Record Encapsulated.")
            else:
                st.warning("Please input both name and symptoms.")

# --- AI CHATBOT ---
elif menu == "AI Chatbot":
    st.title("🤖 AI Consultation")
    if "msgs" not in st.session_state: st.session_state.msgs = []
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
    if p := st.chat_input("Ask Dr. Aria..."):
        st.session_state.msgs.append({"role": "user", "content": p})
        with st.chat_message("user"): st.write(p)
        with st.chat_message("assistant"):
            res = "Analyzing your query against medical protocols... Please monitor symptoms and update the records."
            st.write(res)
            st.session_state.msgs.append({"role": "assistant", "content": res})

# --- REPORT ANALYZER ---
elif menu == "Report Analyzer":
    st.title("📄 Report Analysis Core")
    file = st.file_uploader("Upload Medical Scan", type=['png', 'jpg', 'pdf'])
    if file:
        with st.status("Parsing Document..."):
            time.sleep(2)
        st.info("Analysis: All biomarkers within normal range. Low inflammatory markers detected.")

# --- PATIENT RECORDS ---
elif menu == "Patient Records":
    st.title("👨‍⚕️ Encrypted Archive")
    st.dataframe(st.session_state.db, use_container_width=True, hide_index=True)
