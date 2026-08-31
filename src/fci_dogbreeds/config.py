"""Default config options and read environment variables"""

import os
import asyncio
import logging
from fci_dogbreeds.onepw.functions import get_1pw_entry

logger = logging.getLogger(__name__)

def get_api_key(onepw_url: str | None = None) -> str | None:
    """ 
    Check if onepw_url is set and if so if it's an op:// string so it has to be 
    parsed from onepassword. If not, it returns the value of GOOGLE_API_KEY. 
    """
    if onepw_url is not None  and onepw_url.startswith("op://"):
        # Parse the op:// string to get the actual API key
        return asyncio.run(get_1pw_entry(onepw_url))

    return onepw_url

GOOGLE_API_KEY = get_api_key(os.getenv("GOOGLE_API_KEY", None))

# DATA_PROMPT = """
#  Genereer een uitgebreid overzicht van hondenrassen per officiële FCI-rasgroep (1 tot en met 10),
#  gebaseerd op de rassen uit de database van het Nederlandse LICG.
#
#  Vertaal zowel de namen van de FCI-groepen als de namen van de hondenrassen naar de officiële
#  kynologische benamingen in het %language%. Zorg dat de lijst met rassen per groep zo uitgebreid
#  en compleet mogelijk is.
#  """

TARGET_FILENAME_PREFIX = os.getenv("BREED_PREFIX","fci_breeds_")
PROMPT_LANGUAGES = {
    "NL": "Nederlands",
    "EN": "English",
    "FR": "Français",
    "DE": "Deutsch",
}
DATA_PROMPTS = {
    "NL": """
    Genereer een uitgebreid overzicht van hondenrassen per officiële FCI-rasgroep (1 tot en met 10), 
    gebaseerd op de rassen uit de database van het Nederlandse LICG. 

    Voor de namen van de FCI-groepen en de hondenrassen:
    - Hanteer de officiële en in de praktijk gangbare kynologische benamingen in het Nederlands. 
    - BELANGRIJK: Gebruik de specifieke Nederlandse rasnamen zoals gehanteerd door de Nederlandse Raad van Beheer en het LICG (bijvoorbeeld "Friese Stabij" of "Stabijhoun" in plaats van de internationale FCI-naam "Stabyhoun", en "Duitse Herdershond" in plaats van "Deutscher Schäferhund"). Vertaal buitenlandse namen niet letterlijk als er een ingeburgerde Nederlandse kynologische naam bestaat.
    - Als er twee of meer ingeburgerde namen zijn (zoals Friese Stabij/Stabijhoun) laat allebei de namen zien gescheiden door een "/"

    Zorg dat de lijst met rassen per groep zo uitgebreid en compleet mogelijk is.""",
    "EN": """Generate a comprehensive overview of dog breeds per official Royal Kennel Club breed group, based on the breeds from the database of the UK's Royal Kennel Club.For the names of the breed groups and the dog breeds: 
    - Maintain the official and practically common cynological terminology in English.
    - IMPORTANT: Use the specific English breed names as maintained by the Royal Kennel Club (for example, "German Shepherd Dog" instead of "Deutscher Schäferhund"). Do not literally translate foreign names if an established English cynological name exists.
    - If there are two or more commonly accepted names, show both separated by a "/" (e.g., "Lowchen / Little Lion Dog").
    Ensure that the list of breeds per group is as extensive and complete as possible.""",
    "DE": """Erstellen Sie eine umfassende Übersicht der Hunderassen pro offizieller FCI-Rassegruppe (1 bis 10), basierend auf den Rassen aus der Datenbank des deutschen VDH (Verband für das Deutsche Hundewesen).
    Für die Namen der FCI-Gruppen und der Hunderassen:
    - Verwenden Sie die offiziellen und in der Praxis gebräuchlichen kynologischen Bezeichnungen im Deutschen.
    - WICHTIG: Nutzen Sie die spezifischen deutschen Rassennamen, wie sie vom VDH geführt werden (zum Beispiel „Deutscher Schäferhund“ anstelle von „German Shepherd Dog“). Übersetzen Sie ausländische Namen nicht wortwörtlich, wenn eine etablierte deutsche kynologische Bezeichnung existiert.
    - Wenn es zwei oder mehr etablierte Namen gibt, zeigen Sie beide durch ein „/“ getrennt an (z. B. „Großer Schweizer Sennenhund / Großer Schweizer“).
    Sorgen Sie dafür, dass die Liste der Rassen pro Gruppe so umfassend und vollständig wie möglich ist.""",
    "FR": """Générez un aperçu complet des races de chiens par groupe de races officiel de la FCI (1 à 10), basé sur les races de la base de données de la SCC (Société Centrale Canine) française.
    Pour les noms des groupes FCI et des races de chiens :
    - Utilisez les dénominations cynologiques officielles et courantes en français.
    - IMPORTANT : Utilisez les noms de races spécifiques en français tels qu'ils sont définis par la Société Centrale Canine (par exemple, « Berger Allemand » au lieu de « Deutscher Schäferhund », ou « Chien d'eau romagnol » au lieu de « Lagotto Romagnolo »). Ne traduisez pas littéralement les noms étrangers s'il existe un nom cynologique français bien établi.
    - S'il existe deux noms ou plus couramment admis, affichez les deux séparés par un « / » (par exemple, « Épagneul Nain Continental / Papillon » ou « Chien de Terre-Neuve / Terre-Neuve »).
    Veillez à ce que la liste des races par groupe soit la plus exhaustive et complète possible.""",
}

DATA_PROMPT = """
Genereer een uitgebreid overzicht van hondenrassen per officiële FCI-rasgroep (1 tot en met 10), 
gebaseerd op de rassen uit de database van het Nederlandse LICG. 

Voor de namen van de FCI-groepen en de hondenrassen:
- Hanteer de officiële en in de praktijk gangbare kynologische benamingen in het %language%. 
- BELANGRIJK voor het Nederlands (%language% = "Nederlands" / "nl"): Gebruik de specifieke Nederlandse rasnamen zoals gehanteerd door de Nederlandse Raad van Beheer en het LICG (bijvoorbeeld "Friese Stabij" of "Stabijhoun" in plaats van de internationale FCI-naam "Stabyhoun", en "Duitse Herdershond" in plaats van "Deutscher Schäferhund"). Vertaal buitenlandse namen niet letterlijk als er een ingeburgerde Nederlandse kynologische naam bestaat.

Zorg dat de lijst met rassen per groep zo uitgebreid en compleet mogelijk is.
"""
OUTPUT_DIRECTORY = os.getenv("FCI_OUTPUT_FOLDER", "./wpforms_dogbreed_fill/data")
