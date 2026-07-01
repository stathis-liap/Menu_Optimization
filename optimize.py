"""
optimize.py — Μαθηματικά μοντέλα βελτιστοποίησης μενού εστιατορίου.

Υλοποιεί δύο αναπτυγμένα μοντέλα Γραμμικού Προγραμματισμού με τη βιβλιοθήκη PuLP:

═════════════════════════════════════════════════════════════════════════════

ΜΟΝΤΕΛΟ Α — ΓΡΑΜΜΙΚΟΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ (LP)
─────────────────────────────────────────

Χρησιμοποιεί συνεχείς μεταβλητές για την αναπαράσταση της παραγωγής.

ΜΕΤΑΒΛΗΤΕΣ ΑΠΟΦΑΣΗΣ:
  x_d ∈ ℝ≥0  :  Αριθμός μερίδων πιάτου d που παράγονται/ημέρα

ΑΝΤΙΚΕΙΜΕΝΙΚΗ ΣΥΝΑΡΤΗΣΗ:
  max Z_LP = Σ_d (p_d - c_d) · x_d

  όπου:
    p_d = τιμή πώλησης μερίδας πιάτου d (€)
    c_d = μεταβλητό κόστος ανά μερίδα: c_d = μ_d + λ_d + σ_d
      - μ_d = κόστος πρώτων υλών
      - λ_d = κόστος εργασίας
      - σ_d = κόστος σπατάλης (επιπλέον αγορές που δεν χρησιμοποιούνται)

ΠΕΡΙΟΡΙΣΜΟΙ:
  1. Εργατοώρες:  Σ_d (t_d/60) · x_d ≤ H
     Οι συνολικές ώρες εργασίας δεν υπερβαίνουν τις διαθέσιμες ώρες.

  2. Ζήτηση:     0 ≤ x_d ≤ D_d^max  ∀d
     Κάθε πιάτο παράγεται από 0 έως τη μέγιστη ζήτηση.

═════════════════════════════════════════════════════════════════════════════

ΜΟΝΤΕΛΟ Β — ΜΙΚΤΟΣ ΑΚΕΡΑΙΟΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ (MIP)
──────────────────────────────────────────────

Επεκτείνει το LP προσθέτοντας δυαδικές (binary) μεταβλητές για να δημιουργήσει
πρακτικότερο μενού με σταθερό αριθμό πιάτων και πάγια κόστη προετοιμασίας.

ΜΕΤΑΒΛΗΤΕΣ ΑΠΟΦΑΣΗΣ:
  x_d ∈ ℝ≥0  :  Μερίδες πιάτου d
  y_d ∈ {0,1}:  Δείκτης: 1 αν το πιάτο d εντάσσεται στο μενού, 0 αλλιώς

ΑΝΤΙΚΕΙΜΕΝΙΚΗ ΣΥΝΑΡΤΗΣΗ:
  max Z_MIP = Σ_d (p_d - c_d) · x_d - Σ_d f_d · y_d

  όπου f_d = πάγιο κόστος προετοιμασίας πιάτου d (εξοπλισμός, συστατικά setup)

ΠΕΡΙΟΡΙΣΜΟΙ:
  1. Εργατοώρες:  Σ_d (t_d/60) · x_d ≤ H
     (ίδια με LP)

  2. Σύνδεση παραγωγής-επιλογής:  x_d ≤ D_d^max · y_d  ∀d
     Μπορούμε να παράγουμε πιάτο d ΜΟΝΟ αν το έχουμε επιλέξει.

  3. Ελάχιστη ζήτηση αν επιλεγεί:  x_d ≥ D_d^min · y_d  ∀d
     Αν επιλέξουμε το πιάτο d, πρέπει να παράγουμε τουλάχιστον την ελάχιστη ζήτηση.

  4. Περιορισμός πλήθους πιάτων:  N_min ≤ Σ_d y_d ≤ N_max
     Το μενού περιέχει τουλάχιστον N_min και το πολύ N_max πιάτα.

  5. Φυσικοί περιορισμοί:  x_d ≥ 0, y_d ∈ {0,1}

═════════════════════════════════════════════════════════════════════════════

ΣΗΜΕΙΩΣΕΙΣ ΜΟΝΤΕΛΟΠΟΙΗΣΗΣ:

• Κόστος σπατάλης: σ_d = μ_d · α · β
  όπου α = ποσοστό σπατάλης (π.χ., 6%), β = συντελεστής ποινής (π.χ., 1.0)
  
• Κόστος εργασίας: λ_d = (t_d / 60) · w
  όπου t_d = εργατολεπτά ανά μερίδα, w = ωρομίσθιο
  
• Πάγια κόστη: Τα fixed_setup αντιπροσωπεύουν κόστη που δεν εξαρτώνται από την ποσότητα
  (π.χ., εξοπλισμός, προετοιμασία χώρου, απόστρωση).

═════════════════════════════════════════════════════════════════════════════
"""

