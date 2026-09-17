from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

demand = pd.read_csv(ROOT / "data" / "demand.csv")
sources = pd.read_csv(ROOT / "data" / "sources.csv")

fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.plot(demand["year"], demand["base_total_t"], marker="o", label="Базовый общий")
ax.plot(demand["year"], demand["base_critical_t"], marker="o", label="Базовый критический")
ax.plot(demand["year"], demand["low_total_t"], marker="o", label="Низкий общий")
ax.plot(demand["year"], demand["high_total_t"], marker="o", label="Высокий общий")
ax.set_xlabel("Год")
ax.set_ylabel("т/год")
ax.set_title("Исходные траектории спроса")
ax.grid(True, alpha=0.25)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "demand_scenarios.svg")
plt.close(fig)

fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.scatter(sources["max_capacity_tpy"], sources["variable_cost_m_per_t"], s=70)
for _, row in sources.iterrows():
    ax.annotate(row["source_id"], (row["max_capacity_tpy"], row["variable_cost_m_per_t"]), xytext=(5, 5), textcoords="offset points")
ax.set_xlabel("Максимальная мощность, т/год")
ax.set_ylabel("Переменная стоимость, млн у.е./т")
ax.set_title("Каналы снабжения: мощность и переменная стоимость")
ax.grid(True, alpha=0.25)
fig.tight_layout()
fig.savefig(OUT / "source_tradeoff.svg")
plt.close(fig)

stress = demand[["year", "base_total_t"]].copy()
stress["mandatory_stress_total_t"] = stress["base_total_t"].astype(float)
stress.loc[stress["year"] >= 2038, "mandatory_stress_total_t"] *= 1.15
fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.plot(stress["year"], stress["base_total_t"], marker="o", label="Стандарт")
ax.plot(stress["year"], stress["mandatory_stress_total_t"], marker="o", label="Обязательный стресс")
ax.set_xlabel("Год")
ax.set_ylabel("Общий спрос, т/год")
ax.set_title("Что меняет обязательный стресс в спросе")
ax.grid(True, alpha=0.25)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "mandatory_stress_demand.svg")
plt.close(fig)

print(f"Wrote figures to {OUT}")
