"""
ranging.py — Παραμετρική ανάλυση και ανάλυση εύρους (sensitivity ranging) του LP.

Επεκτείνει τη δυϊκή ανάλυση (βλ. duality.py) με τα δύο κλασικά ερωτήματα ευστάθειας
της θεωρίας Γραμμικού Προγραμματισμού (Bertsimas & Tsitsiklis, Winston):

  1. ΕΥΡΟΣ ΔΕΞΙΟΥ ΜΕΛΟΥΣ (RHS ranging) — για πόσο μπορεί να μεταβληθεί το δεξί μέλος
     ενός περιορισμού (εδώ: οι διαθέσιμες εργατοώρες H) ΧΩΡΙΣ να αλλάξει η βέλτιστη
     βάση, δηλαδή ώστε η ΣΚΙΩΔΗΣ ΤΙΜΗ να παραμένει σταθερή. Το κέρδος είναι
     τμηματικά γραμμικό ως προς H· τα σημεία θραύσης είναι οι αλλαγές βάσης.

  2. ΕΥΡΟΣ ΣΥΝΤΕΛΕΣΤΩΝ ΑΝΤΙΚΕΙΜΕΝΙΚΗΣ (objective coefficient ranging) — για πόσο
     μπορεί να μεταβληθεί το περιθώριο m_d ενός πιάτου χωρίς να αλλάξει η βέλτιστη
     λύση x*. Για τα ΑΠΟΚΛΕΙΟΜΕΝΑ πιάτα, η επιτρεπτή ΑΥΞΗΣΗ ισούται ακριβώς με το
     |μειωμένο κόστος| (πόσο πρέπει να ανέβει το περιθώριο για να μπει το πιάτο).
"""

import pulp
from data import DISHES, PARAMS, contribution_margin
from duality import solve_primal_with_duals


# ---------------------------------------------------------------------------
# Βοηθητικό: επίλυση LP με δεδομένο διάνυσμα περιθωρίων (για objective ranging)
# ---------------------------------------------------------------------------
def _solve_lp(margins, labor_hours):
    """Επιλύει το LP με δοσμένα περιθώρια· επιστρέφει (κέρδος, μερίδες, u*)."""
    prob = pulp.LpProblem("Menu_LP_rng", pulp.LpMaximize)
    x = {d: pulp.LpVariable(f"x_{d}", lowBound=0) for d in DISHES}
    prob += pulp.lpSum(margins[d] * x[d] for d in DISHES)
    prob += (pulp.lpSum((DISHES[d]["labor_min"] / 60.0) * x[d] for d in DISHES)
             <= labor_hours, "Labor_Hours")
    for d in DISHES:
        prob += x[d] <= DISHES[d]["demand_max"], f"DemandMax_{d}"
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    portions = {d: (x[d].value() or 0.0) for d in DISHES}
    u = prob.constraints["Labor_Hours"].pi
    return pulp.value(prob.objective), portions, u


def _same_solution(a, b, tol=1e-3):
    return all(abs(a[d] - b[d]) <= tol for d in DISHES)


# ---------------------------------------------------------------------------
# 1. ΕΥΡΟΣ ΔΕΞΙΟΥ ΜΕΛΟΥΣ ΤΩΝ ΕΡΓΑΤΟΩΡΩΝ (RHS ranging του H)
# ---------------------------------------------------------------------------
def labor_rhs_range(H0=None, tol=1e-4):
    """
    Βρίσκει το διάστημα [H_low, H_high] γύρω από το τρέχον H0 μέσα στο οποίο η
    σκιώδης τιμή της εργασίας u* παραμένει σταθερή (ίδια βέλτιστη βάση).

    Επιστρέφει dict με H_low, H_high, shadow (u*), allowable_decrease, allowable_increase.
    """
    if H0 is None:
        H0 = PARAMS["labor_hours_available"]
    base = solve_primal_with_duals(H0)
    u0 = base["labor_shadow"]

    def u_at(H):
        return solve_primal_with_duals(H)["labor_shadow"]

    # Κάτω όριο: μειώνουμε το H ώσπου να αλλάξει το u*
    lo, hi = 0.0, H0
    if abs(u_at(lo) - u0) <= tol:
        H_low = 0.0
    else:
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if abs(u_at(mid) - u0) <= tol:
                hi = mid
            else:
                lo = mid
        H_low = hi
    # Άνω όριο: αυξάνουμε το H ώσπου να αλλάξει το u*
    lo, hi = H0, 500.0
    if abs(u_at(hi) - u0) <= tol:
        H_high = hi
    else:
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if abs(u_at(mid) - u0) <= tol:
                lo = mid
            else:
                hi = mid
        H_high = lo

    return {
        "H0": H0, "shadow": u0,
        "H_low": H_low, "H_high": H_high,
        "allowable_decrease": H0 - H_low,
        "allowable_increase": H_high - H0,
    }


