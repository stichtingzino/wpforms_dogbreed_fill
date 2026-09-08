"""
Configuration module for the FCI dog breed data extraction and translation pipeline.

Defines global model names, dynamic file paths loaded via environment variables.
"""

# src/fci_dogbreeds/config.py
import os
import logging

# from typing import List
# from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

LOGLEVEL = os.environ.get("FCI_LOGLEVEL", "DEBUG")

FCI_SOURCES = {
    "en": "https://github.com/paiv/fci-breeds/raw/refs/heads/main/fci-breeds.csv",
    "fr": "https://github.com/paiv/fci-breeds/raw/refs/heads/main/fci-breeds-fr.csv",
    "de": "https://github.com/paiv/fci-breeds/raw/refs/heads/main/fci-breeds-de.csv",
    "es": "https://github.com/paiv/fci-breeds/raw/refs/heads/main/fci-breeds-es.csv",
    "pl": "https://github.com/paiv/fci-breeds/raw/refs/heads/main/fci-breeds-pl.csv",
    "uk": "https://github.com/paiv/fci-breeds/raw/refs/heads/main/fci-breeds-uk.csv",
}
COUNTRY_AUTH_URLS = {
    "nl": "https://www.houdenvanhonden.nl/hondenrassen/alle-rassen/"
}

COUNTRY_GROUP_URLS = {
    "nl": "https://www.houdenvanhonden.nl/hondenrassen/"
}
# COHERENTE ONDERSTEUNDE TALEN MATRIX
SUPPORTED_LANGUAGES = {
    "en": "English",
    "de": "Deutsch",
    "fr": "Français",
    "nl": "Nederlands",
}

# Splitsing op basis van de aanwezige bronnen
STATIC_LANGUAGES = list(FCI_SOURCES.keys())
AI_LANGUAGES = [lang for lang in SUPPORTED_LANGUAGES if lang not in STATIC_LANGUAGES]

# DYNAMISCHE FILENAMES VIA ENVIRONMENT EN CENTRAL CONFIG
FCI_CSV_INPUT_PATH = os.environ.get(
    "FCI_CSV_INPUT_PATH", FCI_SOURCES.get("en", "fci-breeds.csv")
)
FCI_JSON_OUTPUT_TEMPLATE = os.environ.get(
    "FCI_JSON_OUTPUT_TEMPLATE", "fci_dataset_{lang}.json"
)

FCI_NOMENCLATURE_URL_TEMPLATE = "https://fci.be/{lang}/nomenclature/"

ALIAS_LIST_NL = {
    "Stabyhoun": "Friese Stabij / Stabijhoun",
    "Stabijhoun": "Friese Stabij / Stabijhoun",
}
ALIAS_LIST_DE = {}
ALIAS_LIST_FR = {}
ALIAS_LIST_ES = {}
ALIAS_LIST_PL = {}
ALIAS_LIST_UK = {}
ALIAS_LIST_EL = {}
ALIAS_LIST_IT = {}
ALIAS_LIST_PT = {}
