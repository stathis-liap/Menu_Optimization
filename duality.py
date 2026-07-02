"""
duality.py — Δυϊκή ανάλυση του Γραμμικού Προγράμματος (LP) βελτιστοποίησης μενού.

Το αρχείο αυτό αποτελεί ΘΕΩΡΗΤΙΚΗ ΕΠΕΚΤΑΣΗ του βασικού μοντέλου: αντλεί και
ερμηνεύει την πλήρη δυϊκή πληροφορία της βέλτιστης λύσης του LP. Καλύπτονται
τα κεντρικά εργαλεία της θεωρίας Γραμμικού Προγραμματισμού:

  1. ΔΥΪΚΟ ΠΡΟΒΛΗΜΑ (dual)      — ρητή διατύπωση και ανεξάρτητη επίλυση.
  2. ΣΚΙΩΔΕΙΣ ΤΙΜΕΣ (shadow prices / dual values) των περιορισμών.
  3. ΜΕΙΩΜΕΝΟ ΚΟΣΤΟΣ (reduced costs) των μεταβλητών.
  4. ΙΣΧΥΡΗ ΔΥΪΚΟΤΗΤΑ (strong duality): Z*_πρωτεύον = Z*_δυϊκό.
  5. ΣΥΜΠΛΗΡΩΜΑΤΙΚΗ ΧΑΛΑΡΟΤΗΤΑ (complementary slackness).

═════════════════════════════════════════════════════════════════════════════

ΠΡΩΤΕΥΟΝ ΠΡΟΒΛΗΜΑ (Primal LP — Μοντέλο Α)
─────────────────────────────────────────
  max  Z = Σ_d m_d · x_d
  υπό:
       Σ_d (t_d/60) · x_d ≤ H            (εργατοώρες)          [δυϊκή u ≥ 0]
       x_d ≤ D_d^max            ∀d        (μέγιστη ζήτηση)      [δυϊκή v_d ≥ 0]
       x_d ≥ 0                  ∀d

ΔΥΪΚΟ ΠΡΟΒΛΗΜΑ (Dual LP)
────────────────────────
  min  W = H · u + Σ_d D_d^max · v_d
  υπό:
       (t_d/60) · u + v_d ≥ m_d          ∀d   (μία ανά πρωτεύουσα μεταβλητή x_d)
       u ≥ 0,  v_d ≥ 0

ΟΙΚΟΝΟΜΙΚΗ ΕΡΜΗΝΕΙΑ:
  u   = σκιώδης τιμή της εργασίας = οριακή αξία μίας επιπλέον εργατοώρας (€/ώρα).
  v_d = σκιώδης τιμή της ζήτησης του πιάτου d = οριακή αξία μίας επιπλέον
        μονάδας ζήτησης (€/μερίδα) — δηλαδή πόσο θα άξιζε επιπλέον διαφήμιση.
  Μειωμένο κόστος r_d = m_d - [(t_d/60)·u + v_d] :
        για πιάτο που ΔΕΝ παράγεται (x_d = 0) ισχύει r_d ≤ 0· το |r_d| είναι
        το ΚΟΣΤΟΣ ΕΥΚΑΙΡΙΑΣ — πόσο θα ΜΕΙΩΝΟΤΑΝ το κέρδος αν επιβάλλαμε την
        παραγωγή μίας μερίδας του d.
═════════════════════════════════════════════════════════════════════════════
"""

import pulp
from data import DISHES, PARAMS, contribution_margin


# ---------------------------------------------------------------------------
# 1. ΕΠΙΛΥΣΗ ΠΡΩΤΕΥΟΝΤΟΣ LP ΚΑΙ ΕΞΑΓΩΓΗ ΔΥΪΚΗΣ ΠΛΗΡΟΦΟΡΙΑΣ
# ---------------------------------------------------------------------------
def solve_primal_with_duals(labor_hours=None):
    """
    Επιλύει το πρωτεύον LP και εξάγει σκιώδεις τιμές (constraint.pi) και
    μειωμένα κόστη (variable.dj) απευθείας από τον επιλύτη CBC.

    Returns:
        dict με κλειδιά: objective, portions, labor_shadow, demand_shadow,
                          reduced_cost, labor_used
    """
    if labor_hours is None:
        labor_hours = PARAMS["labor_hours_available"]

    prob = pulp.LpProblem("Menu_LP_primal", pulp.LpMaximize)
    x = {d: pulp.LpVariable(f"x_{d}", lowBound=0) for d in DISHES}

    prob += pulp.lpSum(contribution_margin(d) * x[d] for d in DISHES), "Z"

    prob += (pulp.lpSum((DISHES[d]["labor_min"] / 60.0) * x[d] for d in DISHES)
             <= labor_hours, "Labor_Hours")
    for d in DISHES:
        prob += (x[d] <= DISHES[d]["demand_max"], f"DemandMax_{d}")

    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    portions = {d: (x[d].value() or 0.0) for d in DISHES}
    reduced_cost = {d: (x[d].dj if x[d].dj is not None else 0.0) for d in DISHES}
    labor_shadow = prob.constraints["Labor_Hours"].pi
    demand_shadow = {d: prob.constraints[f"DemandMax_{d}"].pi for d in DISHES}
    labor_used = sum((DISHES[d]["labor_min"] / 60.0) * portions[d] for d in DISHES)

    return {
        "status": pulp.LpStatus[prob.status],
        "objective": pulp.value(prob.objective),
        "portions": portions,
        "reduced_cost": reduced_cost,
        "labor_shadow": labor_shadow,
        "demand_shadow": demand_shadow,
        "labor_used": labor_used,
        "labor_hours": labor_hours,
    }


