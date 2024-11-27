#imports
#==================================================================================================================================
import numpy as np
from sympy import Symbol, sympify, solve
import random

#methodes
#==================================================================================================================================
from bisectie import BisectieOplosser
from secant import SecantOplosser
from newtonraphson import NewtonRaphsonOplosser
from interval import optimaal_bereik
from functiewaarde import evalueer_sympy_functie

# Global Variables
#==================================================================================================================================
TOLERANTIE = 1e-10
MAXIMUM_HERHALINGEN = 100
x_min = -10.3
x_max = 10.3

# Functions
#==================================================================================================================================
def plot_grafiek(functie, x_max, x_min, index):
    """Bereken nulpunten en log de resultaten naar een bestand."""
    iteratiesBisectie, iteratiesNewtonRaphson, iteratiesSecant = 0, 0, 0
    wortelsBisectie, wortelsNewtonRaphson, wortelsSecant = [], [], []

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
            wortel, iteraties = SecantOplosser(functie, x0=val, x1=val + 1, tol=TOLERANTIE, max_iter=MAXIMUM_HERHALINGEN)
            iteratiesSecant += iteraties
            if wortel is not None:
                wortelsSecant.append(float(wortel))

        val += 1  # Volgend interval

    # Bereken exacte wortels
    x = Symbol("x")
    wortels = solve(functie, x)
    echte_wortels = [float(w) for w in wortels if w.is_real]

    # Log resultaten
    with open("resultaten.txt", "a") as file:
        file.write(f"--- Functie {index} ---\n")
        file.write(f"Functie: {functie}\n")
        file.write(f"Bisectie: {wortelsBisectie}\n")
        file.write(f"Newton-Raphson: {wortelsNewtonRaphson}\n")
        file.write(f"Secant: {wortelsSecant}\n")
        file.write(f"Echte wortels: {echte_wortels}\n")
        file.write(f"Iteraties bisectie: {iteratiesBisectie}\n")
        file.write(f"Iteraties Newton-Raphson: {iteratiesNewtonRaphson}\n")
        file.write(f"Iteraties Secant: {iteratiesSecant}\n\n")

    print(f"Functie {index} voltooid.")

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
    plot_grafiek(polynomial, x_max, x_min, i)
