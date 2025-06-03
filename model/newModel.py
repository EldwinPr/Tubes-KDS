import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import random
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

haplo_csv_name = "haplotype_summary_20250601_135634.csv"
haplo_csv_path = os.path.join(base_dir, "..", "data", "final", haplo_csv_name)
haplo_csv_path = os.path.normpath(haplo_csv_path)

if not os.path.isfile(haplo_csv_path):
    raise FileNotFoundError(f"Tidak menemukan file haplotype CSV di: {haplo_csv_path}")

haplo_df = pd.read_csv(haplo_csv_path)

hap_counts = dict(zip(haplo_df["haplotype_id"], haplo_df["sequence_count"]))

unique_haplotypes = list(hap_counts.keys())

initial_population_size = sum(hap_counts.values())

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
    # Hindari log(0)
    freqs = freqs[freqs > 0]
    H = -np.sum(freqs * np.log(freqs))
    return H


generations = 20         
mutation_rate = 0.15     

results = []

current_population = population.copy()


for gen in range(generations):
    hd = haplotype_diversity(current_population)
    shannon = shannon_entropy(current_population)
    results.append({
        "generation": gen,
        "haplotype_diversity": hd,
        "shannon_index": shannon
    })
    
    next_population = []
    N = len(current_population)
    
    for _ in range(N):
        parent_hap = random.choice(current_population)
        
        if random.random() < mutation_rate:
            offspring_hap = random.choice(unique_haplotypes)
        else:
            offspring_hap = parent_hap
        
        next_population.append(offspring_hap)
    
    current_population = next_population

results_df = pd.DataFrame(results)
results_df.to_csv("diversity_simulation2_results.csv", index=False)

print(results_df.head())

