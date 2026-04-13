"""Tests standard tap features using the built-in SDK tests library."""

import unittest

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_theme_parks.tap import TapThemeParks

DEFAULT_CONFIG = {}

SAMPLE_CONFIG = {"live_data_array": ["1", "2", "3"]}


# Run standard built-in tap tests from the SDK:
class TestTapThemeParks(
    get_tap_test_class(
        tap_class=TapThemeParks,
        config=DEFAULT_CONFIG,
        suite_config=SuiteConfig(max_records_limit=1),
    )
):
    def test_tap_stream_connections(self) -> None:
        """Test connectivity using only the top-level stream to avoid rate limiting."""
        tap = TapThemeParks(config=DEFAULT_CONFIG)
        tap.run_sync_dry_run(
            dry_run_record_limit=1,
            streams=[tap.streams["destination"]],
        )


class TestEnabledStreams(unittest.TestCase):
    """Test class for enabled streams"""

    def test_default_streams(self):
        catalog = TapThemeParks().discover_streams()

        self.assertEqual(len(catalog), 5, "Expected 5 streams from catalog by default")

    def test_streams_with_live_data_array(self):
        catalog = TapThemeParks(config=SAMPLE_CONFIG).discover_streams()

        self.assertEqual(
            len(catalog),
            6,
            "Expected 6 streams from catalog with the live_data_array setting provided",
        )
