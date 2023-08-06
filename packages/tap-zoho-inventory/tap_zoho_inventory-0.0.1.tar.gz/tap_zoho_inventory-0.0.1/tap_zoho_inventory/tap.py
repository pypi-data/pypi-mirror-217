"""zoho-inventory tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_zoho_inventory.streams import (
    ItemsStream,
)

# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    ItemsStream,
]


class TapZohoInventory(Tap):
    """zoho-inventory tap class."""

    name = "tap-zoho-inventory"

    def __init__(
        self,
        config=".env",
        catalog=None,
        state=None,
        parse_env_config=True,
        validate_config=True,
    ) -> None:
        self.config_file = config
        super().__init__(config, catalog, state, parse_env_config, validate_config)

    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "refresh_token",
            th.StringType,
            required=True,
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
        ),
        th.Property(
            "organization_id",
            th.StringType,
        ),
        th.Property(
            "redirect_uri",
            th.StringType,
            default="",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
