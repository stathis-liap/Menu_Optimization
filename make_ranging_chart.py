#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_ranging_chart.py — Παραμετρικό γράφημα του LP ως προς τις εργατοώρες H.

Παράγει το chart_11_parametric_labor.png: την τμηματικά γραμμική καμπύλη
κέρδους(H) του LP, με επισήμανση του διαστήματος εύρους [H_low, H_high] μέσα στο
οποίο η σκιώδης τιμή u* = 20,37 €/ώρα παραμένει σταθερή (κλίση της καμπύλης).
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from duality import solve_primal_with_duals
from ranging import labor_rhs_range

plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans",
                     "axes.labelsize": 11, "axes.titlesize": 13})
NAVY = "#1F4E78"; ORANGE = "#C55A11"; GREEN = "#2E7D32"; RED = "#B00020"

H0 = 65.0
Hs = np.arange(20, 130.5, 1.0)
profits, shadows = [], []
for H in Hs:
    r = solve_primal_with_duals(float(H))
    profits.append(r["objective"])
    shadows.append(r["labor_shadow"])

rr = labor_rhs_range(H0)
base = solve_primal_with_duals(H0)

fig, ax = plt.subplots(figsize=(10, 5.6))
ax.plot(Hs, profits, "-", color=NAVY, linewidth=2.4, label="Κέρδος LP (τμηματικά γραμμικό)")

# Επισήμανση του διαστήματος εύρους (σταθερή σκιώδης τιμή / κλίση)
ax.axvspan(rr["H_low"], rr["H_high"], color=GREEN, alpha=0.15,
           label=f"Εύρος σταθερού $u^*$: [{rr['H_low']:.1f}, {rr['H_high']:.1f}] ώρες")
ax.axvline(H0, color=RED, linestyle="--", linewidth=1.3, alpha=0.8)
ax.scatter([H0], [base["objective"]], s=140, color=RED, marker="*", zorder=6,
           edgecolors="black", linewidth=1, label=f"Τρέχον σημείο ($H=65$)")

# Σχολιασμός κλίσης = σκιώδης τιμή
ax.annotate(f"κλίση = $u^*$ = {rr['shadow']:.2f} €/ώρα",
            xy=(H0, base["objective"]),
            xytext=(H0 - 34, base["objective"] + 250),
            fontsize=11, color=NAVY, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=NAVY))

ax.set_xlabel("Διαθέσιμες εργατοώρες $H$", fontweight="bold")
ax.set_ylabel("Βέλτιστο κέρδος LP (€/ημέρα)", fontweight="bold")
ax.set_title("Παραμετρική ανάλυση: κέρδος LP ως προς $H$\n"
             "Η σκιώδης τιμή είναι η κλίση· ισχύει σε πεπερασμένο εύρος (RHS ranging)",
             color=NAVY, fontweight="bold", fontsize=12)
ax.grid(True, alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
ax.legend(loc="lower right", fontsize=9)
fig.tight_layout()
fig.savefig("chart_11_parametric_labor.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"✓ chart_11_parametric_labor.png  (range [{rr['H_low']:.2f}, {rr['H_high']:.2f}], "
      f"u*={rr['shadow']:.2f})")
