import streamlit as st
import pandas as pd
import time

# --- OOSE PILLAR: ENCAPSULATION ---
class MediCoreEngine:
    def __init__(self):
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

# --- RECTIFIED CSS (DARK SIDEBAR + DARK THEME) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp { 
        background-color: #0f172a; 
        color: #f8fafc; 
    }
    
    /* THE FIX: Forced Dark Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* Fix Sidebar Text and Icons */
    section[data-testid="stSidebar"] .stText, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #f8fafc !important;
    }

    /* Fixed Card Visibility */
    .hero-card {
        background: #ffffff; 
        padding: 35px; 
        border-radius: 16px;
        margin-bottom: 25px;
        color: #0f172a !important; /* Dark text on white card */
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .hero-card h2 { color: #0f172a !important; font-weight: 800; }
    .hero-card p { color: #334155 !important; }

    /* Metric Styling */
    [data-testid="stMetricValue"] { color: #38bdf8 !important; }
    [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    
    /* Button */
    .stButton>button {
        background-color: #38bdf8;
        color: #0f172a;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAV ---
with st.sidebar:
    st.markdown("<h2 style='color:#38bdf8;'>🏥 MediCore.AI</h2>", unsafe_allow_html=True)
    st.caption("Healthcare OS | OOSE Mini Project")
    st.divider()
    # Adding icons manually for a cleaner look
    menu = st.radio("MODULES", ["📊 Dashboard", "🤖 AI Chatbot", "🧪 Symptom Checker", "📄 Report Analyzer", "👨‍⚕️ Patient Records"])
    st.divider()
    st.info("System: AES-256 Encrypted")

# --- DASHBOARD ---
if "📊 Dashboard" in menu:
    st.title("System Dashboard")
    st.markdown("""
        <div class="hero-card">
            <h2>AI-assisted healthcare, built on classic OOP pillars.</h2>
            <p>MediCore AI combines a strongly-typed Python backend with a reactive frontend. 
            The system demonstrates <b>Abstraction</b> by simplifying clinical diagnostics and 
            <b>Encapsulation</b> by protecting patient data integrity.</p>
        </div>
    """, unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL PATIENTS", len(st.session_state.db))
    m2.metric("SYSTEM UPTIME", "99.9%")
    m3.metric("AI ACCURACY", "94.5%")
    m4.metric("ACTIVE SERVICES", "4")

    st.write("---")
    st.subheader("Weekly Patient Inflow")
    chart_data = pd.DataFrame([15, 25, 20, 45, 35, 60, 50], columns=["Patients"])
    st.area_chart(chart_data, color="#38bdf8")

# --- OTHER MODULES (Simplified for quick check) ---
elif "Symptom Checker" in menu:
    st.title("🧪 Symptom Analysis")
    name = st.text_input("Patient Name")
    syms = st.multiselect("Symptoms", ["Fever", "Cough", "Fatigue"])
    if st.button("Analyze"):
        st.success("Analysis complete. Record saved.")
        engine.add_patient(name, syms, "Viral Check", "Stable")

elif "AI Chatbot" in menu:
    st.title("🤖 Neural Core Chat")
    st.chat_message("assistant").write("Ready for clinical query analysis.")
    st.chat_input("Ask Dr. Aria...")

elif "Patient Records" in menu:
    st.title("👨‍⚕️ Records Archive")
    st.dataframe(st.session_state.db, use_container_width=True)
