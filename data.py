"""
data.py — Βάση δεδομένων πρώτων υλών και συνταγών για το πρόβλημα
βελτιστοποίησης μενού εστιατορίου.

Οι τιμές αντικατοπτρίζουν ρεαλιστικές τιμές λιανικής/χονδρικής της
ελληνικής αγοράς (Ιαν.–Μάιος 2026, πηγές: ΕΛΣΤΑΤ, ΟΚΑΑ, ΙΕΛΚΑ,
τιμοληψίες αλυσίδων σουπερμάρκετ). Μονάδα: € ανά kg (ή ανά L για υγρά,
ανά τεμάχιο για αυγά).

ΚΑΤΗΓΟΡΙΕΣ ΥΛΙΚΩΝ:
  - Κρέατα & πρωτεΐνες
  - Λαχανικά φρέσκα
  - Δημητριακά & αρχίδια
  - Γαλακτοκομικά
  - Βασικά & μυρωδικά
  - Κόνδυλοι ψιλοκοπής
"""

# ---------------------------------------------------------------------------
# 1. ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ ΠΡΩΤΩΝ ΥΛΩΝ (INGREDIENTS)
# ---------------------------------------------------------------------------
# Κάθε πρώτη ύλη: τιμή αγοράς (€/kg) και πηγή/σχόλιο.
# Τιμές ανά kg ή ανά L για υγρά, ανά τεμάχιο για αυγά.
INGREDIENTS = {
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━ ΚΡΕΑΤΑ & ΠΡΩΤΕΙΝΕΣ ━━━━━━━━━━━━━━━━━━━━━
    "kimas_mosx":      {"price": 15.50, "unit": "kg", "category": "κρέατα", 
                        "name": "Κιμάς μοσχαρίσιος",        
                        "src": "ΟΚΑΑ/ΕΛΣΤΑΤ 2026: 15-16 €/kg"},
    "kimas_hirino":    {"price": 12.00, "unit": "kg", "category": "κρέατα",
                        "name": "Κιμάς χοιρινός",
                        "src": "ΟΚΑΑ/ΕΛΣΤΑΤ 2026: 11-13 €/kg"},
    "kotopoulo":       {"price": 12.50, "unit": "kg", "category": "κρέατα",
                        "name": "Κοτόπουλο (φιλέτο/μπούτι)",
                        "src": "ΟΚΑΑ/ΕΛΣΤΑΤ 2026: 11-14 €/kg"},
    "paidaki_arni":    {"price": 12.50, "unit": "kg", "category": "κρέατα",
                        "name": "Παϊδάκια αρνίσια (κατεψυγμένα)",
                        "src": "Σ/Μ 2026: 11-14 €/kg"},

    # ━━━━━━━━━━━━━━━━━━━━━━━━━ ΘΑΛΑΣΣΙΝΑ ━━━━━━━━━━━━━━━━━━━━━━
    "garides":         {"price": 14.00, "unit": "kg", "category": "θαλασσινά",
                        "name": "Γαρίδες κατεψυγμένες (Νο 2)",
                        "src": "Σ/Μ 2026: 12-16 €/kg"},
    "htapodi":         {"price": 13.00, "unit": "kg", "category": "θαλασσινά",
                        "name": "Χταπόδι κατεψυγμένο",
                        "src": "Σ/Μ/ΟΚΑΑ 2026: 12-15 €/kg"},

    # ━━━━━━━━━━━━━━━━━━━━━━━━ ΛΑΧΑΝΙΚΑ ΦΡΕΣΚΑ ━━━━━━━━━━━━━━━━━━━━━━
    "patates":         {"price":  0.80, "unit": "kg", "category": "λαχανικά",
                        "name": "Πατάτες",                  
                        "src": "Σ/Μ 2026: 0,70-1,16 €/kg"},
    "tomata":          {"price":  1.80, "unit": "kg", "category": "λαχανικά",
                        "name": "Ντομάτα φρέσκια (κόκκινη)",
                        "src": "Σ/Μ 2026: 1,40-2,19 €/kg"},
    "tomata_cheri":    {"price":  3.50, "unit": "kg", "category": "λαχανικά",
                        "name": "Ντομάτα κεράσι (cherry)",
                        "src": "Σ/Μ 2026: 3-4 €/kg"},
    "melitzanes":      {"price":  2.20, "unit": "kg", "category": "λαχανικά",
                        "name": "Μελιτζάνες",               
                        "src": "Σ/Μ 2026: 1,80-2,50 €/kg"},
    "piperies":        {"price":  3.00, "unit": "kg", "category": "λαχανικά",
                        "name": "Πιπεριές κόκκινες/πράσινες",
                        "src": "Σ/Μ 2026: 2,50-3,50 €/kg"},
    "kremmydia":       {"price":  1.10, "unit": "kg", "category": "λαχανικά",
                        "name": "Κρεμμύδια ξερά",           
                        "src": "Σ/Μ 2026: 0,89-1,12 €/kg"},
    "kremmydia_verde": {"price":  4.50, "unit": "kg", "category": "λαχανικά",
                        "name": "Κρεμμύδια verde (φρέσκα)",
                        "src": "Σ/Μ 2026: 4-5 €/kg"},
    "spanaki":         {"price":  2.50, "unit": "kg", "category": "λαχανικά",
                        "name": "Σπανάκι φρέσκο",           
                        "src": "Σ/Μ 2026: 2,20-2,80 €/kg"},
    "skordo":          {"price":  6.00, "unit": "kg", "category": "λαχανικά",
                        "name": "Σκόρδο",                   
                        "src": "Σ/Μ 2026: 5,50-6,50 €/kg"},
    "mpamia":          {"price":  3.20, "unit": "kg", "category": "λαχανικά",
                        "name": "Μπάμια",
                        "src": "Σ/Μ 2026: 2,80-3,50 €/kg"},
    "kolokithakia":    {"price":  1.90, "unit": "kg", "category": "λαχανικά",
                        "name": "Κολοκιθάκια",
                        "src": "Σ/Μ 2026: 1,50-2,20 €/kg"},
    "agginares":       {"price":  2.80, "unit": "kg", "category": "λαχανικά",
                        "name": "Αγκινάρες",
                        "src": "Σ/Μ 2026: 2,50-3,20 €/kg"},
    "portokalia":      {"price":  1.50, "unit": "kg", "category": "λαχανικά",
                        "name": "Πορτοκάλια",
                        "src": "Σ/Μ 2026: 1,20-1,80 €/kg"},
    "lemonia":         {"price":  1.80, "unit": "kg", "category": "λαχανικά",
                        "name": "Λεμόνια",
                        "src": "Σ/Μ 2026: 1,50-2,20 €/kg"},

    # ━━━━━━━━━━━━━━━━━━━━ ΔΗΜΗΤΡΙΑΚΑ & ΑΡΧΙΔΙΑ ━━━━━━━━━━━━━━━━━━━━
    "rizi":            {"price":  1.60, "unit": "kg", "category": "δημητριακά",
                        "name": "Ρύζι (Καρολίνα)",          
                        "src": "Σ/Μ 2026: ~0,79 €/500g"},
    "rizi_arborio":    {"price":  2.80, "unit": "kg", "category": "δημητριακά",
                        "name": "Ρύζι Arborio (risotto)",
                        "src": "Σ/Μ 2026: 2,50-3,20 €/kg"},
    "makaronia":       {"price":  1.30, "unit": "kg", "category": "δημητριακά",
                        "name": "Μακαρόνια (No6)",          
                        "src": "Σ/Μ 2026: 0,75-1,50 €/kg"},
    "hilopites":       {"price":  1.50, "unit": "kg", "category": "δημητριακά",
                        "name": "Χηλοπίτες (φύλλο ζύμης)",
                        "src": "Σ/Μ 2026: 1,20-1,80 €/kg"},
    "aleuri":          {"price":  1.20, "unit": "kg", "category": "δημητριακά",
                        "name": "Αλεύρι (Τύπου 550)",        
                        "src": "Σ/Μ 2026: 0,90-1,50 €/kg"},
    "korni_psomou":    {"price":  2.50, "unit": "kg", "category": "δημητριακά",
                        "name": "Κορνάρι ψωμιού",
                        "src": "Σ/Μ 2026: 2,20-2,80 €/kg"},
    "psomi":           {"price":  1.00, "unit": "kg", "category": "δημητριακά",
                        "name": "Ψωμί (κατάλληλο για κρούμπες)",
                        "src": "Σ/Μ 2026: 0,80-1,20 €/kg"},

    # ━━━━━━━━━━━━━━━━━━━━ ΓΑΛΑΚΤΟΚΟΜΙΚΑ ━━━━━━━━━━━━━━━━━━━━━
    "feta":            {"price": 11.00, "unit": "kg", "category": "γαλακτοκομικά",
                        "name": "Φέτα ΠΟΠ",                 
                        "src": "Σ/Μ 2026: 9,8-14 €/kg"},
    "graviera":        {"price": 14.50, "unit": "kg", "category": "γαλακτοκομικά",
                        "name": "Γραβιέρα ΠΟΠ",
                        "src": "Σ/Μ 2026: 13-16 €/kg"},
    "kefalotyri":      {"price": 13.00, "unit": "kg", "category": "γαλακτοκομικά",
                        "name": "Κεφαλοτύρι ΠΟΠ (τριμμένο)",
                        "src": "Σ/Μ 2026: 12-14 €/kg"},
    "manouri":         {"price": 12.50, "unit": "kg", "category": "γαλακτοκομικά",
                        "name": "Μανούρι",
                        "src": "Σ/Μ 2026: 11-14 €/kg"},
    "gala":            {"price":  1.35, "unit": "L",  "category": "γαλακτοκομικά",
                        "name": "Γάλα φρέσκο (3,6% λιπαρά)",
                        "src": "Σ/Μ 2026: 1,30-1,47 €/L"},
    "voutyro":         {"price":  9.00, "unit": "kg", "category": "γαλακτοκομικά",
                        "name": "Βούτυρο",                  
                        "src": "Σ/Μ 2026: 8-10 €/kg"},
    "avga":            {"price":  0.30, "unit": "τεμ", "category": "γαλακτοκομικά",
                        "name": "Αυγά (τεμάχιο)",           
                        "src": "Σ/Μ 2026: ~1,76 €/6άδα"},
    "yogorti":         {"price":  1.20, "unit": "L",  "category": "γαλακτοκομικά",
                        "name": "Γιαούρτι στραγγιστό",
                        "src": "Σ/Μ 2026: 1,00-1,50 €/L"},
    "mizithra":        {"price":  8.50, "unit": "kg", "category": "γαλακτοκομικά",
                        "name": "Μυζήθρα",
                        "src": "Σ/Μ 2026: 7,50-9,50 €/kg"},

    # ━━━━━━━━━━━━━━━━━ ΒΑΣΙΚΑ & ΜΥΡΩΔΙΚΑ ━━━━━━━━━━━━━━━━━━
    "elaiolado":       {"price":  7.00, "unit": "L",  "category": "βασικά",
                        "name": "Ελαιόλαδο έξτρα παρθένο",  
                        "src": "Σ/Μ 2026: 6,4-8,5 €/L"},
    "alati":           {"price":  0.50, "unit": "kg", "category": "βασικά",
                        "name": "Αλάτι (χονδρό)",
                        "src": "Σ/Μ 2026: 0,40-0,60 €/kg"},
    "piperi":          {"price":  2.50, "unit": "kg", "category": "βασικά",
                        "name": "Πιπέρι (κατεργασμένο)",
                        "src": "Σ/Μ 2026: 2,00-3,00 €/kg"},
    "krasi_lefko":     {"price":  4.00, "unit": "L",  "category": "βασικά",
                        "name": "Λευκό κρασί μαγειρικής",   
                        "src": "Σ/Μ 2026: 3,50-4,50 €/L"},
    "krasi_kokkino":   {"price":  3.50, "unit": "L",  "category": "βασικά",
                        "name": "Κόκκινο κρασί μαγειρικής",
                        "src": "Σ/Μ 2026: 3,00-4,00 €/L"},
    "ouzaki":          {"price":  5.50, "unit": "L",  "category": "βασικά",
                        "name": "Ούζο μαγειρικής",
                        "src": "Σ/Μ 2026: 5,00-6,00 €/L"},
    "maintanos":       {"price":  6.00, "unit": "kg", "category": "μυρωδικά",
                        "name": "Μαϊντανός",                
                        "src": "Σ/Μ 2026: 5,50-6,50 €/kg"},
    "anithos":         {"price":  8.00, "unit": "kg", "category": "μυρωδικά",
                        "name": "Άνηθος",                   
                        "src": "Σ/Μ 2026: 7,50-8,50 €/kg"},
    "thymo":           {"price": 12.00, "unit": "kg", "category": "μυρωδικά",
                        "name": "Θύμο",
                        "src": "Σ/Μ 2026: 11-13 €/kg"},
    "rodokoko":        {"price": 10.00, "unit": "kg", "category": "μυρωδικά",
                        "name": "Ροδόκοκκο",
                        "src": "Σ/Μ 2026: 9-11 €/kg"},
    "kanela":          {"price": 25.00, "unit": "kg", "category": "μυρωδικά",
                        "name": "Κανέλα (σκόνη)",
                        "src": "Σ/Μ 2026: 20-30 €/kg"},
    "zyma":            {"price":  0.60, "unit": "kg", "category": "βασικά",
                        "name": "Ζύμη (ξηρή, σε σακουλάκια)",
                        "src": "Σ/Μ 2026: 0,50-0,70 €/kg"},
    
    # ━━━━━━━━━━━━━━━ ΚΟΝΔΥΛΟΙ & ΕΠΕΞΕΡΓΑΣΜΕΝΑ ━━━━━━━━━━━
    "konservofasolia": {"price":  1.10, "unit": "kg", "category": "κονδύλοι",
                        "name": "Κονσέρβα φασολιών",
                        "src": "Σ/Μ 2026: 0,90-1,30 €/400g δοχείο"},
    "konservothomata": {"price":  0.85, "unit": "kg", "category": "κονδύλοι",
                        "name": "Κονσέρβα ντομάτας",
                        "src": "Σ/Μ 2026: 0,70-1,00 €/400g δοχείο"},
    "tomatopeltes":    {"price":  1.60, "unit": "kg", "category": "κονδύλοι",
                        "name": "Ντοματοπολτός",           
                        "src": "Σ/Μ 2026: 0,80-1,20 €/500g βάζο"},
    "meli":            {"price":  9.00, "unit": "kg", "category": "κονδύλοι",
                        "name": "Μέλι (φλόγερο)",
                        "src": "Σ/Μ 2026: 8-10 €/kg"},
}