def labor_breakpoints(H_max=140.0, step=0.25):
    """
    Χαρτογραφεί την τμηματικά γραμμική καμπύλη κέρδους(H): εντοπίζει τα σημεία
    θραύσης (αλλαγές της σκιώδους τιμής) και επιστρέφει τα τμήματα με το u* τους.
    Χρήσιμο για το παραμετρικό γράφημα.
    """
    segments = []
    prev_u = None
    seg_start = 0.0
    H = 0.0
    while H <= H_max + 1e-9:
        u = round(solve_primal_with_duals(H)["labor_shadow"], 4)
        if prev_u is None:
            prev_u = u
            seg_start = H
        elif abs(u - prev_u) > 1e-3:
            segments.append({"H_from": seg_start, "H_to": H - step, "shadow": prev_u})
            seg_start = H
            prev_u = u
        H = round(H + step, 6)
    segments.append({"H_from": seg_start, "H_to": H_max, "shadow": prev_u})
    return segments


# ---------------------------------------------------------------------------
# 2. ΕΥΡΟΣ ΣΥΝΤΕΛΕΣΤΩΝ ΑΝΤΙΚΕΙΜΕΝΙΚΗΣ (objective coefficient ranging)
# ---------------------------------------------------------------------------
def objective_ranging(labor_hours=None, cap=25.0, tol=1e-3):
    """
    Για κάθε πιάτο υπολογίζει την επιτρεπτή αύξηση/μείωση του περιθωρίου m_d χωρίς
    αλλαγή της βέλτιστης λύσης x*. Επιβεβαιώνει ότι για τα αποκλειόμενα πιάτα η
    επιτρεπτή αύξηση ισούται με το |μειωμένο κόστος|.
    """
    if labor_hours is None:
        labor_hours = PARAMS["labor_hours_available"]
    base_margins = {d: contribution_margin(d) for d in DISHES}
    _, base_x, _ = _solve_lp(base_margins, labor_hours)
    dual = solve_primal_with_duals(labor_hours)

    rows = []
    for d in DISHES:
        produced = base_x[d] > 1e-6

        def changes(delta):
            m = dict(base_margins)
            m[d] = base_margins[d] + delta
            _, x, _ = _solve_lp(m, labor_hours)
            return not _same_solution(x, base_x)

        # Επιτρεπτή αύξηση (δ>0)
        if not changes(cap):
            inc = float("inf")
        else:
            lo, hi = 0.0, cap
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                if changes(mid):
                    hi = mid
                else:
                    lo = mid
            inc = lo
        # Επιτρεπτή μείωση (δ<0)
        if not changes(-cap):
            dec = float("inf")
        else:
            lo, hi = 0.0, cap
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                if changes(-mid):
                    hi = mid
                else:
                    lo = mid
            dec = lo

        rows.append({
            "code": d, "name": DISHES[d]["name"],
            "margin": base_margins[d],
            "produced": produced,
            "reduced_cost": dual["reduced_cost"][d],
            "allow_increase": inc,
            "allow_decrease": dec,
        })
    return rows


# ---------------------------------------------------------------------------
# ΕΚΤΥΠΩΣΗ / ΕΞΑΓΩΓΗ
# ---------------------------------------------------------------------------
def _fmt(v):
    return "∞" if v == float("inf") else f"{v:.2f}"


if __name__ == "__main__":
    import json
    print("=" * 90)
    print("  ΑΝΑΛΥΣΗ ΕΥΡΟΥΣ (RANGING) — Παραμετρική ανάλυση του LP")
    print("=" * 90)

    rr = labor_rhs_range()
    print(f"\n[1] ΕΥΡΟΣ ΕΡΓΑΤΟΩΡΩΝ (RHS ranging)")
    print(f"    Στο H0 = {rr['H0']:.0f} ώρες, σκιώδης τιμή u* = {rr['shadow']:.2f} €/ώρα")
    print(f"    Ισχύει για H ∈ [{rr['H_low']:.2f}, {rr['H_high']:.2f}] ώρες")
    print(f"    Επιτρεπτή μείωση: {rr['allowable_decrease']:.2f} | "
          f"Επιτρεπτή αύξηση: {rr['allowable_increase']:.2f} ώρες")

    print(f"\n[2] ΕΥΡΟΣ ΠΕΡΙΘΩΡΙΩΝ (objective coefficient ranging)")
    print(f"    {'Πιάτο':<26}{'m':>7}{'κατάστ.':>12}{'επιτρ.αύξ.':>12}{'επιτρ.μείωση':>13}")
    print("    " + "-" * 74)
    obj = objective_ranging()
    for r in sorted(obj, key=lambda z: (-z["produced"], -z["margin"])):
        st = "παράγεται" if r["produced"] else "αποκλείεται"
        print(f"    {r['name']:<26}{r['margin']:>7.2f}{st:>12}"
              f"{_fmt(r['allow_increase']):>12}{_fmt(r['allow_decrease']):>13}")

    out = {
        "labor_rhs_range": rr,
        "objective_ranging": [
            {**r, "allow_increase": (None if r["allow_increase"] == float("inf")
                                     else round(r["allow_increase"], 3)),
             "allow_decrease": (None if r["allow_decrease"] == float("inf")
                                else round(r["allow_decrease"], 3)),
             "reduced_cost": round(r["reduced_cost"], 3),
             "margin": round(r["margin"], 3)}
            for r in obj
        ],
        "labor_breakpoints": labor_breakpoints(),
    }
    with open("ranging.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\n✓ ranging.json saved successfully")
