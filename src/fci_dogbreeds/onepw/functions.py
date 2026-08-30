"""Onepassword functions"""

import logging
import os
from typing import Optional

from onepassword.client import Client, DesktopAuth

logger = logging.getLogger(__name__)

TEST_SECRET = os.getenv("GOOGLE_API_KEY", None)

class OnePasswordError(Exception):
    """Base exception for all custom 1Password SDK wrappers."""

class DesktopAuthDeniedError(OnePasswordError):
    """Raised when the user explicitly denies or cancels the biometric prompt."""

class DesktopAppClosedError(OnePasswordError):
    """Raised when the 1Password desktop app is not running or integration is disabled."""

class AccountNotFoundError(OnePasswordError):
    """Raised when the requested account configuration is missing from the desktop app."""

async def get_1pw_entry(entry_id: str | None) -> Optional[str]:
    """Retrieve an entry from 1Password."""
    token = os.getenv("OP_SERVICE_ACCOUNT_TOKEN", None)
    if token is None:
        logger.info("Using desktop authentication for 1Password.")
        client = await _get_1pw_entry_desktop()
        if not client:
            logger.error(
                "Desktop authentication failed. Please set the "
                "'OP_SERVICE_ACCOUNT_TOKEN' environment variable."
            )
            return None
    else:
        logger.info("Using headless authentication for 1Password.")
        # Connects to 1Password. Fill in your own integration name and version.
        client = await Client.authenticate(
            auth=token,
            integration_name="My 1Password Integration",
            integration_version="v1.0.0",
        )

    # Retrieves a secret from 1Password. Takes a secret reference as input and
    # returns the secret to which it points.
    if entry_id is None:
        entry_id = f"{TEST_SECRET}"  # This should be the path to your 1Password secret

    secret_uri = f"{entry_id}"

    logger.debug(
        "Fetching secret from 1Password, entry_id: %s, secret_uri: %s",
        entry_id,
        secret_uri,
    )

    return await client.secrets.resolve(secret_uri)


async def _get_1pw_entry_desktop() -> Client | None:
    """Attempt to authenticate with 1Password using desktop credentials.

    Returns:
        The JSON string of the 1Password service account, or None if authentication fails.
    """
    account_name = os.getenv("OP_ACCOUNT_NAME")
    if not account_name:
        logger.error(
            "The environment variable 'OP_ACCOUNT_NAME' is not set. "
            "Please set it to your 1Password account name."
        )
        return None

    try:
        # Authenticate using DesktopAuth
        auth = DesktopAuth(account_name=account_name)
        client = await Client.authenticate(
            auth=auth,
            integration_name="My 1Password Integration",
            integration_version="v1.0.0",
        )

        # Retrieve the entry using the op:// URI
        # secret_uri =
        # f"op://{os.getenv('OP_SERVICE_ACCOUNT_VAULT')}/{os.getenv('OP_SERVICE_ACCOUNT_ITEM')}"
        # logger.debug("Fetching secret from 1Password, secret_uri: %s", secret_uri)

        return client
    except RuntimeError as err:
        error_msg = str(err).lower()

        # Translate the string patterns into your custom exceptions
        if "authorization denied" in error_msg or "user canceled" in error_msg:
            raise DesktopAuthDeniedError(
                "User rejected or timed out the biometric prompt."
            ) from err

        if "account not found" in error_msg:
            raise AccountNotFoundError(
                f"Account '{account_name}' is not configured in the app."
            ) from err

        if "app not running" in error_msg or "connection refused" in error_msg:
            raise DesktopAppClosedError("The 1Password Desktop App is completely closed.") from err

        # If it's an unrelated RuntimeError, bubble it up naturally without swallowing it
        raise err

    except (FileNotFoundError, ConnectionError) as sys_err:
        # Catch system-level IPC pipe issues and map them cleanly too
        raise DesktopAppClosedError("Local system IPC pipe failed. App is closed.") from sys_err
