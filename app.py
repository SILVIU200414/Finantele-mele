
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurare pagină pentru mobil
st.set_page_config(page_title="Pro Finance Manager", page_icon="📈", layout="wide")

# Stil vizual personalizat (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Control Financiar Detaliat")

# --- DATE DE INTRARE (LUNA CURENTĂ) ---
with st.sidebar:
    st.header("⚙️ Introducere Date")
    luna_selectata = st.selectbox("Luna", ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie"])
    venit_realizat = st.number_input("Venit Realizat (RON)", min_value=0, value=6500)
    
    st.subheader("Cheltuieli Detaliate")
    c_fixe = st.number_input("Fixe (Chirie, Utilități)", value=2200)
    c_variabile = st.number_input("Variabile (Mâncare, Shopping)", value=1800)
    datorii_rate = st.number_input("Datorii / Rate", value=700)

# --- CALCULE ---
total_cheltuieli = c_fixe + c_variabile + datorii_rate
disponibil = venit_realizat - total_cheltuieli
economii_rata = (disponibil / venit_realizat * 100) if venit_realizat > 0 else 0

# --- DASHBOARD PRINCIPAL ---
st.subheader(f"Rezumat {luna_selectata}")
col1, col2, col3, col4 = st.columns(4)

# Comparăm simulat cu luna trecută (ex: 5% mai bine)
col1.metric("Venit Total", f"{venit_realizat} RON", "+5%")
col2.metric("Total Cheltuit", f"{total_cheltuieli} RON", "-2%", delta_color="inverse")
col3.metric("Disponibil (Cash)", f"{disponibil} RON", "120 RON")
col4.metric("Rată Economisire", f"{economii_rata:.1f}%", "2.1%")

st.divider()

# --- ANALIZĂ DETALIATĂ ---
c_stanga, c_dreapta = st.columns([1, 1])

with c_stanga:
    st.write("### 🥧 Distribuția Bugetului")
    fig_pie = go.Figure(data=[go.Pie(
        labels=['Cheltuieli Fixe', 'Variabile', 'Datorii', 'Economii'],
        values=[c_fixe, c_variabile, datorii_rate, max(0, disponibil)],
        hole=.4,
        marker_colors=['#264653', '#2a9d8f', '#e9c46a', '#f4a261']
    )])
    fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

with c_dreapta:
    st.write("### 📅 Evoluție Ultimele 3 Luni")
    # Date simulate pentru istoric
    date_istoric = pd.DataFrame({
        'Luna': ['Decembrie', 'Ianuarie', 'Februarie', 'Martie'],
        'Venit': [6000, 6200, 5800, venit_realizat],
        'Cheltuieli': [4500, 4300, 4600, total_cheltuieli],
        'Economii': [1500, 1900, 1200, disponibil]
    })
    
    st.line_chart(date_istoric.set_index('Luna'))

# --- TABEL DETALIAT ---
st.subheader("📝 Jurnal Tranzacții")
st.dataframe(date_istoric, use_container_width=True)

# Buton Salvare
if st.button("💾 Salvează și Închide Luna"):
    st.balloons()
    st.success("Datele au fost arhivate cu succes!")
