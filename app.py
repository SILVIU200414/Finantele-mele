import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finanțe Personale", page_icon="💰")

st.title("💰 Manager Financiar")

# Secțiune Input
with st.container():
    st.subheader("Introducere Date")
    venit = st.number_input("Venituri Totale (RON)", min_value=0, value=5000)
    cheltuieli = st.number_input("Cheltuieli Lunare (Mâncare, utilități)", min_value=0, value=2000)
    datorii = st.number_input("Total Rate / Datorii", min_value=0, value=500)

# Calcule
balanta = venit - cheltuieli - datori
economii_procent = (balanta / venit * 100) if venit > 0 else 0

# Afișare Rezultate
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.metric("Rămas la final de lună", f"{balanta} RON", delta=f"{economii_procent:.1f}% din venit")
with col2:
    st.metric("Total Cheltuieli + Datorii", f"{cheltuieli + datori} RON")

# Vizualizare Grafică
st.subheader("Distribuția Banilor")
date_grafic = pd.DataFrame({
    'Categorie': ['Cheltuieli', 'Datorii', 'Disponibil'],
    'Suma': [cheltuieli, datori, max(0, balanta)]
})
st.bar_chart(date_grafic.set_index('Categorie'))

if balanta < 0:
    st.warning("⚠️ Atenție: Cheltuielile depășesc veniturile!")
elif balanta > 0:
    st.success("✅ Ești pe drumul cel bun! Economisește surplusul.")
