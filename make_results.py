"""
make_results.py — Εκτέλεση όλων των βελτιστοποιήσεων και ανάλυσης ευαισθησίας.
Αποθηκεύει τα αποτελέσματα σε JSON για περαιτέρω επεξεργασία (αναφορές, γραφήματα).
"""

from optimize import (
    solve_lp, solve_mip, 
    sensitivity_waste, sensitivity_labor_hours, 
    sensitivity_material_cost, sensitivity_menu_size,
    variable_cost_per_portion, contribution_margin
)
from data import DISHES, ingredient_cost_per_portion, labor_cost_per_portion
import json

# ─────────────────────────────────────────────────────────────────────────────
# ΚΎΡΙΑ ΒΕΛΤΙΣΤΟΠΟΙΗΣΗ
# ─────────────────────────────────────────────────────────────────────────────
lp = solve_lp(verbose=False)
mip = solve_mip(verbose=False)

# ─────────────────────────────────────────────────────────────────────────────
# ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ
# ─────────────────────────────────────────────────────────────────────────────
sw = sensitivity_waste([0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.20])
slh = sensitivity_labor_hours([40, 50, 60, 65, 70, 80])
smc = sensitivity_material_cost([0.75, 0.85, 0.95, 1.0, 1.05, 1.15, 1.25, 1.5])
sms = sensitivity_menu_size([4, 6, 8], [6, 8, 10, 12])

# ─────────────────────────────────────────────────────────────────────────────
# ΟΙΚΟΝΟΜΙΚΗ ΑΝΑΛΥΣΗ ΠΙΑΤΩΝ
# ─────────────────────────────────────────────────────────────────────────────
econ = {
    d: {
        "name": DISHES[d]["name"],
        "category": DISHES[d].get("category", "άλλο"),
        "price": DISHES[d]["price"],
        "ingredient_cost": round(ingredient_cost_per_portion(d), 3),
        "labor_cost": round(labor_cost_per_portion(d), 3),
        "variable_cost": round(variable_cost_per_portion(d), 3),
        "contribution_margin": round(contribution_margin(d), 3),
        "margin_percentage": round(100 * contribution_margin(d) / DISHES[d]["price"], 1),
        "fixed_setup_cost": DISHES[d]["fixed_setup"],
        "demand_min": DISHES[d]["demand_min"],
        "demand_max": DISHES[d]["demand_max"],
        "labor_min": DISHES[d]["labor_min"],
    }
    for d in DISHES
}

# ─────────────────────────────────────────────────────────────────────────────
# ΔΗΜΙΟΥΡΓΙΑ ΕΞΌΔΟΥ
# ─────────────────────────────────────────────────────────────────────────────
out = {
    "metadata": {
        "title": "Restaurant Menu Optimization - Linear & Mixed Integer Programming",
        "timestamp": "2026-05-01",
        "version": "2.0 (Extended)"
    },
    "models": {
        "lp": lp,
        "mip": mip,
    },
    "sensitivity": {
        "waste": sw,
        "labor_hours": slh,
        "material_cost": smc,
        "menu_size": sms,
    },
    "economic_analysis": econ,
}

# ─────────────────────────────────────────────────────────────────────────────
# ΑΠΟΘΗΚΕΥΣΗ
# ─────────────────────────────────────────────────────────────────────────────
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("✓ results.json saved successfully")
print(f"  - LP profit: {lp['profit']:.2f}€")
print(f"  - MIP profit: {mip['profit']:.2f}€")
print(f"  - Dishes in MIP menu: {sum(mip['on_menu'].values())}")
print(f"  - Sensitivity analyses: 4 types completed")
