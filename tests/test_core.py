"""Tests standard tap features using the built-in SDK tests library."""

import unittest

from singer_sdk.testing import get_tap_test_class

from tap_theme_parks.tap import TapThemeParks

DEFAULT_CONFIG = {}

SAMPLE_CONFIG = {"live_data_array": ["1", "2", "3"]}


# Run standard built-in tap tests from the SDK:
TestTapThemeParks = get_tap_test_class(
    tap_class=TapThemeParks,
    config=DEFAULT_CONFIG,
)


class TestEnabledStreams(unittest.TestCase):
    """Test class for enabled streams"""

    def test_default_streams(self):
        catalog = TapThemeParks().discover_streams()

        self.assertEqual(len(catalog), 3, "Expected 3 streams from catalog by default")

    def test_streams_with_live_data_array(self):
        catalog = TapThemeParks(config=SAMPLE_CONFIG).discover_streams()

        self.assertEqual(
            len(catalog),
            5,
            "Expected 5 streams from catalog with the live_data_array setting provided",
        )