# ---------------------------------------------------------------------------
# 2. ΡΗΤΗ ΔΙΑΤΥΠΩΣΗ ΚΑΙ ΕΠΙΛΥΣΗ ΤΟΥ ΔΥΪΚΟΥ ΠΡΟΒΛΗΜΑΤΟΣ
# ---------------------------------------------------------------------------
def solve_dual(labor_hours=None):
    """
    Διατυπώνει και επιλύει ΑΝΕΞΑΡΤΗΤΑ το δυϊκό LP, ώστε να επιβεβαιωθεί
    αριθμητικά η ισχυρή δυϊκότητα (W* = Z*).

    Returns:
        dict με κλειδιά: objective (W*), u (labor dual), v (demand duals)
    """
    if labor_hours is None:
        labor_hours = PARAMS["labor_hours_available"]

    dual = pulp.LpProblem("Menu_LP_dual", pulp.LpMinimize)
    u = pulp.LpVariable("u_labor", lowBound=0)               # σκιώδης τιμή εργασίας
    v = {d: pulp.LpVariable(f"v_{d}", lowBound=0) for d in DISHES}  # σκ. τιμές ζήτησης

    # Αντικειμενική: min H·u + Σ D_d^max · v_d
    dual += (labor_hours * u
             + pulp.lpSum(DISHES[d]["demand_max"] * v[d] for d in DISHES)), "W"

    # Ένας περιορισμός ανά πρωτεύουσα μεταβλητή x_d
    for d in DISHES:
        dual += ((DISHES[d]["labor_min"] / 60.0) * u + v[d]
                 >= contribution_margin(d), f"dual_{d}")

    dual.solve(pulp.PULP_CBC_CMD(msg=0))

    return {
        "status": pulp.LpStatus[dual.status],
        "objective": pulp.value(dual.objective),
        "u": u.value(),
        "v": {d: (v[d].value() or 0.0) for d in DISHES},
    }


# ---------------------------------------------------------------------------
# 3. ΕΛΕΓΧΟΣ ΣΥΜΠΛΗΡΩΜΑΤΙΚΗΣ ΧΑΛΑΡΟΤΗΤΑΣ
# ---------------------------------------------------------------------------
def complementary_slackness(primal, tol=1e-4):
    """
    Επαληθεύει τις συνθήκες συμπληρωματικής χαλαρότητας:

      (α) u · (H - Σ (t_d/60) x_d) = 0
      (β) v_d · (D_d^max - x_d) = 0            ∀d
      (γ) x_d · r_d = 0                        ∀d   (r_d = μειωμένο κόστος)

    Returns:
        dict με τα υπολείμματα (slacks) και boolean συνολικής ικανοποίησης.
    """
    labor_slack = primal["labor_hours"] - primal["labor_used"]
    labor_ok = abs(primal["labor_shadow"] * labor_slack) < tol

    demand_checks = {}
    for d in DISHES:
        slack = DISHES[d]["demand_max"] - primal["portions"][d]
        demand_checks[d] = {
            "slack": slack,
            "shadow": primal["demand_shadow"][d],
            "product": primal["demand_shadow"][d] * slack,
            "ok": abs(primal["demand_shadow"][d] * slack) < tol,
        }

    var_checks = {}
    for d in DISHES:
        prod = primal["portions"][d] * primal["reduced_cost"][d]
        var_checks[d] = {
            "product": prod,
            "ok": abs(prod) < tol,
        }

    all_ok = (labor_ok
              and all(c["ok"] for c in demand_checks.values())
              and all(c["ok"] for c in var_checks.values()))

    return {
        "labor": {"slack": labor_slack, "shadow": primal["labor_shadow"],
                  "product": primal["labor_shadow"] * labor_slack, "ok": labor_ok},
        "demand": demand_checks,
        "variables": var_checks,
        "all_satisfied": all_ok,
    }


