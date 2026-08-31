"""Main process file"""

import csv
import json
import os
import logging
import time
from google.genai import errors
from fci_dogbreeds.google_functions.functions import get_data_from_gemini
from fci_dogbreeds.config import OUTPUT_DIRECTORY, PROMPT_LANGUAGES, TARGET_FILENAME_PREFIX

logger = logging.getLogger(__name__)


def _export_data(base_name: str, live_data: dict) -> None:
    """Export data to CSV and JSON files."""
    # --- CSV EXPORT ---
    csv_path = f"{base_name}.csv"
    with open(csv_path, mode="w", encoding="utf-8", newline="") as csv_fh:
        csv_writer = csv.writer(
            csv_fh, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        csv_writer.writerow(["FCI_Group", "Group_Name", "Breeds"])

        for group in live_data["groups"]:
            breeds_str = ";".join(group["breeds"])
            csv_writer.writerow([group["fci_group"], group["group_name"], breeds_str])

    # --- JSON EXPORT ---
    json_path = f"{base_name}.json"
    with open(json_path, mode="w", encoding="utf-8") as json_fh:
        json.dump(live_data["groups"], json_fh, ensure_ascii=False, indent=2)

    print(f"-> Successfully saved: {csv_path} and {json_path}")


# 3. Main program for generating the files
def get_dogbreeds():
    """Define the languages, display name for the prompt, and desired filename suffix"""

    # Create the export directory
    output_dir = OUTPUT_DIRECTORY
    os.makedirs(output_dir, exist_ok=True)

    lang_keys = list(PROMPT_LANGUAGES.keys())
    total_langs = len(lang_keys)

    # Loop through the configured languages and populate 'dog_data' live via the API
    for idx, lang_code in enumerate(lang_keys):
        logger.info("Fetching live data for %s", lang_code)

        # Fetch the live data via the Gemini API query with retry logic
        live_data = None
        for attempt in range(3):
            try:
                live_data = get_data_from_gemini(lang_code)
                break  # Success, exit retry loop
            except (errors.ServerError, errors.ClientError) as err:
                # Retry on 503 (Service Unavailable) and 429 (Rate Limit)
                if err.code in (503, 429):
                    delay = 2 * (2 ** attempt)  # Exponential backoff: 2s, 4s, 8s
                    logger.warning(
                        "API error %s (attempt %d/3). Retrying in %.1f seconds...",
                        err.code,
                        attempt + 1,
                        delay,
                    )
                    time.sleep(delay)
                else:
                    raise err

        # If all retries failed, skip to the next language
        if live_data is None:
            logger.error(
                "Failed to fetch data for %s after 3 retries. Skipping...",
                lang_code,
            )
            continue

        # Add small delay between language requests to avoid rate limiting
        if idx < total_langs - 1:
            time.sleep(1)

        base_name = os.path.join(output_dir, TARGET_FILENAME_PREFIX + lang_code.lower())
        _export_data(base_name, live_data)

    print(f"\nDone! All generated files are in the directory: '{output_dir}/'")


if __name__ == "__main__":
    get_dogbreeds()
