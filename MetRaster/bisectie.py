#imports
#======================================================================
import numpy as np
from functiewaarde import evalueer_sympy_functie

#functie
#======================================================================
def BisectieOplosser(f, a, b, tol, max_iteraties, iteratie=1):
    fa = evalueer_sympy_functie(f, a)  # Bereken f(a)
    fb = evalueer_sympy_functie(f, b)  # Bereken f(b)
    
    if np.sign(fa) == np.sign(fb):
        return None, iteratie

    m = (a + b)/2  # Bereken het middenpunt
    fm = evalueer_sympy_functie(f, m)  # Bereken f(m)
    if iteratie <= max_iteraties:
        if np.abs(fm) < tol:  # Stopconditie: m als wortel rapporteren
            return m, iteratie
        elif np.sign(fa) == np.sign(fm):  # Het middenpunt verbetert a. Roep opnieuw aan met a = m
            return BisectieOplosser(f, m, b, tol, iteratie+1)
        elif np.sign(fb) == np.sign(fm):  # Het middenpunt verbetert b. Roep opnieuw aan met b = m
            return BisectieOplosser(f, a, m, tol, iteratie+1)
    else:
        return None, iteratie
    
#uitleg
#======================================================================
""" 
Parameters:
    f (sympy expressie): De functie waarvan we de nulwaarden zoeken.
    a (float): Laagste waarde van het interval.
    b (float): Hoogste waarde van het interval.
    tol (float): Tolerantie.
    iteratie (int): Herhalingsteller.
Retourneert:
    wortel (float): De gevonden nulwaarde.
    iteraties (int): Het aantal herhalingen nodig om de nulwaarde te vinden.
"""