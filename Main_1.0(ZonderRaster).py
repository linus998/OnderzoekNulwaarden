#imports
#==================================================================================================================================
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, sympify, solve
import sympy as sp

#globale variabelen
#==================================================================================================================================
TOLERANTIE = 1e-6  # Toelaatbare afwijking op de nulwaarden
#bisectie
MAXIMUMWAARDE = 10  # De maximumwaarde (BISECTIE)
MINIMUMWAARDE = -10  # De minimumwaarde (BISECTIE)
#Newton-Raphson
BEGINSCHATTING = -2
MAXIMUMHERHALINGEN = 100  # Maximale aantal herhalingen (alle methodes)

#helperfuncties
#==================================================================================================================================
def evalueer_sympy_functie(sympy_functie, x_waarde):
    """ Parameters:
            sympy_functie (sympy expressie): De functie (sympy).
            x_waarde (float): De x-waardes van de functie.
        Retourneert:
            float: Functiewaarde.
    """
    if isinstance(sympy_functie, str):
        sympy_functie = sp.sympify(sympy_functie)
    x = sp.symbols('x')
    return sympy_functie.subs(x, x_waarde).evalf()

#hoofdmethodes
#==================================================================================================================================
def BisectieOplosser(f, a, b, tol, iteratie):
    """ Parameters:
            f (sympy expressie): De functie waarvan we de nulwaarden zoeken.
            a (float): Laagste waarde van het interval.
            b (float): Hoogste waarde van het interval.
            tol (float): Tolerantie.
            iteratie (int): Herhalingsteller.
        Retourneert:
            wortel (float): De gevonden nulwaarde.
            iteraties (int): Het aantal herhalingen nodig om de nulwaarde te vinden.
    """
    fa = evalueer_sympy_functie(f, a)  # Bereken f(a)
    fb = evalueer_sympy_functie(f, b)  # Bereken f(b)
    
    if np.sign(fa) == np.sign(fb):
        raise Exception("Er zit geen nulpunt in het interval")

    m = (a + b)/2  # Bereken het middenpunt
    fm = evalueer_sympy_functie(f, m)  # Bereken f(m)
    
    if np.abs(fm) < tol:  # Stopconditie: m als wortel rapporteren
        return m, iteratie
    elif np.sign(fa) == np.sign(fm):  # Het middenpunt verbetert a. Roep opnieuw aan met a = m
        return BisectieOplosser(f, m, b, tol, iteratie+1)
    elif np.sign(fb) == np.sign(fm):  # Het middenpunt verbetert b. Roep opnieuw aan met b = m
        return BisectieOplosser(f, a, m, tol, iteratie+1)

def NewtonRaphsonOplosser(functie, x0, tol, max_iter):
    """ Parameters:
            functie (sympy expressie): De functie waarvan we nulwaarden zoeken.
            x0 (float): Initiële waarde.
            tol (float): Tolerantie.
            max_iter (int): Maximum aantal herhalingen.
        Retourneert:
            wortel (float): De gevonden nulwaarde.
            iteraties (int): Aantal herhalingen.
    """
    x = sp.symbols('x')  # Symbool voor differentiatie
    f_afgeleide = sp.diff(functie, x)  # Bereken de afgeleide van de functie
        
    for stap in range(1, max_iter + 1):
        f_waarde = evalueer_sympy_functie(functie, x0)  # Eval functie bij x0
        f_afgeleide_waarde = evalueer_sympy_functie(f_afgeleide, x0)  # Eval afgeleide bij x0
        
        if f_afgeleide_waarde == 0:
            print(f"Herhaling {stap}: afgeleide is nul => stop.")
            return (None, stap)  # Stop als afgeleide nul is (geen deling door nul)

        x1 = x0 - f_waarde / f_afgeleide_waarde  # Newton-Raphson formule
        print(f"Herhaling {stap}, x1 = {x1:.6f}, f(x1) = {f_waarde:.6f}")

        if abs(f_waarde) <= tol:  # Controleer of de fout binnen de tolerantie ligt
            print(f"\nDe vereiste wortel is: {x1:.8f}")
            return (float(x1), stap)

        x0 = x1  # Update schatting voor volgende iteratie
    return (None, stap)

