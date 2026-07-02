#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_duality_charts.py — Γραφήματα δυϊκής ανάλυσης (LP duality).

Παράγει δύο γραφήματα που αποτυπώνουν την οικονομική ερμηνεία της δυϊκότητας:

  • chart_09_reduced_cost.png  — Ανάλυση μειωμένου κόστους των αποκλειόμενων
    πιάτων: περιθώριο m_d έναντι κόστους ευκαιρίας εργασίας (t_d/60)·u*.
    Δείχνει ΓΙΑΤΙ κάθε πιάτο μένει εκτός (κόστος ευκαιρίας > περιθώριο).

  • chart_10_demand_shadow.png — Σκιώδεις τιμές ζήτησης v_d για τα πιάτα που
    παράγονται στο όριο D_d^max: οριακή αξία μίας επιπλέον μονάδας ζήτησης
    (προτεραιότητα διαφήμισης / marketing).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from data import DISHES, PARAMS, contribution_margin
from duality import full_duality_report

plt.rcParams.update({
    "font.size": 10, "font.family": "DejaVu Sans",
    "axes.labelsize": 11, "axes.titlesize": 13,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
})
NAVY = "#1F4E78"; ORANGE = "#C55A11"; GREEN = "#2E7D32"
RED = "#B00020"; GRAY = "#8A8A8A"

rep = full_duality_report()
u = rep["labor_shadow_price"]
wage = rep["labor_wage"]
print(f"Labor shadow price u* = {u:.2f} €/h  (wage = {wage:.2f} €/h)")
print(f"Strong duality: Z*={rep['primal_objective']}  W*={rep['dual_objective']}  gap={rep['duality_gap']}")

# ═════════════════════════════════════════════════════════════════════
# CHART 9 — Reduced cost decomposition of EXCLUDED dishes
# ═════════════════════════════════════════════════════════════════════
excluded = [r for r in rep["dishes"] if not r["produced"]]
excluded.sort(key=lambda r: r["reduced_cost_solver"])   # πιο αρνητικό πρώτο

names = [r["name"] for r in excluded]
margins = [r["margin"] for r in excluded]
opp_labor = [(DISHES[r["code"]]["labor_min"] / 60.0) * u for r in excluded]
reduced = [r["reduced_cost_solver"] for r in excluded]

y = np.arange(len(names))
fig, ax = plt.subplots(figsize=(11, 7))
ax.barh(y + 0.2, margins, 0.4, color=GREEN, label=r"Περιθώριο $m_d$ (€/μερίδα)")
ax.barh(y - 0.2, opp_labor, 0.4, color=RED, alpha=0.8,
        label=r"Κόστος ευκαιρίας εργασίας $(t_d/60)\,u^*$")

for i, r in enumerate(reduced):
    ax.text(max(margins[i], opp_labor[i]) + 0.15, y[i],
            f"r={r:.2f}€", va="center", fontsize=9, fontweight="bold", color=NAVY)

ax.set_yticks(y); ax.set_yticklabels(names, fontsize=9)
ax.invert_yaxis()
ax.set_xlabel("€ ανά μερίδα", fontweight="bold")
ax.set_title("Γιατί αποκλείονται πιάτα: μειωμένο κόστος (LP duality)\n"
             f"Κόστος ευκαιρίας εργασίας (u*={u:.2f} €/ώρα) > Περιθώριο  ⇒  "
             r"$r_d = m_d-(t_d/60)u^* < 0$",
             color=NAVY, fontweight="bold", fontsize=12)
ax.grid(True, axis="x", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
ax.legend(loc="lower right", fontsize=10)
fig.tight_layout()
fig.savefig("chart_09_reduced_cost.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 9: reduced-cost decomposition of excluded dishes")

# ═════════════════════════════════════════════════════════════════════
# CHART 10 — Demand shadow prices for dishes at their demand cap
# ═════════════════════════════════════════════════════════════════════
capped = [r for r in rep["dishes"] if r["demand_shadow"] > 1e-4]
capped.sort(key=lambda r: r["demand_shadow"], reverse=True)

cnames = [r["name"] for r in capped]
vshadow = [r["demand_shadow"] for r in capped]

x = np.arange(len(cnames))
fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(x, vshadow, 0.62, color=ORANGE, edgecolor=NAVY, linewidth=1.2)
for xi, v in zip(x, vshadow):
    ax.text(xi, v + 0.08, f"{v:.2f}€", ha="center", va="bottom",
            fontsize=9, fontweight="bold", color=NAVY)

ax.set_xticks(x); ax.set_xticklabels(cnames, rotation=40, ha="right", fontsize=9)
ax.set_ylabel(r"Σκιώδης τιμή ζήτησης $v_d$ (€/μερίδα)", fontweight="bold")
ax.set_title("Οριακή αξία επιπλέον ζήτησης (σκιώδεις τιμές $v_d$)\n"
             "Πιάτα στο όριο $D_d^{\\max}$: πού αποδίδει περισσότερο η διαφήμιση/marketing",
             color=NAVY, fontweight="bold", fontsize=12)
ax.grid(True, axis="y", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("chart_10_demand_shadow.png", dpi=150, bbox_inches="tight")
plt.close()
print("✓ Chart 10: demand shadow prices (marketing value)")
print("\n✓ Duality charts saved: chart_09_reduced_cost.png, chart_10_demand_shadow.png")
