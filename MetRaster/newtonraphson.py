#import
#==========================================================================
import sympy as sp
from functiewaarde import evalueer_sympy_functie

#functie
#==========================================================================
def NewtonRaphsonOplosser(functie, x0, tol, max_iter):
    x = sp.symbols('x')  # Symbool voor differentiatie
    f_afgeleide = sp.diff(functie, x)  # Bereken de afgeleide van de functie
        
    for stap in range(1, max_iter + 1):
        f_waarde = evalueer_sympy_functie(functie, x0)  # Eval functie bij x0
        f_afgeleide_waarde = evalueer_sympy_functie(f_afgeleide, x0)  # Eval afgeleide bij x0
        
        if f_afgeleide_waarde == 0:
            return (None, stap)  # Stop als afgeleide nul is (geen deling door nul)

        x1 = x0 - f_waarde / f_afgeleide_waarde  # Newton-Raphson formule

        if abs(f_waarde) <= tol:  # Controleer of de fout binnen de tolerantie ligt
            return (float(x1), stap)

        x0 = x1  # Update schatting voor volgende iteratie
    return (None, stap)

#uitleg
#==========================================================================
""" 
Parameters:
    functie (sympy expressie): De functie waarvan we nulwaarden zoeken.
    x0 (float): Initiële waarde.
    tol (float): Tolerantie.
    max_iter (int): Maximum aantal herhalingen.
Retourneert:
    wortel (float): De gevonden nulwaarde.
    iteraties (int): Aantal herhalingen.
"""