import numpy as np
import pandas as pd
from collections import Counter
import random
import os

def run_diversity_simulation(
    generations=50,
    mutation_rate=0.1,
    haplo_csv_name="haplotype_summary_20250601_135634.csv"
):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    haplo_csv_path = os.path.join(base_dir, "..", "data", "final", haplo_csv_name)
    haplo_csv_path = os.path.normpath(haplo_csv_path)

    if not os.path.isfile(haplo_csv_path):
        raise FileNotFoundError(f"Tidak menemukan file haplotype CSV di: {haplo_csv_path}")

    haplo_df = pd.read_csv(haplo_csv_path)
    hap_counts = dict(zip(haplo_df["haplotype_id"], haplo_df["sequence_count"]))
    unique_haplotypes = list(hap_counts.keys())

    population = []
    for hap, count in hap_counts.items():
        population.extend([hap] * int(count))

    def haplotype_diversity(pop):
        N = len(pop)
        counts = Counter(pop)
        freqs = np.array(list(counts.values())) / N
        if N <= 1:
            return 0.0
        Hd = (N / (N - 1)) * (1 - np.sum(freqs ** 2))
        return Hd

    def shannon_entropy(pop):
        N = len(pop)
        counts = Counter(pop)
        freqs = np.array(list(counts.values())) / N
        freqs = freqs[freqs > 0]
        return -np.sum(freqs * np.log(freqs))

    results = []
    current_population = population.copy()

    for gen in range(generations):
        hd = haplotype_diversity(current_population)
        shannon = shannon_entropy(current_population)
        results.append({
            "Generation": gen,
            "Haplotype_Diversity": hd,
            "Shannon_Index": shannon
        })

        next_population = []
        N = len(current_population)
        for _ in range(N):
            parent_hap = random.choice(current_population)
            offspring_hap = (
                random.choice(unique_haplotypes) if random.random() < mutation_rate else parent_hap
            )
            next_population.append(offspring_hap)

        current_population = next_population

    df = pd.DataFrame(results)
    output_path = os.path.join("results", "diversity_simulation_results.csv")
    df.to_csv(output_path, index=False)
    return df
