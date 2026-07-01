import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from optimize import sensitivity_waste, sensitivity_material_cost, solve_lp, solve_mip
from data import DISHES

plt.rcParams.update({"font.size": 11, "font.family": "DejaVu Sans"})
BLUE = "#1F4E78"; ORANGE = "#C55A11"

# 1. Ευαισθησία σπατάλης
w = sensitivity_waste([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot([r["waste_fraction"]*100 for r in w], [r["profit"] for r in w],
        "o-", color=BLUE, linewidth=2, markersize=7)
ax.set_xlabel("Ποσοστό σπατάλης (%)"); ax.set_ylabel("Βέλτιστο κέρδος (€/ημέρα)")
ax.set_title("Ανάλυση Ευαισθησίας: Επίδραση Σπατάλης στο Κέρδος", color=BLUE, fontweight="bold")
ax.grid(True, alpha=0.3); fig.tight_layout()
fig.savefig("chart_waste.png", dpi=140); plt.close()

# 2. Ευαισθησία κόστους υλικών
m = sensitivity_material_cost([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5])
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot([r["cost_multiplier"] for r in m], [r["profit"] for r in m],
        "s-", color=ORANGE, linewidth=2, markersize=7)
ax.set_xlabel("Πολλαπλασιαστής κόστους πρώτων υλών (×)"); ax.set_ylabel("Βέλτιστο κέρδος (€/ημέρα)")
ax.set_title("Ανάλυση Ευαισθησίας: Επίδραση Κόστους Υλικών", color=ORANGE, fontweight="bold")
ax.axvline(1.0, color="gray", linestyle="--", alpha=0.6)
ax.grid(True, alpha=0.3); fig.tight_layout()
fig.savefig("chart_material.png", dpi=140); plt.close()

# 3. Σύγκριση λύσης LP vs MIP (μερίδες ανά πιάτο)
lp = solve_lp(verbose=False); mip = solve_mip(verbose=False)
names = [DISHES[d]["name"] for d in DISHES]
import numpy as np
x = np.arange(len(names)); width = 0.38
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(x - width/2, [lp["portions"][d] for d in DISHES], width, label="LP", color=BLUE)
ax.bar(x + width/2, [mip["portions"][d] for d in DISHES], width, label="MIP", color=ORANGE)
ax.set_ylabel("Μερίδες/ημέρα"); ax.set_xticks(x); ax.set_xticklabels(names, rotation=30, ha="right")
ax.set_title("Σύγκριση Βέλτιστης Παραγωγής: LP vs MIP", color=BLUE, fontweight="bold")
ax.legend(); ax.grid(True, axis="y", alpha=0.3); fig.tight_layout()
fig.savefig("chart_lp_mip.png", dpi=140); plt.close()
print("charts saved")
