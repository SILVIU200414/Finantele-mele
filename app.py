import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Personal Finance Pro", page_icon="🏦", layout="wide")

st.title("🏦 Analiză Financiară Detaliată")

# --- SIDEBAR PENTRU INTRODUCERE DATE ---
with st.sidebar:
    st.header("📥 Introducere Date")
    
    with st.expander("💰 VENITURI (Detaliat)", expanded=True):
        v_salariu = st.number_input("Salariu Net", value=5000)
        v_bonus = st.number_input("Bonusuri / Prime", value=0)
        v_extra = st.number_input("Alte surse (Freelance, chirii)", value=0)
        total_venit = v_salariu + v_bonus + v_extra

    with st.expander("🛒 CHELTUIELI (Detaliat)", expanded=True):
        st.subheader("Necesități (Fixe)")
        c_chirie = st.number_input("Chirie / Rată Casă", value=1500)
        c_utilitati = st.number_input("Utilități (Gaz, curent, net)", value=500)
        c_supermarket = st.number_input("Supermarket / Mâncare", value=1200)
        
        st.subheader("Stil de viață (Variabile)")
        c_oras = st.number_input("Ieșiri în oraș / Restaurante", value=400)
        c_transport = st.number_input("Transport / Benzină", value=300)
        c_sanatate = st.number_input("Sănătate / Îngrijire", value=150)
        c_haine = st.number_input("Haine / Shopping", value=200)
        
        st.subheader("Obligații")
        c_datorii = st.number_input("Rate bănci / Credite", value=400)
        c_abonamente = st.number_input("Abonamente (Netflix, Gym)", value=100)

    total_cheltuieli = (c_chirie + c_utilitati + c_supermarket + 
                        c_oras + c_transport + c_sanatate + 
                        c_haine + c_datorii + c_abonamente)
    
    disponibil = total_venit - total_cheltuieli

# --- DASHBOARD PRINCIPAL ---
col1, col2, col3 = st.columns(3)
col1.metric("Venit Total", f"{total_venit} RON")
col2.metric("Cheltuieli Totale", f"{total_cheltuieli} RON", delta=f"{(total_cheltuieli/total_venit*100):.1f}% din venit", delta_color="inverse")
col3.metric("Economii (Disponibil)", f"{disponibil} RON", delta=f"{disponibil} RON", delta_color="normal")

st.divider()

# --- GRAFICE ANALITICE ---
tab1, tab2 = st.tabs(["📊 Analiză Cheltuieli", "📈 Evoluție & Comparare"])

with tab1:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("### Unde se duc banii?")
        labels = ['Locuință', 'Mâncare', 'Stil de viață', 'Transport', 'Sănătate', 'Datorii', 'Abonamente', 'Economii']
        values = [c_chirie + c_utilitati, c_supermarket, c_oras + c_haine, c_transport, c_sanatate, c_datorii, c_abonamente, max(0, disponibil)]
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.write("### Clasament Cheltuieli")
        df_explodat = pd.DataFrame({
            'Categorie': labels[:-1], # Fără economii
            'Suma': values[:-1]
        }).sort_values(by='Suma', ascending=True)
        st.bar_chart(df_explodat.set_index('Categorie'))

with tab2:
    st.write("### Comparare cu ultimele 3 luni")
    # Date simulate pentru istoric (Vom lucra la salvarea lor data viitoare)
    data_hist = {
        'Luna': ['Decembrie', 'Ianuarie', 'Februarie', 'Martie (Curent)'],
        'Venituri': [total_venit-500, total_venit-200, total_venit+100, total_venit],
        'Cheltuieli': [total_cheltuieli+200, total_cheltuieli-100, total_cheltuieli+300, total_cheltuieli]
    }
    df_hist = pd.DataFrame(data_hist)
    st.line_chart(df_hist.set_index('Luna'))

# MESAJ DE FINAL
if disponibil > 0:
    st.balloons()
    st.success(f"Bravo! Ai reușit să pui deoparte {(disponibil/total_venit*100):.1f}% din venituri luna aceasta.")
else:
    st.error("Atenție! Cheltuielile sunt mai mari decât veniturile. Verifică secțiunea 'Stil de viață'.")
