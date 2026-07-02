# Menu_Optimization

Εργασία για το μάθημα **Γραμμική & Συνδυαστική Βελτιστοποίηση** — βελτιστοποίηση
του ημερήσιου μενού ενός εστιατορίου με **Γραμμικό (LP)** και **Μικτό Ακέραιο
(MIP)** Προγραμματισμό, με πλήρη **δυϊκή ανάλυση** (σκιώδεις τιμές, μειωμένα κόστη,
ισχυρή δυϊκότητα, συμπληρωματική χαλαρότητα).

## Δομή

| Αρχείο | Περιγραφή |
|---|---|
| `data.py` | Βάση δεδομένων: 52 πρώτες ύλες, 21 συνταγές, παράμετροι + συναρτήσεις κοστολόγησης |
| `optimize.py` | Μοντέλα **LP** & **MIP** (PuLP/CBC), αναλύσεις ευαισθησίας, **LP-χαλάρωση του MIP & διάκενο ακεραιότητας** |
| `duality.py` | **[Νέο]** Δυϊκή ανάλυση του LP: δυϊκό πρόβλημα, σκιώδεις τιμές, μειωμένα κόστη, έλεγχος ισχυρής δυϊκότητας & συμπληρωματικής χαλαρότητας |
| `ranging.py` | **[Νέο]** Παραμετρική ανάλυση: εύρος δεξιού μέλους (RHS ranging) & εύρος συντελεστών αντικειμενικής (objective ranging) |
| `make_results.py` | Εκτέλεση όλων των μοντέλων → `results.json` |
| `make_charts.py`, `make_charts2.py` | Γραφήματα 1–8 (κόστη, αποδοτικότητα, LP/MIP, ευαισθησία) |
| `make_duality_charts.py` | **[Νέο]** Γραφήματα μειωμένου κόστους & σκιωδών τιμών ζήτησης |
| `make_ranging_chart.py` | **[Νέο]** Παραμετρικό γράφημα κέρδους ως προς τις εργατοώρες |
| `make_tables.py` | **[Νέο]** Παραγωγή των πινάκων LaTeX της αναφοράς απευθείας από τον κώδικα |
| `report/report.tex` | Πλήρης αναφορά (24 σελίδες) — μεταγλωττίζεται με `lualatex` |
| `slides/presentation.tex` | Παρουσίαση (Beamer, 22 διαφάνειες, ελληνικά, ~20 λεπτά) |
| `slides/transcript.md` | Κείμενο ομιλητή για την παρουσίαση |

## Εκτέλεση (Python)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/python data.py            # ανάλυση κόστους πιάτων
.venv/bin/python optimize.py        # LP + MIP + ανάλυση ευαισθησίας
.venv/bin/python duality.py         # δυϊκή ανάλυση (→ duality.json)
.venv/bin/python ranging.py         # παραμετρική ανάλυση / ranging (→ ranging.json)
.venv/bin/python make_results.py    # → results.json
.venv/bin/python make_charts.py
.venv/bin/python make_charts2.py    # γραφήματα 1–8 + explain.json
.venv/bin/python make_duality_charts.py   # γραφήματα μειωμένου κόστους / σκιωδών τιμών
.venv/bin/python make_ranging_chart.py    # παραμετρικό γράφημα
.venv/bin/python make_tables.py     # πίνακες LaTeX (→ report/tables/)
```

## Μεταγλώττιση εγγράφων (LaTeX)

Απαιτείται **LuaLaTeX** και οι γραμματοσειρές **GFS** (`fonts-gfs-*`) και
**TeX Gyre**. Τα ελληνικά χειρίζονται μέσω `polyglossia` + `fontspec`.

```bash
# Αναφορά (3 περάσματα για πίνακα περιεχομένων/παραπομπές)
cd report && for i in 1 2 3; do lualatex -interaction=nonstopmode report.tex; done

# Παρουσίαση
cd slides && lualatex presentation.tex && lualatex presentation.tex
```

> Σημείωση: κατά τη μεταγλώττιση **μην** ανακατευθύνετε το log σε αρχείο
> `<jobname>.out` — συγκρούεται με το αρχείο σελιδοδεικτών του hyperref.

## Βασικά αποτελέσματα

- **LP** (άνω φράγμα): **1976,41 €/ημέρα**
- **MIP** (υλοποιήσιμο, 10 πιάτα): **1709,53 €/ημέρα**
- Διαφορά = 241 € πάγια κόστη + 26 € ακεραιότητα
- **Σκιώδης τιμή εργασίας** `u* = 20,37 €/ώρα` ≫ ωρομίσθιο 7,80 €/ώρα
- Ισχυρή δυϊκότητα: `Z* = W* = 1976,41 €` (επιβεβαιωμένη αριθμητικά)
- Εύρος ισχύος του `u*`: `H ∈ [61,88, 69,35]` ώρες (RHS ranging)
- Διάκενο ακεραιότητας MIP: `6,35 €` (0,37%) — 2 κλασματικές μεταβλητές στη ρίζα του B&B