# ---------------------------------------------------------------------------
# 4. ΣΥΓΚΕΝΤΡΩΤΙΚΗ ΑΝΑΛΥΣΗ + ΕΞΑΓΩΓΗ JSON
# ---------------------------------------------------------------------------
def full_duality_report(labor_hours=None):
    """Τρέχει όλη τη δυϊκή ανάλυση και επιστρέφει δομημένο λεξικό."""
    primal = solve_primal_with_duals(labor_hours)
    dual = solve_dual(labor_hours)
    cs = complementary_slackness(primal)

    # Ανακατασκευή μειωμένου κόστους από τον τύπο r_d = m_d - [(t_d/60)u + v_d]
    rows = []
    for d in DISHES:
        m = contribution_margin(d)
        opp = (DISHES[d]["labor_min"] / 60.0) * primal["labor_shadow"] \
            + primal["demand_shadow"][d]
        rows.append({
            "code": d,
            "name": DISHES[d]["name"],
            "margin": round(m, 3),
            "labor_min": DISHES[d]["labor_min"],
            "portions": round(primal["portions"][d], 2),
            "demand_max": DISHES[d]["demand_max"],
            "reduced_cost_solver": round(primal["reduced_cost"][d], 3),
            "reduced_cost_formula": round(m - opp, 3),
            "demand_shadow": round(primal["demand_shadow"][d], 3),
            "produced": primal["portions"][d] > 1e-6,
        })

    return {
        "primal_objective": round(primal["objective"], 2),
        "dual_objective": round(dual["objective"], 2),
        "duality_gap": round(abs(primal["objective"] - dual["objective"]), 6),
        "strong_duality_holds": abs(primal["objective"] - dual["objective"]) < 1e-3,
        "labor_shadow_price": round(primal["labor_shadow"], 4),
        "labor_wage": PARAMS["labor_cost_per_hour"],
        "dual_u": round(dual["u"], 4),
        "complementary_slackness_ok": cs["all_satisfied"],
        "labor_binding": abs(cs["labor"]["slack"]) < 1e-4,
        "dishes": rows,
    }


def _print(rep):
    print("=" * 92)
    print("  ΔΥΪΚΗ ΑΝΑΛΥΣΗ ΤΟΥ ΓΡΑΜΜΙΚΟΥ ΠΡΟΓΡΑΜΜΑΤΟΣ (LP) — Μοντέλο Α")
    print("=" * 92)
    print(f"  Πρωτεύον βέλτιστο  Z* = {rep['primal_objective']:>10.2f} €/ημέρα")
    print(f"  Δυϊκό βέλτιστο     W* = {rep['dual_objective']:>10.2f} €/ημέρα")
    print(f"  Δυϊκό κενό |Z*-W*|    = {rep['duality_gap']:>10.6f}  "
          f"→ Ισχυρή δυϊκότητα: {'ΝΑΙ' if rep['strong_duality_holds'] else 'ΟΧΙ'}")
    print("-" * 92)
    print(f"  Σκιώδης τιμή εργασίας  u* = {rep['labor_shadow_price']:.2f} €/ώρα "
          f"(ωρομίσθιο w = {rep['labor_wage']:.2f} €/ώρα)")
    print(f"  → Κάθε επιπλέον εργατοώρα αξίζει {rep['labor_shadow_price']:.2f} € καθαρού "
          f"περιθωρίου· υπερβαίνει το ωρομίσθιο κατά "
          f"{rep['labor_shadow_price'] - rep['labor_wage']:.2f} €/ώρα.")
    print(f"  Συμπληρωματική χαλαρότητα: "
          f"{'ικανοποιείται πλήρως' if rep['complementary_slackness_ok'] else 'ΠΡΟΒΛΗΜΑ'}")
    print("=" * 92)
    print(f"  {'Πιάτο':<26}{'Περιθ.':>8}{'Εργ.λ':>7}{'Μερίδες':>9}"
          f"{'Μειωμ.κόστος':>14}{'Κατάσταση':>14}")
    print("-" * 92)
    # ταξινόμηση: πρώτα τα παραγόμενα, μετά κατά φθίνον (λιγότερο αρνητικό) reduced cost
    for r in sorted(rep["dishes"], key=lambda z: (-z["produced"], z["reduced_cost_solver"]),
                    reverse=False):
        if r["produced"]:
            state = "παράγεται"
        else:
            state = "αποκλείεται"
        print(f"  {r['name']:<26}{r['margin']:>8.2f}{r['labor_min']:>7}"
              f"{r['portions']:>9.1f}{r['reduced_cost_solver']:>14.3f}{state:>14}")
    print("=" * 92)
    print("  Ερμηνεία: για τα αποκλειόμενα πιάτα το (αρνητικό) μειωμένο κόστος είναι")
    print("  το κόστος ευκαιρίας — πόσο θα έχανε το εστιατόριο ανά μερίδα αν τα επέβαλλε.")
    print("=" * 92)


if __name__ == "__main__":
    import json
    rep = full_duality_report()
    _print(rep)
    with open("duality.json", "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    print("\n✓ duality.json saved successfully")
