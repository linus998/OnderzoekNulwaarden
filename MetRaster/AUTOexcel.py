#imports
#==================================================================================================================================
import numpy as np
from sympy import Symbol, solve
import random
from openpyxl import Workbook

#methodes
#==================================================================================================================================
from bisectie import BisectieOplosser
from secant import SecantOplosser
from newtonraphson import NewtonRaphsonOplosser
from functiewaarde import evalueer_sympy_functie

# Global Variables
#==================================================================================================================================
TOLERANTIE = 1e-10
MAXIMUM_HERHALINGEN = 100
x_min = -10.3
x_max = 10.3

# Functions
#==================================================================================================================================
def find_roots_and_log_to_excel(functie, x_max, x_min, index, sheet):
    iteratiesBisectie, iteratiesNewtonRaphson, iteratiesSecant = 0, 0, 0
    wortelsBisectie, wortelsNewtonRaphson, wortelsSecant = [], [], []
    accuracies = []

    val = x_min
    while val < x_max:
        f1 = evalueer_sympy_functie(functie, val)
        f2 = evalueer_sympy_functie(functie, val + 1)
        if np.sign(f1) != np.sign(f2):
            # Bisectie
            wortel, iteraties = BisectieOplosser(functie, val + 1, val, TOLERANTIE, MAXIMUM_HERHALINGEN)
            iteratiesBisectie += iteraties
            if wortel is not None:
                wortelsBisectie.append(float(wortel))

            # Newton-Raphson
            wortel, iteraties = NewtonRaphsonOplosser(functie, val, TOLERANTIE, MAXIMUM_HERHALINGEN)
            iteratiesNewtonRaphson += iteraties
            if wortel is not None:
                wortelsNewtonRaphson.append(float(wortel))

            # Secant
            result = SecantOplosser(functie, x0=val, x1=val + 1, tol=TOLERANTIE, max_iter=MAXIMUM_HERHALINGEN)
            if result is not None:  # Controleer of de Secant-methode succesvol is
                wortel, iteraties = result
                iteratiesSecant += iteraties
                wortelsSecant.append(float(wortel))

        val += 1

    x = Symbol("x")
    echte_wortels = [float(w) for w in solve(functie, x) if w.is_real]

    wortelsBisectie_str = ", ".join(map(str, wortelsBisectie)) if wortelsBisectie else "-"
    wortelsNewtonRaphson_str = ", ".join(map(str, wortelsNewtonRaphson)) if wortelsNewtonRaphson else "-"
    wortelsSecant_str = ", ".join(map(str, wortelsSecant)) if wortelsSecant else "-"

    accuracies_str = ", ".join(
        [f"Bis: {acc[0]}, New: {acc[1]}, Sec: {acc[2]}" for acc in accuracies]
    ) if accuracies else "-"

    sheet.append([
        index, str(functie), len(echte_wortels),
        iteratiesBisectie, iteratiesNewtonRaphson, iteratiesSecant,
        wortelsBisectie_str, wortelsNewtonRaphson_str, wortelsSecant_str,
        accuracies_str
    ])


# Setup Excel Workbook
wb = Workbook()
sheet = wb.active
sheet.title = "Resultaten"
sheet.append(["#", "Functie", "Aantal Nulpunten", "Iteraties Bis", "Iteraties New", "Iteraties Sec", 
              "Wortels Bis", "Wortels New", "Wortels Sec", "Accuraatheid"])

# Generatie en verwerking
x = Symbol("x")
aantal_functies = 100  # Pas dit aan om het aantal te controleren

for i in range(1, aantal_functies + 1):
    degree = random.randint(2, 5)  # Willekeurige graad
    terms = random.randint(2, degree)  # Willekeurig aantal termen
    coefficients = [random.randint(-10, 10) for _ in range(terms)]
    exponents = sorted(random.sample(range(degree + 1), terms), reverse=True)
    polynomial = sum(coeff * x**exp for coeff, exp in zip(coefficients, exponents))

    # Verwerk de gegenereerde functie
    find_roots_and_log_to_excel(polynomial, x_max, x_min, i, sheet)

# Sla resultaten op
wb.save("resultaten.xlsx")
print("Resultaten opgeslagen in 'resultaten.xlsx'.")
