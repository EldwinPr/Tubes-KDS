import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model import newModel
import traceback

st.set_page_config(
    page_title="Simulasi Keanekaragaman Genetik Populasi Ngengat",
    layout="wide",
    page_icon="🧬"
)

st.title("🧬 Simulasi Keanekaragaman Genetik Populasi Ngengat")

st.sidebar.header("🔧 Parameter Simulasi Diversity")
generations = st.sidebar.slider("Jumlah Generasi", 10, 200, 50, step=10)
mutation_rate = st.sidebar.slider("Tingkat Mutasi", 0.0, 0.5, 0.1, step=0.01)

if "diversity_simulasi_dijalankan" not in st.session_state:
    st.session_state["diversity_simulasi_dijalankan"] = False
if "diversity_simulasi_trigger" not in st.session_state:
    st.session_state["diversity_simulasi_trigger"] = False

if st.sidebar.button("▶️ Jalankan Simulasi Diversity"):
    st.session_state["diversity_simulasi_trigger"] = True

if st.session_state["diversity_simulasi_trigger"]:
    st.session_state["diversity_simulasi_trigger"] = False

    try:
        st.session_state["diversity_simulasi_dijalankan"] = True
        st.info("⏳ Menjalankan simulasi...")

        df = newModel.run_diversity_simulation(
            generations=generations,
            mutation_rate=mutation_rate
        )

        st.session_state["diversity_df"] = df

        st.success("✅ Simulasi selesai!")

    except Exception as e:
        st.session_state["diversity_simulasi_dijalankan"] = False
        st.error("❌ Terjadi error saat simulasi.")
        st.code(traceback.format_exc())

if not st.session_state["diversity_simulasi_dijalankan"]:
    st.info("📢 Belum ada simulasi diversity yang dijalankan.")
    st.markdown("""
    Silakan atur parameter di sidebar, lalu tekan tombol **"▶️ Jalankan Simulasi Diversity"**  
    untuk melihat bagaimana keanekaragaman genetik populasi ngengat berubah akibat mutasi antar generasi.

    🔧 Parameter yang dapat diatur:
    - Jumlah generasi
    - Peluang mutasi haplotype

    📊 Setelah simulasi selesai, akan ditampilkan grafik diversity dan data mentah hasil simulasi.
    """)

if st.session_state.get("diversity_df") is not None:
    df = st.session_state["diversity_df"]

    st.subheader("📊 Hasil Simulasi Diversity")
    selected_metric = st.selectbox(
        "Pilih metrik", ["Haplotype_Diversity", "Shannon_Index"], key="diversity_metric_selector"
    )

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
    st.download_button("📥 Unduh Hasil CSV", csv, file_name="diversity_simulation.csv", mime="text/csv")
