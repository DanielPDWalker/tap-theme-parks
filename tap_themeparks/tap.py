"""themeparks tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_themeparks import streams


class Tapthemeparks(Tap):
    """themeparks tap class."""

    name = "tap-themeparks"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList().to_dict()

    def discover_streams(self) -> list[streams.themeparksStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.DestinationsStream(self),
            streams.entityDetailsStream(self),
        ]


if __name__ == "__main__":
    Tapthemeparks.cli()
