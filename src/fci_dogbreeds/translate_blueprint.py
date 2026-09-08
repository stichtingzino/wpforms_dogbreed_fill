# src/fci_dogbreeds/cli.py
"""
Click-based Command Line Interface (CLI) engine driving deterministic pipelines.

Autonomously branches execution paths between direct Pandas repository conversion
and live HTML token scraping based on target country support vectors.
"""

import logging
import sys
import click

from fci_dogbreeds.config import SUPPORTED_LANGUAGES, FCI_SOURCES, COUNTRY_AUTH_URLS, LOGLEVEL
from fci_dogbreeds.common.fci_functions import (
    convert_static_fci_csv,
    extract_national_kennel_club_registry,
)

logger = logging.getLogger(__name__)

try:
    log_level = getattr(logging, LOGLEVEL)
    logger.setLevel(log_level)
except AttributeError:
    logger.error(
        "Invalid log level: %s, current level: %s remains active.",
        LOGLEVEL,
        logging.getLevelName(logger.getEffectiveLevel())
    )


@click.command()
@click.option(
    "--lang",
    type=click.Choice(list(SUPPORTED_LANGUAGES.keys()), case_sensitive=False),
    default="nl",
    help="Select the target language code execution path.",
)
def cli(lang: str) -> None:
    """Deterministic FCI Dog Breed Database Engineering Framework."""
    selected_lang = lang.lower()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger.info(
        "🚀 Initializing Pipeline. Target language matrix: %s", selected_lang.upper()
    )

    # OPTIE 1: De taal heeft een live web-portal gedefinieerd (Scraper Track)
    if selected_lang in COUNTRY_AUTH_URLS:
        logger.info(
            "🌐 Route Verified: [NET-SCRAPE TRACK]. Extracting authority portal..."
        )
        try:
            extract_national_kennel_club_registry(lang=selected_lang)
            logger.info("🎉 Authoritative live database successfully synchronized!")
        except (ValueError, IOError) as err:
            logger.critical("Scraper pipeline execution failure: %s", err)
            sys.exit(1)

    # OPTIE 2: De taal heeft een statische CSV bron gedefinieerd (Convert Track)
    elif selected_lang in FCI_SOURCES:
        logger.info(
            "⚡ Route Verified: [STATIC REPO CONVERT]. Downloading FCI CSV source..."
        )
        try:
            convert_static_fci_csv(lang=selected_lang)
            logger.info("🎉 Static repository conversion completed successfully!")
        except (ValueError, KeyError, IOError) as err:
            logger.critical("Static transformation block failure: %s", err)
            sys.exit(1)

    else:
        logger.critical(
            "Requested language vector '%s' holds no registered data track.",
            selected_lang.upper(),
        )
        sys.exit(1)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
