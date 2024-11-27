#import
#==========================================================================
import sympy as sp

#functie
#==========================================================================
def evalueer_sympy_functie(sympy_functie, x_waarde):
    if isinstance(sympy_functie, str):
        sympy_functie = sp.sympify(sympy_functie)
    x = sp.symbols('x')
    return sympy_functie.subs(x, x_waarde).evalf()

#uitleg
#==========================================================================
""" 
Parameters:
    sympy_functie (sympy expressie): De functie (sympy).
    x_waarde (float): De x-waardes van de functie.
Retourneert:
    float: Functiewaarde.
"""