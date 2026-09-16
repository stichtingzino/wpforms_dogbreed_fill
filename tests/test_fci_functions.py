"""Test fci functions"""

# tests/test_fci_functions.py

from unittest import mock
from urllib.error import URLError
from fci_dogbreeds.common.fci_functions import _scrape_rvb_groups_metadata


# Mocking the ssl module to avoid actual SSL context creation and verification.
@mock.patch("ssl.create_default_context")
def test_scrape_rvb_groups_metadata_success(_mock_ssl):
    """test scrape"""
    # We gebruiken MagicMock zodat de mock zich als een contextmanager
    # (__enter__ / __exit__) kan gedragen
    mock_response = mock.MagicMock()
    html_content = """
        <h2>FCI groep 1 - Herdershonden</h2>
        <p>Een beschrijving van de herdershonden.</p>
        <div class="other-content">Andere inhoud die we negeren.</div>
        <h2>FCI groep 3 - Terriers</h2>
    """

    mock_response.read.return_value = html_content.encode("utf-8")

    # Zorg ervoor dat wanneer urlopen als contextmanager wordt gebruikt, hij
    # de mock_response teruggeeft
    mock_urlopen_ctx = mock.MagicMock()
    mock_urlopen_ctx.__enter__.return_value = mock_response

    with mock.patch("urllib.request.urlopen", return_value=mock_urlopen_ctx):
        result = _scrape_rvb_groups_metadata("http://example.com")

        assert isinstance(result, dict)
        expected_result = {1: "Herdershonden", 3: "Terriers"}

        # Inspringing hersteld naar pure spaties
        for key, val in expected_result.items():
            assert result[key] == val


@mock.patch("ssl.create_default_context")
def test_scrape_rvb_groups_metadata_network_error(_mock_ssl):
    """test scrape group"""
    with mock.patch("urllib.request.urlopen", side_effect=URLError("Network error")):
        result = _scrape_rvb_groups_metadata("http://example.com")
        assert isinstance(result, dict)
        # Check if the function returns an empty dictionary when network request fails.
        assert len(result) == 0


@mock.patch("ssl.create_default_context")
def test_scrape_rvb_groups_metadata_os_error(_mock_ssl):
    """test test error"""
    with mock.patch("urllib.request.urlopen", side_effect=OSError("OS error")):
        result = _scrape_rvb_groups_metadata("http://example.com")
        assert isinstance(result, dict)
        # Check if the function returns an empty dictionary when OSError occurs.
        assert len(result) == 0