import pulp
from data import (DISHES, PARAMS, ingredient_cost_per_portion, 
                  labor_cost_per_portion, variable_cost_per_portion, 
                  contribution_margin)


# ---------------------------------------------------------------------------
# ΜΟΝΤΕΛΟ Α — ΓΡΑΜΜΙΚΟΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ (LINEAR PROGRAMMING)
# ---------------------------------------------------------------------------
def solve_lp(waste_fraction=None, waste_penalty=None, labor_hours=None, verbose=True):
    """
    Επιλύει το μοντέλο Γραμμικού Προγραμματισμού (LP).
    
    Χρησιμοποιούνται συνεχείς μεταβλητές για τις ποσότητες παραγωγής.
    Δεν υπάρχει περιορισμός στο πλήθος των πιάτων που προσφέρονται.
    
    Args:
        waste_fraction (float): Ποσοστό σπατάλης (default από PARAMS)
        waste_penalty (float): Συντελεστής ποινής σπατάλης (default από PARAMS)
        labor_hours (float): Διαθέσιμες εργατοώρες (default από PARAMS)
        verbose (bool): Τύπωση αποτελεσμάτων
    
    Returns:
        dict: Λεξικό με κλειδιά status, profit, portions, on_menu, labor_used
    """
    if labor_hours is None:
        labor_hours = PARAMS["labor_hours_available"]

    prob = pulp.LpProblem("Menu_LP", pulp.LpMaximize)
    x = {d: pulp.LpVariable(f"x_{d}", lowBound=0) for d in DISHES}

    # Αντικειμενική: Μεγιστοποίηση κέρδους συνεισφοράς
    prob += pulp.lpSum(
        contribution_margin(d, waste_fraction, waste_penalty) * x[d]
        for d in DISHES
    ), "Total_Contribution_Margin"

    # Περιορισμός 1: Εργατοώρες
    prob += (
        pulp.lpSum((DISHES[d]["labor_min"] / 60.0) * x[d] for d in DISHES) <= labor_hours,
        "Labor_Hours"
    )

    # Περιορισμός 2: Όρια ζήτησης
    for d in DISHES:
        prob += x[d] <= DISHES[d]["demand_max"], f"DemandMax_{d}"

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    result = _collect(prob, x, None)
    if verbose:
        _print_result("ΜΟΝΤΕΛΟ Α — Γραμμικός Προγραμματισμός (LP)", result)
    return result


