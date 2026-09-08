# src/fci_dogbreeds/common/fci_functions.py
"""
Dynamic data-transformation and web extraction layer compiling dog breeds.

Asynchronously scrapes structural metadata directly from international canine
registries to ensure deterministic conversions without static local maps.
"""

import html
import json
import logging
import re
import ssl
import urllib.request
import urllib.error
from typing import Dict, Any, List
import pandas as pd

from fci_dogbreeds.config import (
    FCI_SOURCES,
    COUNTRY_AUTH_URLS,
    COUNTRY_GROUP_URLS,
    FCI_NOMENCLATURE_URL_TEMPLATE,
    FCI_JSON_OUTPUT_TEMPLATE,
)
import fci_dogbreeds.config as project_config

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def load_fci_dataframe(source_path: str) -> pd.DataFrame:
    """Loads FCI CSV data into a Pandas DataFrame."""
    try:
        return pd.read_csv(source_path)
    except (FileNotFoundError, pd.errors.EmptyDataError, IOError) as err:
        logger.error("Data resource mapping failure on '%s': %s", source_path, err)
        raise


def save_json_matrix(data: Dict[str, Any], output_json_path: str) -> None:
    """Safely writes a structured dictionary to disk as a clean JSON file."""
    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(
            "Successfully synchronized dataset output to: '%s'", output_json_path
        )
    except IOError as io_err:
        logger.error(
            "Critical write failure on target '%s': %s", output_json_path, io_err
        )
        raise


def _scrape_fci_groups_metadata(lang: str) -> Dict[int, str]:
    """Live scraps group numbers and localized names directly from fci.be nomenclature."""
    url = FCI_NOMENCLATURE_URL_TEMPLATE.format(lang=lang.lower())
    logger.info("Fetching dynamic FCI group metadata schema from: '%s'", url)

    req = urllib.request.Request(url, headers=HEADERS)
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, timeout=15, context=context) as response:
            html_content = response.read().decode("utf-8")
    except (urllib.error.URLError, IOError) as net_err:
        logger.error("FCI structural metadata fetch failed: %s", net_err)
        return {}

    metadata_map: Dict[int, str] = {}
    for i in range(10):
        group_num = i + 1
        span_id = f"ContentPlaceHolder1_GroupesRepeater_Label1_{i}"

        pattern = re.compile(
            rf'<span[^>]+id="{span_id}"[^>]*>(?P<gname>[^<]+)<\/span>',
            re.IGNORECASE | re.DOTALL,
        )

        match = pattern.search(html_content)
        if match:
            raw_gname = match.group("gname").strip()
            clean_gname = html.unescape(raw_gname)
            clean_gname = re.sub(r"\s+", " ", clean_gname).strip()
            metadata_map[group_num] = clean_gname

    return metadata_map


# Sluit direct en onafgebroken aan onder Deel 1 in src/fci_dogbreeds/common/fci_functions.py


def _scrape_rvb_groups_metadata(url: str) -> Dict[int, str]:
    """Live scraps Dutch group names directly from the Raad van Beheer overzichtspagina."""
    logger.info("Fetching dynamic Raad van Beheer group metadata from: '%s'", url)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=15, context=context) as response:
            html_content = response.read().decode("utf-8")
    except (urllib.error.URLError, IOError) as net_err:
        logger.error("RvB structural metadata fetch failed: %s", net_err)
        return {}

    # RAAD VAN BEHEER CARD PATTERN: Plukt 'FCI groep 1 - Herdershonden...' live uit de pagina!
    rvb_pattern = re.compile(
        r"<h2[^>]*>FCI\s+groep\s+(?P<gid>\d+)\s*-\s*(?P<gname>[^<]+)<\/h2>",
        re.IGNORECASE,
    )

    metadata_map: Dict[int, str] = {}
    for match in rvb_pattern.finditer(html_content):
        gid = int(match.group("gid"))
        gname = html.unescape(match.group("gname")).strip().title()
        metadata_map[gid] = gname

    return metadata_map


