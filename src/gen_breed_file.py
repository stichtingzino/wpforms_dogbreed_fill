import csv
import json
import os
from typing import List
from google import genai
from google.genai import types
from pydantic import BaseModel

# 1. Definieer de gewenste JSON-structuur met Pydantic
class BreedGroup(BaseModel):
    fci_group: int
    group_name: str
    breeds: List[str]

class LanguageDataset(BaseModel):
    groups: List[BreedGroup]

# 2. Initialiseer de Gemini Client
# Zorg dat de omgevingsvariabele GEMINI_API_KEY is ingesteld op je systeem,
# of geef hem hier direct mee: client = genai.Client(api_key="JOUW_API_KEY")
client = genai.Client()

def haal_data_op_via_gemini(taal_naam: str) -> dict:
    """Stuurt een prompt naar Gemini en dwingt een gestructureerde JSON-output af."""
    print(f"Bezig met ophalen van de FCI-data voor de taal: {taal_naam}...")
    
    prompt = f"""
    Genereer een uitgebreid overzicht van hondenrassen per officiële FCI-rasgroep (1 tot en met 10), 
    gebaseerd op de rassen uit de database van het Nederlandse LICG. 
    
    Vertaal zowel de namen van de FCI-groepen als de namen van de hondenrassen naar de officiële 
    kynologische benamingen in het {taal_naam}. Zorg dat de lijst met rassen per groep zo uitgebreid 
    en compleet mogelijk is.
    """
    
    # We gebruiken gemini-2.5-flash omdat deze perfect is voor gestructureerde data-taken
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=LanguageDataset, # Dwingt Gemini om de Pydantic-structuur te volgen
            temperature=0.1 # Lage temperatuur voor consistente en accurate data
        ),
    )
    
    # De response.text bevat nu gegarandeerd een valide JSON die matcht met ons Pydantic model
    return json.loads(response.text)

# 3. Hoofdprogramma voor het genereren van de bestanden
def main():
    # Definieer de talen, de weergavenaam voor de prompt en de gewenste bestandsnaam-suffix
    talen_config = {
        "nl": {"prompt_taal": "Nederlands", "filename": "fci_rassen_nl"},
        "en": {"prompt_taal": "Engels (English)", "filename": "fci_rassen_en"},
        "fr": {"prompt_taal": "Frans (Français)", "filename": "fci_rassen_fr"},
        "de": {"prompt_taal": "Duits (Deutsch)", "filename": "fci_rassen_de"}
    }
    
    # Maak de exportmap aan
    output_dir = "fci_datasets_gemini"
    os.makedirs(output_dir, exist_ok=True)
    
    # Loop door de geconfigureerde talen en vul 'dog_data' live via de API
    for lang_code, config in talen_config.items():
        try:
            # Haal de live data op via de Gemini API query
            live_data = haal_data_op_via_gemini(config["prompt_taal"])
            
            base_name = os.path.join(output_dir, config["filename"])
            
            # --- CSV EXPORT ---
            csv_file = f"{base_name}.csv"
            with open(csv_file, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["FCI_Group", "Group_Name", "Breeds"])
                
                for item in live_data["groups"]:
                    breeds_str = ";".join(item["breeds"])
                    writer.writerow([item["fci_group"], item["group_name"], breeds_str])
                    
            # --- JSON EXPORT ---
            json_file = f"{base_name}.json"
            with open(json_file, mode='w', encoding='utf-8') as f:
                json.dump(live_data["groups"], f, ensure_ascii=False, indent=2)
                
            print(f"-> Succesvol opgeslagen: {csv_file} en {json_file}")
            
        except Exception as e:
            print(f"Fout opgetreden bij het verwerken van {config['prompt_taal']}: {e}")

    print(f"\nKlaar! Alle gegenereerde bestanden staan in de map: '{output_dir}/'")

if __name__ == "__main__":
    main()
