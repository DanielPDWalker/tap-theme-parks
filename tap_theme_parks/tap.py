"""Theme parks tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_theme_parks import streams


class TapThemeParks(Tap):
    """Theme parks tap class."""

    name = "tap-theme-parks"

    config_jsonschema = th.PropertiesList(
        th.Property("live_data_array", th.ArrayType(th.StringType)),
    ).to_dict()

    def discover_streams(self) -> list[streams.ThemeParksStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        selected_streams = [
            streams.DestinationsStream(self),
            streams.DestinationDetailsStream(self),
            streams.DestinationChildrenStream(self),
            streams.ParkDetailsStream(self),
            streams.ParkChildrenStream(self),
        ]

        if self.config.get("live_data_array"):
            selected_streams.append(streams.LiveDataStream(self))

        return selected_streams


if __name__ == "__main__":
    TapThemeParks.cli()
