# MothAgent.py

import random

class MothAgent:
    def __init__(self, unique_id, model, haplotype_id, phenotype):
        # Hilangkan super().__init__; kita simpan unique_id dan model sendiri
        self.unique_id = unique_id
        self.model = model
        self.haplotype_id = haplotype_id
        self.phenotype = phenotype
        self.fitness = 1.0

    def step(self):
        # 1. Hitung ulang fitness sebelum apa pun
        self.calculate_fitness()

        # 2. Mutasi dengan probabilitas mutation_rate
        if random.random() < self.model.mutation_rate:
            possible = list(self.model.haplotype_pool.keys())
            new_hid = random.choice(possible)
            self.haplotype_id = new_hid
            self.phenotype = self.model.haplotype_to_phenotype[new_hid]
            # Hitung ulang fitness setelah mutasi
            self.calculate_fitness()

        # 3. Jika fitness di bawah threshold, agen mati
        if self.fitness < 0.1:
            if self in self.model.agent_list:
                self.model.agent_list.remove(self)
            return  # agen sudah "mati", berhenti di sini

        # 4. Reproduksi dengan probabilitas tergantung fitness × environmental_pressure
        reproduce_prob = self.fitness * self.model.environmental_pressure
        if random.random() < reproduce_prob:
            new_id = self.model.next_id()
            child = MothAgent(new_id, self.model, self.haplotype_id, self.phenotype)
            self.model.agent_list.append(child)

    def calculate_fitness(self):
        """
        Contoh skema fitness:
        - 'dark' lebih fit saat environmental_pressure tinggi
        - 'light' lebih fit saat environmental_pressure rendah
        """
        env = self.model.environmental_pressure
        if self.phenotype == "dark":
            self.fitness = 1.0 * env + 0.5 * (1 - env)
        else:  # 'light'
            self.fitness = 0.5 * env + 1.0 * (1 - env)
