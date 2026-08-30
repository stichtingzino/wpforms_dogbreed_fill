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
DATA_PROMPT = """
Genereer een uitgebreid overzicht van hondenrassen per officiële FCI-rasgroep (1 tot en met 10), 
gebaseerd op de rassen uit de database van het Nederlandse LICG. 

Voor de namen van de FCI-groepen en de hondenrassen:
- Hanteer de officiële en in de praktijk gangbare kynologische benamingen in het %language%. 
- BELANGRIJK voor het Nederlands (%language% = "Nederlands" / "nl"): Gebruik de specifieke Nederlandse rasnamen zoals gehanteerd door de Nederlandse Raad van Beheer en het LICG (bijvoorbeeld "Friese Stabij" of "Stabijhoun" in plaats van de internationale FCI-naam "Stabyhoun", en "Duitse Herdershond" in plaats van "Deutscher Schäferhund"). Vertaal buitenlandse namen niet letterlijk als er een ingeburgerde Nederlandse kynologische naam bestaat.

Zorg dat de lijst met rassen per groep zo uitgebreid en compleet mogelijk is.
"""
OUTPUT_DIRECTORY = os.getenv("FCI_OUTPUT_FOLDER", "./wpforms_dogbreed_fill/data")