# ---------------------------------------------------------------------------
# 2. ΣΥΝΤΑΓΕΣ ΠΙΑΤΩΝ (DISHES) — Ελληνική Κουζίνα
# ---------------------------------------------------------------------------
"""
Κάθε πιάτο ορίζεται με:
  recipe       : {ingredient_code: ποσότητα_ανά_μερίδα}
  price        : τιμή πώλησης ανά μερίδα (€)
  labor_min    : εργατολεπτά προετοιμασίας ανά μερίδα
  fixed_setup  : πάγιο κόστος προετοιμασίας/ημέρα αν είναι στο μενού (€)
  demand_min   : ελάχιστη ημερήσια ζήτηση (μερίδες) αν προσφέρεται
  demand_max   : μέγιστη ημερήσια ζήτηση (μερίδες)
  category     : κατηγορία πιάτου (πρώτο/κυρίως/πλευρικό)
"""
DISHES = {
    # ━━━━━━━━━━━━━━━━━━━ ΚΥΡΙΑ ΠΙΑΤΑ ━━━━━━━━━━━━━━━━━━
    "moussakas": {
        "name": "Μουσακάς",
        "category": "κυρίως",
        "price": 12.50,
        "labor_min": 22,
        "fixed_setup": 40.0,
        "demand_min": 8,
        "demand_max": 50,
        "recipe": {
            "kimas_mosx": 0.160, "melitzanes": 0.220, "patates": 0.140,
            "kremmydia": 0.055, "tomatopeltes": 0.045, "elaiolado": 0.045,
            "gala": 0.160, "aleuri": 0.035, "voutyro": 0.030, "avga": 0.6,
            "kefalotyri": 0.045, "skordo": 0.006, "kanela": 0.002,
            "alati": 0.004, "piperi": 0.002,
        },
    },
    
    "pastitsio": {
        "name": "Παστίτσιο",
        "category": "κυρίως",
        "price": 12.00,
        "labor_min": 20,
        "fixed_setup": 38.0,
        "demand_min": 7,
        "demand_max": 45,
        "recipe": {
            "makaronia": 0.140, "kimas_mosx": 0.150, "kremmydia": 0.055,
            "tomatopeltes": 0.055, "gala": 0.160, "aleuri": 0.040,
            "voutyro": 0.030, "avga": 0.6, "kefalotyri": 0.050,
            "kanela": 0.002, "alati": 0.004, "piperi": 0.002,
        },
    },

    "gemista": {
        "name": "Γεμιστά",
        "category": "κυρίως",
        "price": 9.50,
        "labor_min": 18,
        "fixed_setup": 28.0,
        "demand_min": 5,
        "demand_max": 35,
        "recipe": {
            "tomata": 0.380, "piperies": 0.120, "rizi": 0.095, "kremmydia": 0.085,
            "elaiolado": 0.065, "maintanos": 0.012, "skordo": 0.008,
            "alati": 0.004, "piperi": 0.002,
        },
    },

    "makaronia_kima": {
        "name": "Μακαρόνια με κιμά",
        "category": "κυρίως",
        "price": 10.50,
        "labor_min": 13,
        "fixed_setup": 24.0,
        "demand_min": 7,
        "demand_max": 45,
        "recipe": {
            "makaronia": 0.135, "kimas_mosx": 0.130, "kremmydia": 0.055,
            "tomatopeltes": 0.065, "elaiolado": 0.035, "skordo": 0.006,
            "kefalotyri": 0.035, "kanela": 0.001, "alati": 0.004, "piperi": 0.002,
        },
    },

    "pastitsada_kotopoulo": {
        "name": "Παστιτσάδα κοτόπουλο",
        "category": "κυρίως",
        "price": 13.00,
        "labor_min": 25,
        "fixed_setup": 45.0,
        "demand_min": 5,
        "demand_max": 30,
        "recipe": {
            "kotopoulo": 0.220, "kremmydia": 0.080, "tomatopeltes": 0.070,
            "krasi_kokkino": 0.100, "elaiolado": 0.050, "skordo": 0.008,
            "hilopites": 0.100, "kanela": 0.003, "alati": 0.005, "piperi": 0.003,
        },
    },

    "stifado": {
        "name": "Στιφάδο (μοσχαρίσιο)",
        "category": "κυρίως",
        "price": 13.50,
        "labor_min": 28,
        "fixed_setup": 50.0,
        "demand_min": 4,
        "demand_max": 28,
        "recipe": {
            "kimas_mosx": 0.220, "kremmydia": 0.200, "tomatopeltes": 0.060,
            "krasi_kokkino": 0.080, "elaiolado": 0.050, "skordo": 0.008,
            "alati": 0.005, "piperi": 0.003, "rodokoko": 0.003,
        },
    },

    "briam": {
        "name": "Μπριάμ",
        "category": "κυρίως",
        "price": 8.50,
        "labor_min": 14,
        "fixed_setup": 22.0,
        "demand_min": 4,
        "demand_max": 32,
        "recipe": {
            "patates": 0.220, "melitzanes": 0.170, "kolokithakia": 0.120,
            "kremmydia": 0.070, "tomata": 0.160, "elaiolado": 0.080,
            "skordo": 0.008, "maintanos": 0.010, "alati": 0.004, "piperi": 0.002,
        },
    },

    "fasolada": {
        "name": "Φασολάδα",
        "category": "κυρίως",
        "price": 7.50,
        "labor_min": 10,
        "fixed_setup": 15.0,
        "demand_min": 4,
        "demand_max": 30,
        "recipe": {
            "konservofasolia": 0.280, "kremmydia": 0.070, "patates": 0.095,
            "tomatopeltes": 0.045, "elaiolado": 0.060, "skordo": 0.007,
            "maintanos": 0.008, "alati": 0.004, "piperi": 0.002,
        },
    },

    "yiouvetsi": {
        "name": "Γιουβέτσι (κιμάς)",
        "category": "κυρίως",
        "price": 11.00,
        "labor_min": 16,
        "fixed_setup": 32.0,
        "demand_min": 5,
        "demand_max": 35,
        "recipe": {
            "kimas_mosx": 0.140, "kremmydia": 0.050, "tomatopeltes": 0.070,
            "hilopites": 0.110, "elaiolado": 0.040, "kefalotyri": 0.035,
            "kanela": 0.002, "alati": 0.004, "piperi": 0.002,
        },
    },

    # ━━━━━━━━━━━━━━━━━ ΠΡΩΤΑ ΠΙΑΤΑ / ΛΑΧΑΝΙΚΑ ━━━━━━━━━━━━━
    "spanakorizo": {
        "name": "Σπανακόρυζο",
        "category": "πρώτο",
        "price": 8.50,
        "labor_min": 10,
        "fixed_setup": 18.0,
        "demand_min": 6,
        "demand_max": 40,
        "recipe": {
            "spanaki": 0.270, "rizi": 0.090, "kremmydia": 0.065,
            "elaiolado": 0.055, "anithos": 0.012, "tomatopeltes": 0.025,
            "alati": 0.004, "piperi": 0.002,
        },
    },

    "gigantes_plaki": {
        "name": "Γίγαντες πλακί",
        "category": "πρώτο",
        "price": 9.00,
        "labor_min": 12,
        "fixed_setup": 20.0,
        "demand_min": 5,
        "demand_max": 32,
        "recipe": {
            "konservofasolia": 0.300, "tomatopeltes": 0.080, "kremmydia": 0.070,
            "elaiolado": 0.060, "skordo": 0.008, "maintanos": 0.010,
            "alati": 0.004, "piperi": 0.002,
        },
    },

    "mpamies_lathi": {
        "name": "Μπάμιες λάδι",
        "category": "πρώτο",
        "price": 8.00,
        "labor_min": 11,
        "fixed_setup": 19.0,
        "demand_min": 4,
        "demand_max": 28,
        "recipe": {
            "mpamia": 0.300, "tomatopeltes": 0.070, "kremmydia": 0.060,
            "elaiolado": 0.065, "skordo": 0.007, "maintanos": 0.008,
            "alati": 0.004, "piperi": 0.002,
        },
    },

    "kolokithokeftedes": {
        "name": "Κολοκιθοκεφτέδες",
        "category": "πρώτο",
        "price": 8.50,
        "labor_min": 14,
        "fixed_setup": 22.0,
        "demand_min": 4,
        "demand_max": 30,
        "recipe": {
            "kolokithakia": 0.250, "aleuri": 0.045, "avga": 0.4,
            "kefalotyri": 0.040, "maintanos": 0.010, "elaiolado": 0.050,
            "alati": 0.004, "piperi": 0.002,
        },
    },

    "melitzanosalata": {
        "name": "Μελιτζανοσαλάτα",
        "category": "πρώτο",
        "price": 7.50,
        "labor_min": 8,
        "fixed_setup": 14.0,
        "demand_min": 5,
        "demand_max": 35,
        "recipe": {
            "melitzanes": 0.280, "kremmydia": 0.070, "tomatopeltes": 0.050,
            "elaiolado": 0.060, "skordo": 0.008, "maintanos": 0.010,
            "alati": 0.004, "piperi": 0.002,
        },
    },

    # ━━━━━━━━━━━━━━━━━━━ ΚΡΕΑΤΙΚΑ ΠΙΑΤΑ ━━━━━━━━━━━━━━━━━
    "keftedes": {
        "name": "Κεφτέδες",
        "category": "κυρίως",
        "price": 10.50,
        "labor_min": 16,
        "fixed_setup": 26.0,
        "demand_min": 6,
        "demand_max": 42,
        "recipe": {
            "kimas_mosx": 0.170, "kremmydia": 0.045, "avga": 0.6,
            "aleuri": 0.025, "elaiolado": 0.045, "maintanos": 0.010,
            "alati": 0.004, "piperi": 0.003,
        },
    },

    "keftedes_hirino": {
        "name": "Κεφτέδες χοιρινές",
        "category": "κυρίως",
        "price": 9.50,
        "labor_min": 15,
        "fixed_setup": 24.0,
        "demand_min": 5,
        "demand_max": 40,
        "recipe": {
            "kimas_hirino": 0.180, "kremmydia": 0.050, "avga": 0.6,
            "aleuri": 0.025, "elaiolado": 0.045, "maintanos": 0.010,
            "alati": 0.004, "piperi": 0.003,
        },
    },

    "keftedes_tomata": {
        "name": "Κεφτέδες σμέας",
        "category": "κυρίως",
        "price": 11.00,
        "labor_min": 18,
        "fixed_setup": 28.0,
        "demand_min": 5,
        "demand_max": 38,
        "recipe": {
            "kimas_mosx": 0.160, "kremmydia": 0.045, "avga": 0.5,
            "aleuri": 0.025, "elaiolado": 0.050, "tomatopeltes": 0.060,
            "skordo": 0.006, "maintanos": 0.010, "alati": 0.004, "piperi": 0.002,
        },
    },

    "paidakia": {
        "name": "Παϊδάκια (κατεψυγμένα)",
        "category": "κυρίως",
        "price": 15.00,
        "labor_min": 12,
        "fixed_setup": 35.0,
        "demand_min": 3,
        "demand_max": 20,
        "recipe": {
            "paidaki_arni": 0.280, "elaiolado": 0.040, "lemonia": 0.020,
            "skordo": 0.008, "rodokoko": 0.003, "thymo": 0.003,
            "alati": 0.004, "piperi": 0.003,
        },
    },

    "souvlaki": {
        "name": "Σουβλάκι κοτόπουλο",
        "category": "κυρίως",
        "price": 11.50,
        "labor_min": 14,
        "fixed_setup": 30.0,
        "demand_min": 6,
        "demand_max": 44,
        "recipe": {
            "kotopoulo": 0.200, "kremmydia": 0.050, "elaiolado": 0.045,
            "lemonia": 0.020, "skordo": 0.008, "rodokoko": 0.003, "thymo": 0.002,
            "alati": 0.004, "piperi": 0.003,
        },
    },

    # ━━━━━━━━━━━━━━━━ ΘΑΛΑΣΣΙΝΑ ΠΙΑΤΑ ━━━━━━━━━━━━━━━━
    "garides_saganaki": {
        "name": "Γαρίδες σαγανάκι",
        "category": "κυρίως",
        "price": 16.00,
        "labor_min": 12,
        "fixed_setup": 40.0,
        "demand_min": 2,
        "demand_max": 15,
        "recipe": {
            "garides": 0.200, "elaiolado": 0.060, "tomatopeltes": 0.050,
            "kremmydia": 0.040, "feta": 0.060, "skordo": 0.008,
            "anithos": 0.005, "alati": 0.004, "piperi": 0.003,
        },
    },

    "htapodi_stifado": {
        "name": "Χταπόδι στιφάδο",
        "category": "κυρίως",
        "price": 14.00,
        "labor_min": 30,
        "fixed_setup": 48.0,
        "demand_min": 2,
        "demand_max": 12,
        "recipe": {
            "htapodi": 0.250, "kremmydia": 0.150, "tomatopeltes": 0.070,
            "krasi_kokkino": 0.100, "elaiolado": 0.055, "skordo": 0.008,
            "alati": 0.005, "piperi": 0.003,
        },
    },
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. ΠΑΡΑΜΕΤΡΟΙ ΕΣΤΙΑΤΟΡΙΟΥ (GLOBAL PARAMETERS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
ΠΑΡΑΜΕΤΡΟΙ ΓΡΑΜΜΙΚΟΥ & ΜΙΚΤΟΥ ΑΚΕΡΑΙΟΥ ΠΡΟΓΡΑΜΜΑΤΙΣΜΟΥ

Για το Μοντέλο LP (Γραμμικός Προγραμματισμός):
  Μεταβλητές: x_d ∈ ℝ≥0 = μερίδες παραγωγής ανά πιάτο
  Αντικειμενική: max Σ_d (p_d - c_d) · x_d
    όπου p_d = τιμή πώλησης, c_d = μεταβλητό κόστος (υλικά + εργασία + σπατάλη)
  Περιορισμοί:
    - εργατοώρες: Σ_d (t_d/60) · x_d ≤ H
    - ζήτηση: 0 ≤ x_d ≤ D_d

Για το Μοντέλο MIP (Μικτός Ακέραιος Προγραμματισμός):
  Προσθέτει δυαδικές μεταβλητές y_d ∈ {0,1} = δείκτης ένταξης στο μενού
  Αντικειμενική: max Σ_d (p_d - c_d) · x_d - Σ_d f_d · y_d
  Περιορισμοί:
    - σύνδεση: x_d ≤ D_d · y_d (παραγωγή μόνο αν επιλεγεί το πιάτο)
    - ελάχιστη ζήτηση: x_d ≥ m_d · y_d
    - πλήθος πιάτων: N_min ≤ Σ_d y_d ≤ N_max
"""
PARAMS = {
    "labor_hours_available": 65.0,   # συνολικές διαθέσιμες εργατοώρες/ημέρα
    "labor_cost_per_hour": 7.80,     # κόστος εργασίας €/ώρα (2026)
    "waste_fraction": 0.06,          # ποσοστό υλικών που χάνεται (σπατάλη)
    "waste_penalty_factor": 1.0,     # συντελεστής ποινής σπατάλης στο κόστος
    "max_dishes_on_menu": 10,        # μέγιστος αριθμός πιάτων στο μενού (MIP)
    "min_dishes_on_menu": 6,         # ελάχιστος αριθμός πιάτων στο μενού (MIP)
}


def ingredient_cost_per_portion(dish_code):
    """
    Κόστος πρώτων υλών ανά μερίδα για ένα πιάτο (€).
    
    Args:
        dish_code (str): Κωδικός πιάτου
    
    Returns:
        float: Συνολικό κόστος πρώτων υλών ανά μερίδα
    """
    recipe = DISHES[dish_code]["recipe"]
    return sum(qty * INGREDIENTS[ing]["price"] for ing, qty in recipe.items())


def labor_cost_per_portion(dish_code):
    """
    Κόστος εργασίας ανά μερίδα (€).
    
    Args:
        dish_code (str): Κωδικός πιάτου
    
    Returns:
        float: Κόστος εργασίας ανά μερίδα
    """
    minutes = DISHES[dish_code]["labor_min"]
    return (minutes / 60.0) * PARAMS["labor_cost_per_hour"]


def waste_cost_per_portion(dish_code, waste_fraction=None, waste_penalty=None):
    """
    Κόστος σπατάλης ανά μερίδα (€).
    
    Η σπατάλη θεωρείται ως επιπλέον κόστος υλικών που αγοράζονται αλλά δεν χρησιμοποιούνται.
    
    Args:
        dish_code (str): Κωδικός πιάτου
        waste_fraction (float): Ποσοστό σπατάλης (default από PARAMS)
        waste_penalty (float): Συντελεστής ποινής (default από PARAMS)
    
    Returns:
        float: Κόστος σπατάλης ανά μερίδα
    """
    if waste_fraction is None:
        waste_fraction = PARAMS["waste_fraction"]
    if waste_penalty is None:
        waste_penalty = PARAMS["waste_penalty_factor"]
    
    mat_cost = ingredient_cost_per_portion(dish_code)
    return mat_cost * waste_fraction * waste_penalty


def variable_cost_per_portion(dish_code, waste_fraction=None, waste_penalty=None):
    """
    Συνολικό μεταβλητό κόστος ανά μερίδα: υλικά + εργασία + σπατάλη (€).
    
    Args:
        dish_code (str): Κωδικός πιάτου
        waste_fraction (float): Ποσοστό σπατάλης
        waste_penalty (float): Συντελεστής ποινής σπατάλης
    
    Returns:
        float: Συνολικό μεταβλητό κόστος ανά μερίδα
    """
    mat = ingredient_cost_per_portion(dish_code)
    lab = labor_cost_per_portion(dish_code)
    waste = waste_cost_per_portion(dish_code, waste_fraction, waste_penalty)
    return mat + lab + waste


def contribution_margin(dish_code, waste_fraction=None, waste_penalty=None):
    """
    Περιθώριο συνεισφοράς ανά μερίδα = τιμή πώλησης - μεταβλητό κόστος (€).
    
    Args:
        dish_code (str): Κωδικός πιάτου
        waste_fraction (float): Ποσοστό σπατάλης
        waste_penalty (float): Συντελεστής ποινής σπατάλης
    
    Returns:
        float: Περιθώριο συνεισφοράς ανά μερίδα
    """
    price = DISHES[dish_code]["price"]
    var_cost = variable_cost_per_portion(dish_code, waste_fraction, waste_penalty)
    return price - var_cost


def margin_per_labor_hour(dish_code, waste_fraction=None, waste_penalty=None):
    """
    Περιθώριο συνεισφοράς ανά εργατoώρα που απαιτείται.
    
    Χρήσιμο μέτρο για αξιολόγηση αποδοτικότητας δεδομένου του περιορισμένου χρόνου εργασίας.
    
    Args:
        dish_code (str): Κωδικός πιάτου
        waste_fraction (float): Ποσοστό σπατάλης
        waste_penalty (float): Συντελεστής ποινής σπατάλης
    
    Returns:
        float: Περιθώριο συνεισφοράς ανά εργατoώρα
    """
    margin = contribution_margin(dish_code, waste_fraction, waste_penalty)
    labor_hours = DISHES[dish_code]["labor_min"] / 60.0
    if labor_hours > 0:
        return margin / labor_hours
    return 0.0


if __name__ == "__main__":
    print("=" * 90)
    print("ΑΝΑΛΥΣΗ ΠΙΑΤΩΝ — Κόστος & Περιθώρια Συνεισφοράς")
    print("=" * 90)
    print(f"{'Πιάτο':<30} {'Τιμή':>8} {'Κ.Υλ':>8} {'Κ.Εργ':>8} {'Κ.Σπα':>8} {'Περιθ':>8} {'Περ/Ώρα':>10}")
    print("-" * 90)
    
    for code, d in DISHES.items():
        price = d["price"]
        mat_cost = ingredient_cost_per_portion(code)
        lab_cost = labor_cost_per_portion(code)
        waste_cost = waste_cost_per_portion(code)
        margin = contribution_margin(code)
        margin_hour = margin_per_labor_hour(code)
        
        print(f"{d['name']:<30} {price:>8.2f} {mat_cost:>8.2f} {lab_cost:>8.2f} {waste_cost:>8.2f} {margin:>8.2f} {margin_hour:>10.2f}")
    
    print("=" * 90)
    print(f"Σύνολο πιάτων: {len(DISHES)}")
    print(f"Σύνολο υλικών: {len(INGREDIENTS)}")
    print(f"Διαθέσιμες εργατοώρες/ημέρα: {PARAMS['labor_hours_available']}")

