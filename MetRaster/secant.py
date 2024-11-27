#import
#==========================================================================
import sympy as sp
from functiewaarde import evalueer_sympy_functie

#functie
#==========================================================================
def SecantOplosser(functie, x0, x1, tol, max_iter):
    x = sp.symbols('x')  # Symbool voor substitutie

    for stap in range(1, max_iter + 1):
        f_x0 = evalueer_sympy_functie(functie, x0)  # f(x0)
        f_x1 = evalueer_sympy_functie(functie, x1)  # f(x1)

        if f_x1 - f_x0 == 0:
            return (None, stap)  # Vermijd deling door nul

        x2 = x0 - (x1 - x0) * f_x0 / (f_x1 - f_x0)  # Secant-formule
        f_x2 = evalueer_sympy_functie(functie, x2)  # Eval functie bij x2

        if abs(f_x2) <= tol:  # Controleer of fout binnen tolerantie ligt
            return (float(x2), stap)

        # Update schattingen
        x0 = x1
        x1 = x2
        
    return None

#uitleg
#==========================================================================
""" 
Parameters:
    functie (sympy expressie): De functie waarvan we nulwaarden zoeken.
    x0 (float): Eerste initiële waarde.
    x1 (float): Tweede initiële waarde.
    tol (float): Toelaatbare fout.
    max_iter (int): Maximum aantal iteraties.
Retourneert:
    wortel (float): De benaderde wortel (indien gevonden).
    None: Indien de methode niet convergeert.
"""