def SecantOplosser(functie, x0, x1, tol, max_iter):
    """ Parameters:
            functie (sympy expressie): De functie waarvan we nulwaarden zoeken.
            x0 (float): Eerste initiële waarde.
            x1 (float): Tweede initiële waarde.
            tol (float): Toelaatbare fout.
            max_iter (int): Maximum aantal iteraties.
        Retourneert:
            wortel (float): De benaderde wortel (indien gevonden).
            None: Indien de methode niet convergeert.
    """
    x = sp.symbols('x')  # Symbool voor substitutie

    for stap in range(1, max_iter + 1):
        f_x0 = evalueer_sympy_functie(functie, x0)  # f(x0)
        f_x1 = evalueer_sympy_functie(functie, x1)  # f(x1)

        if f_x1 - f_x0 == 0:
            print(f"Herhaling-{stap}: Deling door nul.")
            return (None, stap)  # Vermijd deling door nul

        x2 = x0 - (x1 - x0) * f_x0 / (f_x1 - f_x0)  # Secant-formule
        f_x2 = evalueer_sympy_functie(functie, x2)  # Eval functie bij x2

        print(f"Herhaling-{stap}, x2 = {x2:.6f}, f(x2) = {f_x2:.6f}")

        if abs(f_x2) <= tol:  # Controleer of fout binnen tolerantie ligt
            return (float(x2), stap)

        # Update schattingen
        x0 = x1
        x1 = x2

    print("\nNiet convergent binnen het maximale aantal herhalingen.")
    return None

# Functie om de grafiek te plotten
#==================================================================================================================================
def plot_grafiek():
    # Haal de functie op uit de invoer van de gebruiker
    functie = functie_invoer.get()

    x = Symbol('x')
    sympy_functie = sympify(functie)
    x_waarden = np.linspace(-10, 10, 400)
    y_waarden = [sympy_functie.evalf(subs={x: val}) for val in x_waarden]
    
    ax.clear()
    ax.plot(x_waarden, y_waarden, label=f"y = {functie}")
    
    # Zoek de nulpunten (wortels) met sympy of eigen methodes
    if methode_dropdown.get() == "Bisectie": 
        wortels, iteraties = BisectieOplosser(functie, MAXIMUMWAARDE, MINIMUMWAARDE, TOLERANTIE, 0)
        iteratiesLabel.config(text=f"Iteraties: {iteraties}")
        
    elif methode_dropdown.get() == "Newton-Raphson":
        wortels, iteraties = NewtonRaphsonOplosser(functie, BEGINSCHATTING, TOLERANTIE, MAXIMUMHERHALINGEN)
        iteratiesLabel.config(text=f"Iteraties: {iteraties}")

    elif methode_dropdown.get() == "Secant":
        wortels, iteraties = SecantOplosser(functie, x0=2.0, x1=2.5, tol=1e-6, max_iter=100)
        iteratiesLabel.config(text=f"Iteraties: {iteraties}")

    elif methode_dropdown.get() == "Referentie":
        wortels = solve(sympy_functie, x)

    echte_wortels = []
    if isinstance(wortels, list):
        for wortel in wortels:
            if wortel.is_real:
                echte_wortels.append(wortel)
                ax.plot(wortel, 0, 'ro')
    elif isinstance(wortels, float):
        echte_wortels.append(wortels)
        ax.plot(wortels, 0, 'ro')

    wortelLabel.config(text=f"Wortels: {echte_wortels}")

    # Voeg labels en een legenda toe
    ax.axhline(0, color='black', linewidth=0.5)  # x-as
    ax.axvline(0, color='black', linewidth=0.5)  # y-as
    ax.grid(color='gray', linestyle='--', linewidth=0.5)  # Raster
    ax.legend()

    canvas.draw()  # Verfris de grafiek

#TKINTER - GUI setup
#==================================================================================================================================
root = tk.Tk()
root.title("Worteloplossing")

functie_invoer = ttk.Entry(root)
functie_invoer.grid(row=0, column=0, padx=5, pady=5)

plot_knop = ttk.Button(root, text="Plot Functie", command=plot_grafiek)
plot_knop.grid(row=0, column=1, padx=5, pady=5)

methode_dropdown = ttk.Combobox(root, values=["Bisectie", "Newton-Raphson", "Secant", "Referentie"], state="readonly")
methode_dropdown.grid(row=1, column=0, padx=5, pady=5)
methode_dropdown.current(0)

wortelLabel = ttk.Label(root, text="Wortels:")
wortelLabel.grid(row=2, column=0, padx=5, pady=5)

iteratiesLabel = ttk.Label(root, text="Iteraties:")
iteratiesLabel.grid(row=2, column=1, padx=5, pady=5)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()