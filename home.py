import streamlit as st

st.set_page_config(
    page_title="Simulasi Evolusi Ngengat",
    layout="wide",
    page_icon="🦋"
)

st.title("🦋 Simulasi Evolusi Ngengat Berbasis Agen")

st.markdown("""
Selamat datang di **Simulasi Evolusi Ngengat**, sebuah aplikasi untuk mengeksplorasi seleksi alam, mutasi, dan adaptasi genetik populasi ngengat melalui pendekatan **Agent-Based Modeling (ABM)**.
""")

st.markdown("---")

st.subheader("🔍 Tentang Proyek")
st.markdown("""
📌 Proyek ini memodelkan dinamika evolusi berdasarkan:
- Data genetik nyata (haplotype COI dari GenBank)
- Faktor lingkungan (seperti tingkat polusi)
- Reproduksi selektif dan mutasi adaptif

Hasilnya divisualisasikan untuk membantu memahami perubahan keanekaragaman genetik populasi dari waktu ke waktu.
""")

st.markdown("---")

st.subheader("🚀 Siap Bereksperimen?")
st.markdown("Klik tombol di bawah ini untuk memulai simulasi interaktif.")

if st.button("🔬 Masuk ke Halaman Simulasi"):
    st.switch_page("pages/simulasi.py")
