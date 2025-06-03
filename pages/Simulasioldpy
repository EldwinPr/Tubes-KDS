import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import runModel
import traceback

st.set_page_config(
    page_title="Simulasi Evolusi Ngengat",
    layout="wide",
    page_icon="🦋"
)

st.title("🦋 Simulasi Evolusi Ngengat Berbasis Agen")

st.sidebar.header("🔧 Parameter Simulasi")
generations = st.sidebar.slider("Jumlah Generasi", 10, 200, 50, step=10)
pollution_level = st.sidebar.slider("Tingkat Polusi (0.0 - 1.0)", 0.0, 1.0, 0.5, step=0.05)
mutation_rate = st.sidebar.slider("Tingkat Mutasi", 0.0, 0.1, 0.01, step=0.005)

if "simulasi_dijalankan" not in st.session_state:
    st.session_state["simulasi_dijalankan"] = False
if "simulasi_trigger" not in st.session_state:
    st.session_state["simulasi_trigger"] = False

if st.sidebar.button("▶️ Jalankan Simulasi"):
    st.session_state["simulasi_trigger"] = True

if st.session_state["simulasi_trigger"]:
    st.session_state["simulasi_trigger"] = False

    try:
        st.session_state["simulasi_dijalankan"] = True
        st.info("⏳ Menjalankan simulasi...")

        env_schedule = [pollution_level] * generations

        df = runModel.run_simulation(
            N_initial=500,
            mutation_rate=mutation_rate,
            env_schedule=env_schedule
        )

        df = df.reset_index().rename(columns={"index": "Generation"})
        st.session_state["simu_df"] = df

        st.success("✅ Simulasi selesai!")

    except Exception as e:
        st.session_state["simulasi_dijalankan"] = False
        st.error("❌ Terjadi error saat simulasi.")
        st.code(traceback.format_exc())

if not st.session_state["simulasi_dijalankan"]:
    st.info("📢 Belum ada simulasi yang dijalankan.")
    st.markdown("""
    Silakan atur parameter di sidebar, lalu tekan tombol **"▶️ Jalankan Simulasi"**  
    untuk melihat bagaimana populasi ngengat berevolusi terhadap tekanan lingkungan dan mutasi genetik.
    
    🔧 Parameter yang dapat diatur:
    - Jumlah generasi
    - Tingkat polusi lingkungan
    - Peluang mutasi genetik

    📊 Setelah simulasi selesai, akan ditampilkan grafik, data, dan tombol ekspor hasil.
    """)

if st.session_state.get("simu_df") is not None:
    df = st.session_state["simu_df"]

    st.subheader("📊 Hasil Simulasi")
    selected_metric = st.selectbox("Pilih metrik", df.columns[1:], key="metric_selector")

    fig, ax = plt.subplots(figsize=(4, 2))
    ax.plot(df["Generation"], df[selected_metric], marker='o')
    ax.set_xlabel("Generasi", fontsize=6)
    ax.set_ylabel(selected_metric, fontsize=6)
    ax.set_title(f"Perubahan {selected_metric} selama Generasi", fontsize=8)
    ax.tick_params(labelsize=7)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("🗂️ Data mentah:")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Unduh Hasil CSV", csv, file_name="hasil_simulasi.csv", mime="text/csv")
