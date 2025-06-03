# runModel.py
import pandas as pd
import os
from .mothModel import MothModel
from .MothAgent import MothAgent

def run_simulation(N_initial=500, mutation_rate=0.01, env_schedule=None, haplo_csv_name=None):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    if haplo_csv_name is None:
        haplo_csv_name = "haplotype_summary_20250601_135634.csv"
    haplo_csv_path = os.path.join(base_dir, "..", "data", "final", haplo_csv_name)
    haplo_csv_path = os.path.normpath(haplo_csv_path)

    if not os.path.isfile(haplo_csv_path):
        raise FileNotFoundError(f"Tidak menemukan file haplotype CSV di: {haplo_csv_path}")
    
    haplo_df = pd.read_csv(haplo_csv_path)

    haplotype_pool = {}
    for _, row in haplo_df.iterrows():
        hid = row["haplotype_id"]
        haplotype_pool[hid] = {
            "sequence": row["representative_sequence"],
            "frequency": row["frequency"]
        }

    haplotype_to_phenotype = {}
    for hid in haplotype_pool:
        haplotype_to_phenotype[hid] = "dark" if hid.endswith("002") else "light"

    if env_schedule is None:
        env_schedule = [0.2] * 10 + [0.8] * 10

    model = MothModel(
        N_initial=N_initial,
        haplotype_pool=haplotype_pool,
        haplotype_to_phenotype=haplotype_to_phenotype,
        mutation_rate=mutation_rate,
        environment_schedule=env_schedule
    )

    for step in range(len(env_schedule)):
        print(f"[DEBUG] Step {step} mulai")
        model.step()
        print(f"[DEBUG] Step {step} selesai, populasi: {len(model.agent_list)}")

    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    df = model.datacollector.get_model_vars_dataframe().reset_index()
    output_path = os.path.join(output_dir, "simulation_output.csv")
    df.to_csv(output_path, index=False)
    print(f"Simulasi selesai. Hasil disimpan di: {output_path}")
    
    return df

if __name__ == "__main__":
    run_simulation()
