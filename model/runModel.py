# runModel.py  (Letakkan di root TUBES-KDS/ atau di dalam folder model/, 
#              namun pastikan impor path-nya sesuai.)
import pandas as pd
import os
from mothModel import MothModel
from MothAgent import MothAgent

def main():
    # 1. Tentukan lokasi file Haplotype CSV
    #    Jika runModel.py berada di folder root TUBES-KDS/, maka path-nya:
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # Dari situ, naik satu level lalu masuk ke data/final/…
    csv_name = "haplotype_summary_20250601_135634.csv"
    haplo_csv_path = os.path.join(base_dir, csv_name)
    haplo_csv_path = os.path.normpath(haplo_csv_path)

    # 3. Cek keberadaan file
    if not os.path.isfile(haplo_csv_path):
        raise FileNotFoundError(f"Tidak menemukan file haplotype CSV di: {haplo_csv_path}")
    # 2. Muat data haplotype dengan pandas
    haplo_df = pd.read_csv(haplo_csv_path)

    # … lanjutkan kode seperti biasa …
    print("CSV berhasil dimuat, jumlah baris:", len(haplo_df))
    
    # 3. Bentuk variabel haplotype_pool
    #    goal: haplotype_pool = { haplotype_id: { "sequence": ..., "frequency": ... }, ... }
    haplotype_pool = {}
    for _, row in haplo_df.iterrows():
        hid = row["haplotype_id"]
        seq = row["representative_sequence"]  # kolom di CSV
        freq = row["frequency"]               # kolom di CSV
        # Simpan ke dictionary
        haplotype_pool[hid] = {
            "sequence": seq,
            "frequency": freq
        }
    
    # 4. Buat mapping haplotype → phenotype ('light' atau 'dark', dsb.)
    #    Contoh sederhana: jika nama haplotype mengandung "002" jadikan 'dark', sisanya 'light'.
    #    Anda bisa menyesuaikan aturan ini sesuai data sebenarnya.
    haplotype_to_phenotype = {}
    for hid in haplotype_pool:
        if hid.endswith("002"):            # contoh aturan: Hap_002 → 'dark'
            haplotype_to_phenotype[hid] = "dark"
        else:
            haplotype_to_phenotype[hid] = "light"
    
    # 5. Atur parameter simulasi
    N_initial = 500                  # jumlah agen awal
    mutation_rate = 0.01             # misal 1% peluang mutasi per agen per langkah
    # Contoh schedule tekanan lingkungan: 
    #   10 langkah pertama env_pressure = 0.2, 
    #   10 langkah berikutnya env_pressure = 0.8
    env_schedule = [0.2] * 10 + [0.8] * 10
    
    # 6. Inisialisasi model
    model = MothModel(
        N_initial=N_initial,
        haplotype_pool=haplotype_pool,
        haplotype_to_phenotype=haplotype_to_phenotype,
        mutation_rate=mutation_rate,
        environment_schedule=env_schedule
    )
    
    # 7. Jalankan simulasi sebanyak len(env_schedule) langkah
    for step in range(len(env_schedule)):
        model.step()
    
    # 8. Ekspor hasil DataCollector ke CSV (misalnya ke folder results/)
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    df = model.datacollector.get_model_vars_dataframe()
    output_file = os.path.join(output_dir, "simulation_output.csv")
    df.to_csv(output_file, index=False)
    print(f"Simulasi selesai. Hasil disimpan di: {output_file}")

if __name__ == "__main__":
    main()