def convert_static_fci_csv(lang: str) -> None:
    """Converts a remote repository FCI CSV (EN/FR/DE) using dynamic cloud metadata."""
    source_url = FCI_SOURCES.get(lang.lower())
    if not source_url:
        raise ValueError(f"No static CSV source URL mapped for language code: '{lang}'")

    fci_groups = _scrape_fci_groups_metadata(lang)
    en_groups_lookup = (
        _scrape_fci_groups_metadata("en") if lang.lower() != "en" else fci_groups
    )

    if not fci_groups:
        raise ValueError(
            "Could not construct live metadata layer for backend layout conversion."
        )

    df = load_fci_dataframe(source_url)
    output_json_path = FCI_JSON_OUTPUT_TEMPLATE.format(lang=lang)
    raw_db: Dict[str, Any] = {}

    try:
        group_cols = [
            c
            for c in df.columns
            if any(g in str(c).lower() for g in ["group", "groupe", "gruppe"])
        ]
        name_cols = [
            c
            for c in df.columns
            if any(n in str(c).lower() for n in ["name", "nom", "bezeichnung"])
        ]

        if not group_cols:
            raise KeyError(
                "Could not automatically detect the FCI group column in CSV headers."
            )

        group_col_name = str(group_cols[0])
        name_col_name = str(name_cols[0]) if name_cols else str(df.columns[0])

        df["group_clean_key"] = df[group_col_name].astype(str).str.strip().str.lower()
        df["name_clean"] = df[name_col_name].astype(str).str.strip().str.title()

        for group_text_name, group_df in df.groupby(group_col_name):
            first_index = group_df.index[0]
            clean_key = str(group_df.at[first_index, "group_clean_key"])

            group_id = None
            for gid, en_name in en_groups_lookup.items():
                if (
                    en_name.lower().strip() in clean_key
                    or clean_key in en_name.lower().strip()
                ):
                    group_id = gid
                    break

            if not group_id:
                for gid, lang_name in fci_groups.items():
                    if (
                        lang_name.lower().strip() in clean_key
                        or clean_key in lang_name.lower().strip()
                    ):
                        group_id = gid
                        break

            if not group_id:
                logger.warning(
                    "Group name '%s' could not be mapped to FCI ID.", group_text_name
                )
                continue

            group_key = f"group_{group_id}"
            breeds_list: List[str] = (
                group_df["name_clean"].drop_duplicates().sort_values().tolist()
            )

            raw_db[group_key] = {
                "fci_group": int(group_id),
                "group_name": fci_groups[group_id],
                "breeds": breeds_list,
            }

        sorted_db = {
            k: raw_db[k]
            for k in sorted(
                raw_db.keys(), key=lambda x: int(str(x).rsplit("_", maxsplit=1)[-1])
            )
        }
        save_json_matrix(sorted_db, output_json_path)

    except (KeyError, IndexError) as err:
        logger.error("CSV Structural layout mismatch: %s", err)
        raise


def extract_national_kennel_club_registry(lang: str) -> None:
    """Streams a live national registry portal and parses breeds into sorted FCI groups."""
    target_lang = lang.lower()

    group_url = COUNTRY_GROUP_URLS.get(target_lang)
    if not group_url:
        raise ValueError(
            f"No official authority group URL registered for language: '{lang}'"
        )

    rvb_groups = _scrape_rvb_groups_metadata(group_url)
    if not rvb_groups:
        raise ValueError(
            "Could not establish dynamic group schema structure layer from remote portal."
        )

    auth_url = COUNTRY_AUTH_URLS.get(target_lang)
    if not auth_url:
        raise ValueError(
            f"No official authority breed URL registered for language: '{lang}'"
        )

    output_json_path = FCI_JSON_OUTPUT_TEMPLATE.format(lang=target_lang)

    req = urllib.request.Request(auth_url, headers=HEADERS)
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=15, context=context) as response:
            html_content = response.read().decode("utf-8")
    except (urllib.error.URLError, IOError) as net_err:
        logger.critical("Network infrastructure breakdown: %s", net_err)
        raise

    # GECORRIGEERDE ALFABETISCHE REGEX PATTERN: Matcht exact de links uit jouw html-dump!
    pattern = re.compile(
        r'<a[^>]+class="large"[^>]+href="(?P<url>[^"]+)"[^>]*>(?P<breed_name>[^<]+)</a>',
        re.IGNORECASE,
    )

    structured_db: Dict[str, Any] = {}
    for gid, gname in rvb_groups.items():
        structured_db[f"group_{gid}"] = {
            "fci_group": gid,
            "group_name": gname,
            "breeds": [],
        }


    alias_dict = getattr(project_config, f"ALIAS_LIST_{target_lang.upper()}", {})

    total_counter = 0
    for match in pattern.finditer(html_content):
        url_path = str(match.group("url")).lower()

        group_match = re.search(r"fci-groep-(\d+)", url_path)
        if group_match:
            group_num = int(group_match.group(1))
            gkey = f"group_{group_num}"

            clean_breed = html.unescape(match.group("breed_name").strip())
            clean_breed = re.sub(r"\s+", " ", clean_breed).strip().title()

            if alias_dict and clean_breed in alias_dict:
                clean_breed = alias_dict[clean_breed]

            if "Terug" in clean_breed or "Fci" in clean_breed or not clean_breed:
                continue

            if (
                gkey in structured_db
                and clean_breed not in structured_db[gkey]["breeds"]
            ):
                structured_db[gkey]["breeds"].append(clean_breed)
                total_counter += 1

    if total_counter > 0:
        # Uw schitterende .values() sortering uitgevoerd!
        for gval in structured_db.values():
            gval["breeds"] = sorted(list(gval["breeds"]))

        sorted_db = {
            k: structured_db[k]
            for k in sorted(
                structured_db.keys(),
                key=lambda x: int(str(x).rsplit("_", maxsplit=1)[-1]),
            )
        }
        save_json_matrix(sorted_db, output_json_path)
    else:
        raise ValueError(
            "Portal extraction failure: 0 breed nodes matched the alphabetical regex matrix."
        )
