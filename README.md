---

# OnderzoekNulwaarden

OnderzoekNulwaarden is een project waarmee je wiskundige functies kunt analyseren en hun nulpunten kunt berekenen met behulp van verschillende numerieke methoden, waaronder de bisectiemethode, de Newton-Raphson-methode en de secant-methode. Het bevat ook een interactieve grafische gebruikersinterface (GUI) voor het visualiseren van functies en het toepassen van deze methoden.

## Overzicht van het Project

1. **Eerste Document**:  
   Dit programma biedt de mogelijkheid om een enkele functie op te lossen voor één nulpunt. Gebruikers kunnen kiezen welke numerieke methode (bisectie, Newton-Raphson of secant) ze willen gebruiken.

2. **Folder met Raster**:  
   Deze folder bevat alle bestanden die nodig zijn voor het programma met de rastermethode, inclusief:
   - Python-bestanden die de functionaliteit implementeren.
   - Een video-uitleg over hoe het programma werkt en hoe het gebruikt kan worden.

## Functies

- **GUI voor Visualisatie**: Een gebruiksvriendelijke grafische interface waarin je een functie kunt invoeren, een interval kunt opgeven en de nulpunten visueel kunt bekijken.  
- **Numerieke Methoden**: Kies tussen verschillende methoden om nulpunten te berekenen.  
- **Thema-selectie**: Pas de interface aan met verschillende stijlen.  
- **Interactiviteit**: Gebruik zoom en pan om grafieken beter te inspecteren.

## Vereisten

- Python 3.10 of hoger
- Matplotlib
- SymPy
- NumPy
- tkinter (meestal standaard meegeleverd)

## Installatie

1. Download de benodigde bestanden uit de folder. Zorg ervoor dat alle bestanden in dezelfde directory staan.
2. Voer de volgende pip-installatie uit om de benodigde pakketten te installeren:

   ```bash
   pip install -r requirements.txt
   ```

   *Opmerking*: De `requirements.txt` bevat de vereiste Python-bibliotheken voor dit project. Zorg ervoor dat je deze toevoegt aan je project.

3. Run het programma in de terminal:

   ```bash
   python Main.py
   ```

## Bestandsoverzicht

- **`Main_2.0(Optimization+GUI).py`**: Hoofdbestand met de GUI voor visualisatie en berekening.
- **`bisectie.py`**: Bevat de implementatie van de bisectiemethode.
- **`secant.py`**: Bevat de implementatie van de secant-methode.
- **`interval.py`**: Bevat logica voor het berekenen van optimale intervallen voor grafieken.
- **`functiewaarde.py`**: Hulpfuncties voor het evalueren van functies.
- **Video**: Uitlegvideo over het gebruik van het programma.

## Gebruik

1. Open het programma met `python Main_2.0(Optimization+GUI).py`.
2. Voer een functie in, zoals `x**2 - 4`.
3. Geef een interval op (optioneel). Het programma berekent automatisch een interval als je dit niet invult.
4. Klik op "Plot Functie" om de grafiek te genereren en de numerieke methoden toe te passen.
5. Bekijk de resultaten in de GUI, inclusief de gevonden nulpunten en iteraties per methode.

## Ondersteuning

De video in de folder geeft een uitgebreide uitleg over het gebruik van dit programma. Mocht je verdere vragen hebben, open een issue in deze repository.

---
