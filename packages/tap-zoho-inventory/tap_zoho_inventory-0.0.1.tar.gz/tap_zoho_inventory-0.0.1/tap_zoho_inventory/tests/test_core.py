"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_standard_tap_tests

from tap_zoho_inventory.tap import TapZohoInventory

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "auth_token": "my_auth_token",
    "project_ids": ["my_project_id"],
    "client_id": "my_client_id",
    "client_secret": "my_client_secret",
    "api_url": "https://api.mysample.com",
    "refresh_token": "my_refresh_token",
    "expires_in": 3600,
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapZohoInventory, config=SAMPLE_CONFIG)
    for test in tests:
        test()
