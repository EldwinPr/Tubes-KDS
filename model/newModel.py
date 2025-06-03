import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import random
import os

# ==========================
# 1. Baca Data Haplotype COI
# ==========================
# Pastikan file CSV Anda memiliki kolom: haplotype_id, sequence_count, frequency

base_dir = os.path.abspath(os.path.dirname(__file__))

haplo_csv_name = "haplotype_summary_20250601_135634.csv"
haplo_csv_path = os.path.join(base_dir, "..", "data", "final", haplo_csv_name)
haplo_csv_path = os.path.normpath(haplo_csv_path)

if not os.path.isfile(haplo_csv_path):
    raise FileNotFoundError(f"Tidak menemukan file haplotype CSV di: {haplo_csv_path}")

haplo_df = pd.read_csv(haplo_csv_path)

# Buat dictionary {haplotype_id: sequence_count}
hap_counts = dict(zip(haplo_df["haplotype_id"], haplo_df["sequence_count"]))

# Daftar semua haplotype unik
unique_haplotypes = list(hap_counts.keys())

# Hitung total populasi awal
initial_population_size = sum(hap_counts.values())

# ==========================
# 2. Inisialisasi Populasi
# ==========================
# Representasi populasi sebagai list of haplotype_id, panjang = initial_population_size
population = []
for hap, count in hap_counts.items():
    population.extend([hap] * int(count))

# ==========================
# 3. Fungsi Keanekaragaman
# ==========================
def haplotype_diversity(pop):
    """
    Hitung Haplotype Diversity (Hd):
    Hd = (N/(N-1)) * (1 - sum(pi^2))
    di mana pi = frekuensi haplotype i = n_i / N
    """
    N = len(pop)
    counts = Counter(pop)
    freqs = np.array(list(counts.values())) / N
    if N <= 1:
        return 0.0
    Hd = (N / (N - 1)) * (1 - np.sum(freqs ** 2))
    return Hd

def shannon_entropy(pop):
    """
    Hitung Shannon-Wiener index:
    H = - sum(pi * log(pi))
    """
    N = len(pop)
    counts = Counter(pop)
    freqs = np.array(list(counts.values())) / N
    # Hindari log(0)
    freqs = freqs[freqs > 0]
    H = -np.sum(freqs * np.log(freqs))
    return H

# ==========================
# 4. Parameter Simulasi ABM
# ==========================
generations = 20         # Jumlah generasi yang disimulasikan
mutation_rate = 0.15     # Probabilitas mutasi per individu per generasi (1%)

# List untuk menyimpan hasil keanekaragaman tiap generasi
results = []

# Copy populasi awal untuk simulasi
current_population = population.copy()

# ==========================
# 5. Loop Simulasi Per Generasi
# ==========================
for gen in range(generations):
    # 5.1 Hitung Keanekaragaman pada Generasi ini
    hd = haplotype_diversity(current_population)
    shannon = shannon_entropy(current_population)
    results.append({
        "generation": gen,
        "haplotype_diversity": hd,
        "shannon_index": shannon
    })
    
    # 5.2 Inisialisasi Populasi Generasi Berikutnya
    next_population = []
    N = len(current_population)
    
    # Tiap individu baru “dipilih” dari generasi sekarang (drift netral + mutasi)
    for _ in range(N):
        parent_hap = random.choice(current_population)
        
        # 5.2.1 Mutasi: dengan peluang kecil, haplotype berubah
        if random.random() < mutation_rate:
            offspring_hap = random.choice(unique_haplotypes)
        else:
            offspring_hap = parent_hap
        
        next_population.append(offspring_hap)
    
    # Update populasi ke generasi selanjutnya
    current_population = next_population

# ==========================
# 6. Simpan Hasil ke CSV
# ==========================
results_df = pd.DataFrame(results)
results_df.to_csv("diversity_simulation2_results.csv", index=False)

# Tampilkan 5 baris pertama hasil sebagai konfirmasi
print(results_df.head())

