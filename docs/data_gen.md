# Data Generatie voor FCI Hondenrassen

Dit document beschrijft de functionaliteit van het Python-script `gen_breed_file.py`, dat zich richt op het genereren van een lijst van officiële FCI hondenrassen. Het script maakt gebruik van een AI-prompt om de hondenrassen op te halen en exporteert deze in JSON- en CSV-formaat voor meerdere talen.

## Hoofdfunctionaliteit

Het script voert de volgende stappen uit:

1. **Initialisatie**:
   - Importeer benodigde bibliotheken (`csv`, `json`, `os`, `logging`, `time`).
   - Importeer aangepaste functies en configuraties van andere bestanden in het project.

2. **Exportfunctie**:
   - `_export_data(base_name: str, live_data: dict)`: Deze functie exporteert de opgehaalde hondenrasgegevens naar zowel CSV- als JSON-bestanden.
     - **CSV Export**:
       - Schrijft de gegevens naar een CSV-bestand met kolommen voor `FCI_Group`, `Group_Name` en `Breeds`.
     - **JSON Export**:
       - Schrijft de gegevens naar een JSON-bestand met een structuur die de groepen en hun bijbehorende hondenrassen bevat.

3. **Hoofdprogramma**:
   - `get_dogbreeds()`: Deze functie beheert het genereren van de hondenraslijsten voor meerdere talen.
     - **Configuratie**:
       - Leest de configuratie voor de uitvoermap (`OUTPUT_DIRECTORY`), de beschikbare talen (`PROMPT_LANGUAGES`) en het voorvoegsel voor de doelbestandsnamen (`TARGET_FILENAME_PREFIX`).
     - **Directory Aanmaken**:
       - Maakt de uitvoermap aan als deze nog niet bestaat.
     - **Taalverwerking**:
       - Doorloopt elke geconfigureerde taal en haalt de live gegevens op via de Gemini API.
       - Implementeert een retry-mechanisme voor het afhandelen van tijdelijke fouten (503 Service Unavailable, 429 Rate Limit).
       - Voegt een kleine vertraging toe tussen de aanvragen voor elke taal om rate limiting te voorkomen.
     - **Gegevens Exporteren**:
       - Roep de `_export_data`-functie aan om de gegevens te exporteren naar CSV- en JSON-bestanden voor elke taal.

4. **Uitvoering**:
   - Het script wordt uitgevoerd als een zelfstandig programma door de `if __name__ == "__main__":`-constructie, die de `get_dogbreeds`-functie aanroept.

## Configuratie

De configuratie voor het script wordt beheerd via de `config.py`-bestand, waarin de volgende variabelen zijn gedefinieerd:

- `OUTPUT_DIRECTORY`: Het pad naar de map waar de gegenereerde bestanden worden opgeslagen.
- `PROMPT_LANGUAGES`: Een dictionary met de beschikbare talen en hun bijbehorende weergavenamen voor de prompt.
- `TARGET_FILENAME_PREFIX`: Het voorvoegsel dat wordt gebruikt voor de namen van de gegenereerde bestanden.

## Afhankelijkheden

Het script maakt gebruik van de volgende externe bibliotheken en functies:

- `csv`: Voor het schrijven van CSV-bestanden.
- `json`: Voor het schrijven van JSON-bestanden.
- `os`: Voor het beheer van bestandssystemen.
- `logging`: Voor het loggen van informatie en fouten.
- `time`: Voor het toevoegen van vertragingen tussen aanvragen.
- `google.genai.errors`: Voor het afhandelen van fouten van de Google GenAI API.
- `fci_dogbreeds.google_functions.functions.get_data_from_gemini`: Een aangepaste functie voor het ophalen van gegevens via de Gemini API.

## Uitvoer

Het script genereert de volgende uitvoerbestanden voor elke geconfigureerde taal:

- `TARGET_FILENAME_PREFIX<taalcode>.csv`: Een CSV-bestand met de hondenrasgegevens.
- `TARGET_FILENAME_PREFIX<taalcode>.json`: Een JSON-bestand met de hondenrasgegevens.

De bestanden worden opgeslagen in de `OUTPUT_DIRECTORY`.

## Voorbeeld

Stel dat de configuratie als volgt is ingesteld:

- `OUTPUT_DIRECTORY`: `data`
- `PROMPT_LANGUAGES`: `{"en": "English", "nl": "Nederlands"}`
- `TARGET_FILENAME_PREFIX`: `fci_breeds_`

Dan zal het script de volgende bestanden genereren:

- `data/fci_breeds_en.csv`
- `data/fci_breeds_en.json`
- `data/fci_breeds_nl.csv`
- `data/fci_breeds_nl.json`

Deze bestanden bevatten de lijst van officiële FCI hondenrassen voor de Engelse en Nederlandse talen.
