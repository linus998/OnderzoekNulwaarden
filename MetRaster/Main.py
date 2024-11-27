#imports
#==================================================================================================================================
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, sympify, solve
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

# Functions
#==================================================================================================================================
def validate_inputs():
    """Validates user inputs and returns the parsed function and interval."""
    try:
        functie = sympify(functie_invoer.get())
    except Exception as e:
        raise ValueError(f"Fout in functie-invoer: {e}")
    
    try:
        x_min = float(x_min_invoer.get()) if x_min_invoer.get() else None
        x_max = float(x_max_invoer.get()) if x_max_invoer.get() else None
    except ValueError:
        raise ValueError("x-min en x-max moeten getallen zijn.")
    
    return functie, x_min, x_max

def calculate_interval(functie, x_min, x_max):
    """Calculates an optimal interval if not provided."""
    if x_min is None or x_max is None:
        try:
            x_min, x_max = optimaal_bereik(functie, Symbol('x'))
        except Exception:
            raise ValueError("Kan het interval niet berekenen.")
    return x_min, x_max

def plot_grafiek():
    try:
        functie, x_min, x_max = validate_inputs()
        x_min, x_max = calculate_interval(functie, x_min, x_max)
        
        x = Symbol("x")
        x_waarden = np.linspace(x_min, x_max, 400)
        y_waarden = [functie.evalf(subs={x: val}) for val in x_waarden]

        # Plot
        ax.clear()
        ax.plot(x_waarden, y_waarden, label=f"y = {functie}")
        ax.axhline(0, color="black", linewidth=0.5)  # x-axis
        ax.axvline(0, color="black", linewidth=0.5)  # y-axis
        ax.grid(color="gray", linestyle="--", linewidth=0.5)

        # Root-finding methods
        iteratiesBisectie, iteratiesNewtonRaphson, iteratiesSecant = 0, 0, 0
        wortelsBisectie, wortelsNewtonRaphson, wortelsSecant = [], [], []

        val = x_min
        while val < x_max:
            f1 = evalueer_sympy_functie(functie, val)
            f2 = evalueer_sympy_functie(functie, val + 1)
            if np.sign(f1) != np.sign(f2):
                
                wortel, iteraties = BisectieOplosser(functie, val + 1, val, TOLERANTIE, MAXIMUM_HERHALINGEN)
                iteratiesBisectie += iteraties
                if wortel is not None:
                    wortelsBisectie.append(float(wortel))

                wortel, iteraties = NewtonRaphsonOplosser(functie, val, TOLERANTIE, MAXIMUM_HERHALINGEN)
                iteratiesNewtonRaphson += iteraties
                if wortel is not None:
                    wortelsNewtonRaphson.append(float(wortel))

                wortel, iteraties = SecantOplosser(functie, x0=val, x1=val + 1, tol=TOLERANTIE, max_iter=MAXIMUM_HERHALINGEN)
                iteratiesSecant += iteraties
                if wortel is not None:
                    wortelsSecant.append(float(wortel))

            #next in interval
            val += 1
        
        # Find roots
        wortels = solve(functie, x)
        echte_wortels = [float(w) for w in wortels if w.is_real]
        for wortel in echte_wortels:
            ax.plot(wortel, 0, "ro")

        # Update labels
        wortelLabel.config(text=f"Wortels:{echte_wortels} Bis:{wortelsBisectie}, NR:{wortelsNewtonRaphson}, Sec:{wortelsSecant}")
        iteratiesLabel.config(text=f"Iteraties: Bisectie={iteratiesBisectie}, Newton-Raphson={iteratiesNewtonRaphson}, Secant={iteratiesSecant}")
        # Add Legend and Redraw
        ax.legend()
        canvas.draw()
    except ValueError as e:
        wortelLabel.config(text=f"Fout: {e}")
    except Exception as e:
        wortelLabel.config(text=f"Onverwachte fout: {e}")

def update_theme(theme):
    """Updates the theme of the application."""
    style.theme_use(theme)

# TKINTER GUI Setup
#==================================================================================================================================
root = tk.Tk()
root.title("Worteloplossing")
root.geometry("800x700")
root.resizable(True, True)

# Apply a default theme
style = ttk.Style(root)
style.theme_use("clam")  # Default theme

# Input Frame
input_frame = ttk.LabelFrame(root, text="Invoer", padding=10)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(input_frame, text="Functie:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
functie_invoer = ttk.Entry(input_frame, width=30)
functie_invoer.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="x-min:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
x_min_invoer = ttk.Entry(input_frame, width=15)
x_min_invoer.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="x-max:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
x_max_invoer = ttk.Entry(input_frame, width=15)
x_max_invoer.grid(row=2, column=1, padx=5, pady=5)

# Theme Selector
theme_label = ttk.Label(input_frame, text="Thema:")
theme_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
theme_selector = ttk.Combobox(input_frame, values=style.theme_names())
theme_selector.grid(row=3, column=1, padx=5, pady=5)
theme_selector.set("clam")
theme_selector.bind("<<ComboboxSelected>>", lambda e: update_theme(theme_selector.get()))

# Plot Button
plot_knop = ttk.Button(root, text="Plot Functie", command=plot_grafiek)
plot_knop.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Output Frame
output_frame = ttk.LabelFrame(root, text="Resultaten", padding=10)
output_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

wortelLabel = ttk.Label(output_frame, text="Wortels:", anchor="w")
wortelLabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")

iteratiesLabel = ttk.Label(output_frame, text="Iteraties:", anchor="w")
iteratiesLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
# Graph Area
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

# Toolbar for Interactive Graph
toolbar_frame = ttk.Frame(root)
toolbar_frame.grid(row=4, column=0, pady=10)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

# Configure resizing
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(0, weight=1)

# Run the Application
root.mainloop()
