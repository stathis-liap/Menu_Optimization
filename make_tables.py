#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_tables.py — Παράγει τα αριθμητικά πινακάκια (LaTeX fragments) της αναφοράς
απευθείας από τη βάση δεδομένων και τους επιλύτες, ώστε κάθε αριθμός στην αναφορά
να ταυτίζεται ΑΚΡΙΒΩΣ με τον κώδικα.

Κάθε αρχείο περιέχει ΠΛΗΡΕΣ περιβάλλον \\begin{tabular}...\\end{tabular} και
συμπεριλαμβάνεται με \\input σε κανονική κατάσταση (εκτός στοίχισης), ώστε να
αποφεύγονται προβλήματα \\input εντός \\halign. Τα αρχεία τοποθετούνται στο
report/tables/.
"""

import os
from data import (DISHES, INGREDIENTS, PARAMS,
                  ingredient_cost_per_portion, labor_cost_per_portion,
                  variable_cost_per_portion, contribution_margin,
                  margin_per_labor_hour)
from optimize import (solve_lp, solve_mip, sensitivity_labor_hours,
                      sensitivity_material_cost, sensitivity_waste,
                      integrality_gap)
from duality import full_duality_report
from ranging import labor_rhs_range, objective_ranging

OUT = os.path.join("report", "tables")
os.makedirs(OUT, exist_ok=True)


def gr(x, dec=2):
    """Μορφοποίηση αριθμού με ελληνικό δεκαδικό κόμμα (και εξάλειψη θορύβου -0,00)."""
    if abs(x) < 0.5 * 10 ** (-dec):
        x = 0.0
    return f"{x:.{dec}f}".replace(".", ",")


_TEX_ESCAPE = {"&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#", "_": "\\_"}


def tex(s):
    """Διαφυγή ειδικών χαρακτήρων LaTeX σε ονόματα (π.χ. % στο «3,6% λιπαρά»)."""
    return "".join(_TEX_ESCAPE.get(c, c) for c in str(s))


def write(name, text):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  ✓ {os.path.join(OUT, name)}")


def tabular(colspec, header, body_rows, tabcolsep=None):
    """Δημιουργεί πλήρες περιβάλλον tabular με booktabs κανόνες."""
    parts = []
    if tabcolsep is not None:
        parts.append(f"\\setlength{{\\tabcolsep}}{{{tabcolsep}}}")
    parts.append(f"\\begin{{tabular}}{{{colspec}}}")
    parts.append("\\toprule")
    parts.append(header + " \\\\")
    parts.append("\\midrule")
    parts.extend(body_rows)
    parts.append("\\bottomrule")
    parts.append("\\end{tabular}")
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# 1. ΠΙΝΑΚΑΣ ΠΡΩΤΩΝ ΥΛΩΝ (δύο πλήρεις tabular: αριστερά / δεξιά)
# ---------------------------------------------------------------------------
CATEGORY_TITLES = {
    "κρέατα": "Κρέατα \\& πρωτεΐνες",
    "θαλασσινά": "Θαλασσινά",
    "λαχανικά": "Λαχανικά φρέσκα",
    "δημητριακά": "Δημητριακά \\& αμυλούχα",
    "γαλακτοκομικά": "Γαλακτοκομικά",
    "βασικά": "Βασικά \\& μυρωδικά",
    "μυρωδικά": "Βασικά \\& μυρωδικά",
    "κονδύλοι": "Κονσέρβες \\& επεξεργασμένα",
}
ING_HEADER = "\\textbf{Πρώτη ύλη} & \\textbf{Μον.} & \\textbf{€}"
ING_COLSPEC = "@{}p{5.2cm}cr@{}"


def _group_rows(title, items):
    rows = [f"\\multicolumn{{3}}{{@{{}}l}}{{\\textbf{{{title}}}}}\\\\"]
    for ing in items:
        rows.append(f"\\quad {tex(ing['name'])} & {ing['unit']} & {gr(ing['price'],2)} \\\\")
    return rows


def table_ingredients():
    order, groups = [], {}
    for ing in INGREDIENTS.values():
        title = CATEGORY_TITLES.get(ing["category"], ing["category"])
        groups.setdefault(title, [])
        if title not in order:
            order.append(title)
        groups[title].append(ing)

    left, right = [], []
    side = left
    for title in order:
        if title == "Γαλακτοκομικά":
            side = right
        side.extend(_group_rows(title, groups[title]))
        side.append("\\addlinespace")

    write("tbl_ingredients_L.tex",
          tabular(ING_COLSPEC, ING_HEADER, left, tabcolsep="4pt"))
    write("tbl_ingredients_R.tex",
          tabular(ING_COLSPEC, ING_HEADER, right, tabcolsep="4pt"))


# ---------------------------------------------------------------------------
# 2. ΣΥΓΚΕΝΤΡΩΤΙΚΟΣ ΠΙΝΑΚΑΣ ΚΟΣΤΟΛΟΓΗΣΗΣ (ταξ. κατά ρ) + LP/MIP
# ---------------------------------------------------------------------------
def table_costing():
    lp = solve_lp(verbose=False)
    mip = solve_mip(verbose=False)
    order = sorted(DISHES, key=lambda d: margin_per_labor_hour(d), reverse=True)
    rows = []
    for d in order:
        lp_flag = "\\checkmark" if lp["on_menu"][d] else "--"
        mip_flag = "\\checkmark" if mip["on_menu"][d] else "--"
        rows.append(
            f"{tex(DISHES[d]['name'])} & {gr(DISHES[d]['price'],1)} & "
            f"{gr(ingredient_cost_per_portion(d),2)} & {gr(labor_cost_per_portion(d),2)} & "
            f"{gr(variable_cost_per_portion(d),2)} & {gr(contribution_margin(d),2)} & "
            f"{gr(margin_per_labor_hour(d),2)} & {gr(DISHES[d]['fixed_setup'],0)} & "
            f"{lp_flag} & {mip_flag} \\\\")
    header = ("\\textbf{Πιάτο} & $P$ & $\\mu$ & $\\lambda$ & $C$ & $m$ & $\\rho$ & "
              "$f$ & \\textbf{\\en{LP}} & \\textbf{\\en{MIP}}")
    write("tbl_costing.tex",
          tabular("@{}lrrrrrrrcc@{}", header, rows, tabcolsep="4.4pt"))


# ---------------------------------------------------------------------------
# 3. ΠΙΝΑΚΑΣ ΔΥΪΚΟΤΗΤΑΣ
# ---------------------------------------------------------------------------
def table_duality():
    rep = full_duality_report()
    prod = sorted([r for r in rep["dishes"] if r["produced"]],
                  key=lambda r: r["demand_shadow"], reverse=True)
    excl = sorted([r for r in rep["dishes"] if not r["produced"]],
                  key=lambda r: r["reduced_cost_solver"])

    def row(r, state):
        return (f"{tex(r['name'])} & {gr(r['margin'],2)} & {r['labor_min']} & "
                f"{gr(r['portions'],1)} & {gr(r['reduced_cost_solver'],2)} & "
                f"{gr(r['demand_shadow'],2)} & {state} \\\\")

    rows = [row(r, "παράγεται") for r in prod]
    rows.append("\\addlinespace")
    rows += [row(r, "αποκλείεται") for r in excl]
    header = ("\\textbf{Πιάτο} & $m$ & $t$ & $x^\\star$ & $r$ & $v$ & \\textbf{Κατάσταση}")
    write("tbl_duality.tex", tabular("@{}lrrrrrl@{}", header, rows, tabcolsep="6pt"))

    macros = [
        f"\\newcommand{{\\LPobj}}{{{gr(rep['primal_objective'],2)}}}",
        f"\\newcommand{{\\DUALobj}}{{{gr(rep['dual_objective'],2)}}}",
        f"\\newcommand{{\\LaborShadow}}{{{gr(rep['labor_shadow_price'],2)}}}",
        f"\\newcommand{{\\LaborWage}}{{{gr(rep['labor_wage'],2)}}}",
    ]
    write("duality_macros.tex", "\n".join(macros) + "\n")


# ---------------------------------------------------------------------------
# 4. ΕΥΑΙΣΘΗΣΙΑ — ΕΡΓΑΤΟΩΡΕΣ (με οριακό όφελος)
# ---------------------------------------------------------------------------
def table_labor():
    hours = [40, 50, 60, 65, 70, 80, 90, 100, 120]
    rows, prev = [], None
    for r in sensitivity_labor_hours(hours):
        h, profit, used = r["labor_hours"], r["profit"], r["labor_used"]
        marg = "--" if prev is None else gr((profit - prev[1]) / (h - prev[0]), 2)
        b = "\\bfseries " if h == 65 else ""
        rows.append(f"{b}{h} & {b}{gr(profit,2)} & {b}{gr(used,1)} & {b}{marg} \\\\")
        prev = (h, profit)
    header = ("$H$ (ώρες) & \\textbf{Κέρδος (€)} & \\textbf{Ώρες σε χρήση} & "
              "\\textbf{Οριακό όφελος (€/ώρα)}")
    write("tbl_sens_labor.tex", tabular("@{}rrrr@{}", header, rows))


# ---------------------------------------------------------------------------
# 5. ΕΥΑΙΣΘΗΣΙΑ — ΜΕΓΕΘΟΣ ΜΕΝΟΥ (χαλάρωση N_max)
# ---------------------------------------------------------------------------
def table_menu():
    rows = []
    for nmax in [6, 8, 10, 12, 21]:
        r = solve_mip(min_dishes=min(6, nmax), max_dishes=nmax, verbose=False)
        label = str(nmax) if nmax != 21 else "21 (χωρίς όριο)"
        rows.append(f"{label} & {sum(r['on_menu'].values())} & {gr(r['profit'],2)} \\\\")
    header = "$N_{\\max}$ & \\textbf{Επιλεγμένα πιάτα} & \\textbf{Κέρδος (€)}"
    write("tbl_sens_menu.tex", tabular("@{}lrr@{}", header, rows))


# ---------------------------------------------------------------------------
# 6. ΕΥΑΙΣΘΗΣΙΑ — ΚΟΣΤΟΣ ΥΛΙΚΩΝ & ΣΠΑΤΑΛΗ
# ---------------------------------------------------------------------------
def table_cost_waste():
    rows = []
    for r in sensitivity_material_cost([0.75, 0.85, 0.95, 1.0, 1.05, 1.15, 1.25, 1.5]):
        b = "\\bfseries " if abs(r["cost_multiplier"] - 1.0) < 1e-9 else ""
        rows.append(f"{b}$\\times${gr(r['cost_multiplier'],2)} & {b}{gr(r['profit'],2)} & "
                    f"{b}{r['n_dishes']} \\\\")
    header = "\\textbf{Πολ/στής} & \\textbf{Κέρδος (€)} & \\textbf{Πιάτα}"
    write("tbl_sens_material.tex", tabular("@{}lrr@{}", header, rows))

    rows = []
    for r in sensitivity_waste([0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.20]):
        b = "\\bfseries " if abs(r["waste_fraction"] - 0.06) < 1e-9 else ""
        rows.append(f"{b}{gr(r['waste_fraction']*100,1)}\\% & {b}{gr(r['profit'],2)} & "
                    f"{b}{r['n_dishes']} \\\\")
    header = "\\textbf{Σπατάλη} & \\textbf{Κέρδος (€)} & \\textbf{Πιάτα}"
    write("tbl_sens_waste.tex", tabular("@{}lrr@{}", header, rows))


# ---------------------------------------------------------------------------
# 7. ΠΙΝΑΚΑΣ ΕΥΡΟΥΣ ΣΥΝΤΕΛΕΣΤΩΝ ΑΝΤΙΚΕΙΜΕΝΙΚΗΣ (objective coefficient ranging)
#    + μακροεντολές RHS ranging και διακένου ακεραιότητας
# ---------------------------------------------------------------------------
def _inf(v, dec=2):
    return "$\\infty$" if v == float("inf") else gr(v, dec)


def table_ranging():
    obj = objective_ranging()
    prod = sorted([r for r in obj if r["produced"]], key=lambda z: -z["margin"])
    excl = sorted([r for r in obj if not r["produced"]], key=lambda z: -z["allow_increase"])

    def row(r, state):
        return (f"{tex(r['name'])} & {gr(r['margin'],2)} & {state} & "
                f"{_inf(r['allow_increase'])} & {_inf(r['allow_decrease'])} \\\\")

    rows = [row(r, "παράγεται") for r in prod]
    rows.append("\\addlinespace")
    rows += [row(r, "αποκλείεται") for r in excl]
    header = ("\\textbf{Πιάτο} & $m$ & \\textbf{Κατάσταση} & "
              "\\textbf{Επιτρ. αύξηση} & \\textbf{Επιτρ. μείωση}")
    write("tbl_ranging.tex", tabular("@{}lrlrr@{}", header, rows, tabcolsep="6pt"))

    # Μακροεντολές για το κείμενο
    rr = labor_rhs_range()
    ig = integrality_gap()
    frac = ", ".join(tex(DISHES[d]["name"]) for d in ig["fractional_y"])
    macros = [
        f"\\newcommand{{\\Hlow}}{{{gr(rr['H_low'],2)}}}",
        f"\\newcommand{{\\Hhigh}}{{{gr(rr['H_high'],2)}}}",
        f"\\newcommand{{\\Hdec}}{{{gr(rr['allowable_decrease'],2)}}}",
        f"\\newcommand{{\\Hinc}}{{{gr(rr['allowable_increase'],2)}}}",
        f"\\newcommand{{\\RelaxBound}}{{{gr(ig['relaxation_bound'],2)}}}",
        f"\\newcommand{{\\IntOpt}}{{{gr(ig['integer_optimum'],2)}}}",
        f"\\newcommand{{\\IntGap}}{{{gr(ig['gap_absolute'],2)}}}",
        f"\\newcommand{{\\IntGapPct}}{{{gr(ig['gap_percent'],2)}}}",
        f"\\newcommand{{\\FracDishes}}{{{frac}}}",
    ]
    write("ranging_macros.tex", "\n".join(macros) + "\n")


if __name__ == "__main__":
    print("Παραγωγή πινάκων LaTeX...")
    table_ingredients()
    table_costing()
    table_duality()
    table_labor()
    table_menu()
    table_cost_waste()
    table_ranging()
    print("Όλοι οι πίνακες παρήχθησαν στο", OUT)
