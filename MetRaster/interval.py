#import
#==========================================================================
from sympy import symbols, diff, solve

#functie
#==========================================================================
def optimaal_bereik(f, var, interval=None):
    # Bereken de eerste afgeleide
    f_prime = diff(f, var)
    
    # Vind kritieke punten (waar f'(x) = 0)
    kritieke_punten = solve(f_prime, var)
    kritieke_punten = [punt.evalf() for punt in kritieke_punten]  # Converteer naar numerieke waarden
    
    # Voeg grenzen van het interval toe (indien gegeven)
    if interval:
        min_interval, max_interval = interval
        relevante_punten = kritieke_punten + [min_interval, max_interval]
    else:
        relevante_punten = kritieke_punten

    # Controleer of er relevante punten zijn
    if not relevante_punten:
        return None
    
    # Bepaal het minimum en maximum bereik
    min_x = min(relevante_punten)
    max_x = max(relevante_punten)

    # Optionele marge toevoegen
    marge = 0.1 * (max_x - min_x) if max_x > min_x else 1
    min_x -= marge
    max_x += marge

    return float(min_x), float(max_x)

#uitleg
#==========================================================================
"""
Parameters:
    f: SymPy-expressie van de functie.
    var: SymPy-symbool van de variabele.
    interval: Optioneel, een tuple (min_x, max_x) met een voorgesteld bereik.
Retourneert:
    Tuple (min_x, max_x) met het optimale bereik.
"""