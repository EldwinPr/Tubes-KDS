import streamlit as st

st.set_page_config(
    page_title="Simulasi Keanekaragaman Genetik Populasi Ngengat",
    layout="wide",
    page_icon="🦋"
)

st.title("🦋 Simulasi Keanekaragaman Genetik Populasi Ngengat")

st.markdown("""
Selamat datang di Simulasi Evolusi Ngengat, sebuah aplikasi edukatif untuk mengeksplorasi seleksi alam, mutasi, dan dinamika adaptasi dalam populasi ngengat menggunakan pendekatan Agent-Based Modeling (ABM) berbasis data genetik nyata.
""")

st.markdown("---")

st.subheader("🔍 Tentang")
st.markdown("""
Simulasi ini memodelkan proses evolusi dengan:
- Agent-Based Modeling (ABM): setiap individu ngengat direpresentasikan sebagai agen dengan atribut genetik dan fenotip adaptif.
- Data genetik nyata dari GenBank (haplotype COI), digunakan untuk menginisialisasi keragaman awal populasi.
- Lingkungan dinamis (misalnya polusi) yang memengaruhi survival dan reproduksi berdasarkan kecocokan fenotip.
- Mutasi dan seleksi alam, yang menghasilkan perubahan frekuensi genetik dari generasi ke generasi.
""")

st.markdown("---")

st.subheader("🧪 Tujuan Simulasi")
st.markdown("""
 Simulasi ini membantu memahami:
- Agent-Based Modeling (ABM): setiap individu ngengat direpresentasikan sebagai agen dengan atribut genetik dan fenotip adaptif.
- Data genetik nyata dari GenBank (haplotype COI), digunakan untuk menginisialisasi keragaman awal populasi.
- Lingkungan dinamis (misalnya polusi) yang memengaruhi survival dan reproduksi berdasarkan kecocokan fenotip.
- Mutasi dan seleksi alam, yang menghasilkan perubahan frekuensi genetik dari generasi ke generasi.
""")

st.markdown("---")

st.subheader("📈 Hasil Simulasi")
st.markdown("""
Simulasi ini membantu memahami:
- Perubahan metrik haplotype diversity dan Shannon index
- Visualisasi grafik per generasi
- Data siap unduh untuk analisis lebih lanjut
""")

st.markdown("---")

st.subheader("🚀 Mulai Eksperimen?")
st.markdown("Klik tombol di bawah ini untuk memulai simulasi interaktif.")

if st.button("🔬 Masuk ke Halaman Simulasi"):
    st.switch_page("pages/Simulasi.py")
