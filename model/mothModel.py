from mesa import Model  
from mesa.datacollection import DataCollector
from .MothAgent import MothAgent
import random

class MothModel(Model):
    def __init__(
        self,
        N_initial,
        haplotype_pool,
        haplotype_to_phenotype,
        mutation_rate,
        environment_schedule,
        max_fitness_value=1.5
    ):
        super().__init__()
        self.haplotype_pool = haplotype_pool
        self.haplotype_to_phenotype = haplotype_to_phenotype
        self.mutation_rate = mutation_rate
        self.max_fitness_value = max_fitness_value

        self.environment_schedule = environment_schedule
        self.current_step = 0
        self.environmental_pressure = self.environment_schedule[0]

        self.agent_list = []

        for _ in range(N_initial):
            self.add_initial_agent()

        self.datacollector = DataCollector(
            model_reporters={
                "Diversity": self.compute_shannon_diversity,
                "Population": lambda m: len(m.agent_list),
                "Freq_Light": lambda m: m.count_phenotype("light"),
                "Freq_Dark": lambda m: m.count_phenotype("dark"),
            },
            agent_reporters={
                "haplotype": "haplotype_id",
                "fitness": "fitness"
            }
        )
        self.datacollector.collect(self)

    def add_initial_agent(self):
        hap_ids = list(self.haplotype_pool.keys())
        freqs = [self.haplotype_pool[h]["frequency"] for h in hap_ids]
        chosen = random.choices(hap_ids, weights=freqs, k=1)[0]
        phenotype = self.haplotype_to_phenotype[chosen]

        a = MothAgent(self.next_id(), self, chosen, phenotype)
        self.agent_list.append(a)

    def step(self):
        if self.current_step < len(self.environment_schedule):
            self.environmental_pressure = self.environment_schedule[self.current_step]

        self.datacollector.collect(self)

        random.shuffle(self.agent_list)

        for agent in list(self.agent_list):
            agent.step()

        self.current_step += 1

    def compute_shannon_diversity(self):
        counts = {}
        for agent in self.agent_list:
            h = agent.haplotype_id
            counts[h] = counts.get(h, 0) + 1
        total = sum(counts.values())
        import math
        H = 0.0
        for c in counts.values():
            p = c / total
            H -= p * math.log(p) if p > 0 else 0
        return H

    def count_phenotype(self, phenotype_label):
        return sum(1 for a in self.agent_list if a.phenotype == phenotype_label)

    def next_id(self):
        self.num_agents = getattr(self, "num_agents", 0) + 1
        return self.num_agents