# ---------------------------------------------------------------------------
# ΜΟΝΤΕΛΟ Β — ΜΙΚΤΟΣ ΑΚΕΡΑΙΟΣ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΣ (MIXED INTEGER PROGRAMMING)
# ---------------------------------------------------------------------------
def solve_mip(waste_fraction=None, waste_penalty=None, labor_hours=None,
              max_dishes=None, min_dishes=None, verbose=True):
    """
    Επιλύει το μοντέλο Μικτού Ακέραιου Προγραμματισμού (MIP).
    
    Προσθέτει δυαδικές μεταβλητές για την επιλογή πιάτων και πάγια κόστη,
    δημιουργώντας ένα πρακτικότερο μενού με σταθερό αριθμό επιλογών.
    
    Args:
        waste_fraction (float): Ποσοστό σπατάλης (default από PARAMS)
        waste_penalty (float): Συντελεστής ποινής (default από PARAMS)
        labor_hours (float): Διαθέσιμες εργατοώρες (default από PARAMS)
        max_dishes (int): Μέγιστος αριθμός πιάτων στο μενού (default από PARAMS)
        min_dishes (int): Ελάχιστος αριθμός πιάτων στο μενού (default από PARAMS)
        verbose (bool): Τύπωση αποτελεσμάτων
    
    Returns:
        dict: Λεξικό με κλειδιά status, profit, portions, on_menu, labor_used
    """
    if labor_hours is None:
        labor_hours = PARAMS["labor_hours_available"]
    if max_dishes is None:
        max_dishes = PARAMS["max_dishes_on_menu"]
    if min_dishes is None:
        min_dishes = PARAMS["min_dishes_on_menu"]

    prob = pulp.LpProblem("Menu_MIP", pulp.LpMaximize)
    
    # Μεταβλητές αποφάσεων
    x = {d: pulp.LpVariable(f"x_{d}", lowBound=0) for d in DISHES}  # ποσότητες
    y = {d: pulp.LpVariable(f"y_{d}", cat="Binary") for d in DISHES}  # επιλογή πιάτων

    # Αντικειμενική: Κέρδος συνεισφοράς μείον πάγια κόστη
    prob += (
        pulp.lpSum(
            contribution_margin(d, waste_fraction, waste_penalty) * x[d]
            for d in DISHES
        ) - pulp.lpSum(DISHES[d]["fixed_setup"] * y[d] for d in DISHES),
        "Total_Net_Profit"
    )

    # Περιορισμός 1: Εργατοώρες
    prob += (
        pulp.lpSum((DISHES[d]["labor_min"] / 60.0) * x[d] for d in DISHES) <= labor_hours,
        "Labor_Hours"
    )

    # Περιορισμοί 2-4: Σύνδεση παραγωγής-επιλογής και ζήτηση
    for d in DISHES:
        # Περιορισμός 2α: Μέγιστη ζήτηση (και σύνδεση με y_d)
        prob += x[d] <= DISHES[d]["demand_max"] * y[d], f"MaxDemand_{d}"
        
        # Περιορισμός 2β: Ελάχιστη ζήτηση αν το πιάτο επιλεγεί
        prob += x[d] >= DISHES[d]["demand_min"] * y[d], f"MinDemand_{d}"

    # Περιορισμός 5: Πλήθος πιάτων στο μενού
    prob += (
        pulp.lpSum(y[d] for d in DISHES) <= max_dishes,
        "MaxMenuSize"
    )
    prob += (
        pulp.lpSum(y[d] for d in DISHES) >= min_dishes,
        "MinMenuSize"
    )

    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    result = _collect(prob, x, y)
    if verbose:
        _print_result("ΜΟΝΤΕΛΟ Β — Μικτός Ακέραιος Προγραμματισμός (MIP)", result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ
# ─────────────────────────────────────────────────────────────────────────────

def _collect(prob, x, y):
    """
    Συλλέγει και δομοποιεί τα αποτελέσματα της βελτιστοποίησης.
    
    Args:
        prob: Το προσδιορισμένο πρόβλημα PuLP
        x (dict): Λεξικό μεταβλητών ποσοτήτων
        y (dict): Λεξικό δυαδικών μεταβλητών (ή None για LP)
    
    Returns:
        dict: Δομημένα αποτελέσματα
    """
    portions = {d: (x[d].value() or 0.0) for d in DISHES}
    on_menu = {d: (round(y[d].value()) if y else (1 if portions[d] > 1e-6 else 0)) for d in DISHES}
    labor_used = sum((DISHES[d]["labor_min"] / 60.0) * portions[d] for d in DISHES)
    return {
        "status": pulp.LpStatus[prob.status],
        "profit": pulp.value(prob.objective),
        "portions": portions,
        "on_menu": on_menu,
        "labor_used": labor_used,
    }


def _print_result(title, r):
    """Τυπώνει τα αποτελέσματα βελτιστοποίησης σε μορφή πίνακα."""
    print("=" * 80)
    print(f"  {title}")
    print("=" * 80)
    print(f"  Κατάσταση: {r['status']:12} | Συνολικό κέρδος: {r['profit']:>10.2f} €/ημέρα")
    print(f"  Εργατοώρες: {r['labor_used']:>6.1f} / {PARAMS['labor_hours_available']:>6.0f} ώρες | "
          f"Χρησιμοποίηση: {100*r['labor_used']/PARAMS['labor_hours_available']:>5.1f}%")
    print(f"  Πιάτα στο μενού: {sum(r['on_menu'].values())}")
    print("-" * 80)
    print(f"  {'Πιάτο':<35} {'Μενού':>8} {'Μερίδες':>10} {'Κέρδος':>12}")
    print("-" * 80)
    for d in DISHES:
        flag = "✓" if r["on_menu"][d] else "—"
        margin = contribution_margin(d) * r["portions"][d]
        print(f"  {DISHES[d]['name']:<35} {flag:>8} {r['portions'][d]:>10.1f} {margin:>12.2f}€")
    print("=" * 80)
    print()


# ─────────────────────────────────────────────────────────────────────────────
# ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ (SENSITIVITY ANALYSIS)
# ─────────────────────────────────────────────────────────────────────────────
"""
Ανάλυση ευαισθησίας: Εξέταση πώς το βέλτιστο λύση αλλάζει όταν παραμέτρων
του προβλήματος μεταβάλλονται.
"""

def sensitivity_waste(fractions):
    """
    Εξετάζει πώς μεταβάλλεται το βέλτιστο κέρδος με το ποσοστό σπατάλης.
    
    Χρήσιμο για την κατανόηση της επίδρασης της σπατάλης τροφίμων και τη
    δικαιολόγηση επενδύσεων σε αποθήκευση και ποιοτικό έλεγχο.
    
    Args:
        fractions (list): Λίστα ποσοστών σπατάλης (π.χ., [0.0, 0.05, 0.10])
    
    Returns:
        list: Λίστα λεξικών με κλειδιά waste_fraction, profit, n_dishes
    """
    rows = []
    for wf in fractions:
        r = solve_mip(waste_fraction=wf, verbose=False)
        rows.append({
            "waste_fraction": wf,
            "profit": r["profit"],
            "n_dishes": sum(r["on_menu"].values()),
            "labor_used": r["labor_used"]
        })
    return rows


def sensitivity_labor_hours(hours_list):
    """
    Εξετάζει πώς μεταβάλλεται το κέρδος με τις διαθέσιμες εργατοώρες.
    
    Χρήσιμο για τον προγραμματισμό της εργασίας και την αξιολόγηση του
    κόστους προσθήκης επιπλέον ωρών εργασίας (overtime).
    
    Args:
        hours_list (list): Λίστα διαθέσιμων ωρών (π.χ., [40, 50, 60, 70])
    
    Returns:
        list: Λίστα λεξικών με κλειδιά labor_hours, profit, n_dishes
    """
    rows = []
    for hours in hours_list:
        r = solve_mip(labor_hours=hours, verbose=False)
        rows.append({
            "labor_hours": hours,
            "profit": r["profit"],
            "n_dishes": sum(r["on_menu"].values()),
            "labor_used": r["labor_used"]
        })
    return rows


def sensitivity_material_cost(multipliers):
    """
    Εξετάζει πώς μεταβάλλεται το κέρδος αν αλλάξει ομοιόμορφα το κόστος πρώτων υλών.
    
    Χρήσιμο για σενάρια αγορών (πληθωρισμός, εποχιακές διακυμάνσεις, αλλαγές προμηθευτών).
    
    Args:
        multipliers (list): Λίστα πολλαπλασιαστών (π.χ., [0.8, 0.9, 1.0, 1.1, 1.25])
    
    Returns:
        list: Λίστα λεξικών με κλειδιά cost_multiplier, profit, n_dishes
    """
    import data
    base = {ing: data.INGREDIENTS[ing]["price"] for ing in data.INGREDIENTS}
    rows = []
    for m in multipliers:
        # Προσωρινή τροποποίηση των τιμών
        for ing in data.INGREDIENTS:
            data.INGREDIENTS[ing]["price"] = base[ing] * m
        
        r = solve_mip(verbose=False)
        rows.append({
            "cost_multiplier": m,
            "profit": r["profit"],
            "n_dishes": sum(r["on_menu"].values()),
            "labor_used": r["labor_used"]
        })
    
    # Επαναφορά των αρχικών τιμών
    for ing in data.INGREDIENTS:
        data.INGREDIENTS[ing]["price"] = base[ing]
    
    return rows


def sensitivity_menu_size(min_list, max_list):
    """
    Εξετάζει πώς μεταβάλλεται το κέρδος με το μέγεθος του μενού.
    
    Χρήσιμο για ευελιξία στη σύνθεση του μενού και κατανόηση του trade-off
    μεταξύ ποικιλίας και αποδοτικότητας.
    
    Args:
        min_list (list): Λίστα ελάχιστων πιάτων (π.χ., [3, 4, 5])
        max_list (list): Λίστα μέγιστων πιάτων (π.χ., [8, 10, 12])
    
    Returns:
        list: Λίστα λεξικών με κλειδιά min_dishes, max_dishes, profit, n_dishes_selected
    """
    rows = []
    for min_d in min_list:
        for max_d in max_list:
            if min_d <= max_d:
                r = solve_mip(min_dishes=min_d, max_dishes=max_d, verbose=False)
                rows.append({
                    "min_dishes": min_d,
                    "max_dishes": max_d,
                    "profit": r["profit"],
                    "n_dishes_selected": sum(r["on_menu"].values()),
                    "labor_used": r["labor_used"]
                })
    return rows


if __name__ == "__main__":
    print("\n" + "═" * 90)
    print("  ΒΕΛΤΙΣΤΟΠΟΙΗΣΗ ΜΕΝΟΥ ΕΣΤΙΑΤΟΡΙΟΥ — Γραμμικός & Μικτός Ακέραιος Προγραμματισμός")
    print("═" * 90 + "\n")
    
    # ─────────────────────────────────────────────────────────────────────────────
    # ΚΎΡΙΑ ΒΕΛΤΙΣΤΟΠΟΙΗΣΗ
    # ─────────────────────────────────────────────────────────────────────────────
    print("\n[1] ΚΥΡΙΑ ΒΕΛΤΙΣΤΟΠΟΙΗΣΗ\n")
    solve_lp()
    solve_mip()

    # ─────────────────────────────────────────────────────────────────────────────
    # ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ — ΣΠΑΤΆΛΗ
    # ─────────────────────────────────────────────────────────────────────────────
    print("\n[2] ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ — ΠΟΣΟΣΤΟ ΣΠΑΤΆΛΗΣ\n")
    print("─" * 90)
    print(f"{'Σπατάλη (%)':>12} {'Κέρδος (€)':>14} {'Πιάτα':>10} {'Ώρες χρήσης':>15}")
    print("─" * 90)
    for row in sensitivity_waste([0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.20]):
        print(f"  {row['waste_fraction']*100:>10.1f}% {row['profit']:>14.2f}€ {row['n_dishes']:>10} "
              f"{row['labor_used']:>15.1f} ώρες")
    print("─" * 90)
    print("Σχόλιο: Υψηλότερη σπατάλη μειώνει σημαντικά το κέρδος. Επενδύστε σε ποιοτικό έλεγχο.")

    # ─────────────────────────────────────────────────────────────────────────────
    # ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ — ΕΡΓΑΤΟΏΡΕΣ
    # ─────────────────────────────────────────────────────────────────────────────
    print("\n[3] ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ — ΔΙΑΘΕΣΙΜΕΣ ΕΡΓΑΤΟΏΡΕΣ\n")
    print("─" * 90)
    print(f"{'Εργατοώρες':>12} {'Κέρδος (€)':>14} {'Πιάτα':>10} {'Χρήσιμες ώρες':>15}")
    print("─" * 90)
    for row in sensitivity_labor_hours([40, 50, 60, 65, 70, 80]):
        print(f"  {row['labor_hours']:>10.0f} {row['profit']:>14.2f}€ {row['n_dishes']:>10} "
              f"{row['labor_used']:>15.1f} ώρες")
    print("─" * 90)
    print("Σχόλιο: Περισσότερες ώρες επιτρέπουν μεγαλύτερο κέρδος, αλλά με φθίνουσες αποδόσεις.")

    # ─────────────────────────────────────────────────────────────────────────────
    # ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ — ΚΟΣΤΟΣ ΠΡΩΤΩΝ ΥΛΩΝ
    # ─────────────────────────────────────────────────────────────────────────────
    print("\n[4] ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ — ΚΟΣΤΟΣ ΠΡΩΤΩΝ ΥΛΩΝ\n")
    print("─" * 90)
    print(f"{'Πολλαπλασιαστής':>18} {'Κέρδος (€)':>14} {'Πιάτα':>10} {'Ώρες χρήσης':>15}")
    print("─" * 90)
    for row in sensitivity_material_cost([0.75, 0.85, 0.95, 1.0, 1.05, 1.15, 1.25, 1.5]):
        mult_str = f"×{row['cost_multiplier']:.2f}"
        print(f"  {mult_str:>17} {row['profit']:>14.2f}€ {row['n_dishes']:>10} "
              f"{row['labor_used']:>15.1f} ώρες")
    print("─" * 90)
    print("Σχόλιο: Το κέρδος είναι ευαίσθητο στο κόστος υλικών. Διαπραγματευθείτε με προμηθευτές.")

    # ─────────────────────────────────────────────────────────────────────────────
    # ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ — ΜΕΓΕΘΟΣ ΜΕΝΟΥ
    # ─────────────────────────────────────────────────────────────────────────────
    print("\n[5] ΑΝΑΛΥΣΗ ΕΥΑΙΣΘΗΣΙΑΣ — ΜΕΓΕΘΟΣ ΜΕΝΟΥ (MIP)\n")
    print("─" * 90)
    print(f"{'Min-Max':>12} {'Κέρδος (€)':>14} {'Πιάτα':>10} {'Ώρες':>15}")
    print("─" * 90)
    for row in sensitivity_menu_size([4, 6, 8], [6, 8, 10, 12]):
        range_str = f"{row['min_dishes']}-{row['max_dishes']}"
        print(f"  {range_str:>11} {row['profit']:>14.2f}€ {row['n_dishes_selected']:>10} "
              f"{row['labor_used']:>15.1f} ώρες")
    print("─" * 90)
    print("Σχόλιο: Μεγαλύτερο μενού προσφέρει περισσότερες επιλογές αλλά μπορεί να μειώσει αποδοτικότητα.")
    
    print("\n" + "═" * 90)
    print("  ΟΛΟΚΛΗΡΩΣΗ ΑΝΑΛΥΣΗΣ")
    print("═" * 90 + "\n")

