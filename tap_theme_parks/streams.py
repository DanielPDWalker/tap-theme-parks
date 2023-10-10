"""Stream type classes for tap-theme-parks."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_theme_parks.client import ThemeParksStream


class DestinationsStream(ThemeParksStream):
    """Define destinations stream"""

    name = "destinations"
    path = "/destinations"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.destinations[*]"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property(
            "parks",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType), th.Property("name", th.StringType)
                )
            ),
        ),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "destination_id": record["id"],
            "park_ids": [x["id"] for x in record["parks"]],
        }


class ParkDetailsStream(ThemeParksStream):
    """Define park details stream"""

    parent_stream_type = DestinationsStream
    name = "park_detail"
    path_template = "/entity/{park_id}"
    primary_keys = ["id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property(
            "location",
            th.ObjectType(
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
                th.Property("pointOfInterest", th.ArrayType(th.StringType)),
            ),
        ),
        th.Property("parentId", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property("entityType", th.StringType),
        th.Property("destinationId", th.StringType),
        th.Property("externalId", th.StringType),
    ).to_dict()

    def request_records(self, context: dict | None) -> Iterable[dict]:
        for id in context["park_ids"]:
            self.path = self.path_template.format(park_id=id)
            yield from super().request_records(context)

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {"park_id": record["id"]}


class ParkChildrenStream(ThemeParksStream):
    """Define park children stream"""

    parent_stream_type = ParkDetailsStream
    name = "park_children"
    path = "/entity/{park_id}/children"
    primary_keys = ["id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("entityType", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property(
            "children",
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("entityType", th.StringType),
                th.Property("slug", th.StringType),
                th.Property("externalId", th.StringType),
            ),
        ),
    ).to_dict()


class DestinationDetailsStream(ThemeParksStream):
    """Define destination details stream"""

    parent_stream_type = DestinationsStream
    name = "destination_detail"
    path = "/entity/{destination_id}"
    primary_keys = ["id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("slug", th.StringType),
        th.Property(
            "location",
            th.ObjectType(
                th.Property("latitude", th.NumberType),
                th.Property("longitude", th.NumberType),
                th.Property("pointOfInterest", th.ArrayType(th.StringType)),
            ),
        ),
        th.Property("parentId", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property("entityType", th.StringType),
        th.Property("destinationId", th.StringType),
        th.Property("externalId", th.StringType),
    ).to_dict()


class DestinationChildrenStream(ThemeParksStream):
    """Define destination children stream"""

    parent_stream_type = DestinationsStream
    name = "destination_children"
    path = "/entity/{destination_id}/children"
    primary_keys = ["id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("entityType", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property(
            "children",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("entityType", th.StringType),
                    th.Property("slug", th.StringType),
                    th.Property("externalId", th.StringType),
                )
            ),
        ),
    ).to_dict()


class LiveDataStream(ThemeParksStream):
    """Define live data stream"""

    name = "live_data"
    path_template = "/entity/{live_data_id}/live"
    primary_keys = ["id"]
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("entityType", th.StringType),
        th.Property("timezone", th.StringType),
        th.Property(
            "liveData",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.StringType),
                    th.Property("name", th.StringType),
                    th.Property("entityType", th.StringType),
                    th.Property("status", th.StringType),
                    th.Property("lastUpdated", th.DateTimeType),
                    th.Property(
                        "queue",
                        th.ObjectType(
                            th.Property(
                                "STANDBY",
                                th.ObjectType(
                                    th.Property("waitTime", th.NumberType),
                                ),
                            ),
                            th.Property(
                                "SINGLE_RIDER",
                                th.ObjectType(
                                    th.Property("waitTime", th.NumberType),
                                ),
                            ),
                            th.Property(
                                "RETURN_TIME",
                                th.ObjectType(
                                    th.Property("state", th.StringType),
                                    th.Property("returnStart", th.DateTimeType),
                                    th.Property("returnEnd", th.DateTimeType),
                                ),
                            ),
                            th.Property(
                                "PAID_RETURN_TIME",
                                th.ObjectType(
                                    th.Property("allocationStatus", th.StringType),
                                    th.Property("currentGroupStart", th.DateTimeType),
                                    th.Property("currentGroupEnd", th.DateTimeType),
                                    th.Property("nextAllocationTime", th.DateTimeType),
                                    th.Property("estimatedWait", th.NumberType),
                                ),
                            ),
                        ),
                    ),
                    th.Property(
                        "showTimes",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("type", th.StringType),
                                th.Property("startTime", th.DateTimeType),
                                th.Property("endTime", th.DateTimeType),
                            )
                        ),
                    ),
                    th.Property(
                        "operatingHours",
                        th.ArrayType(
                            th.ObjectType(
                                th.Property("type", th.StringType),
                                th.Property("startTime", th.DateTimeType),
                                th.Property("endTime", th.DateTimeType),
                            )
                        ),
                    ),
                ),
            ),
        ),
    ).to_dict()

    def request_records(self, context: dict | None) -> Iterable[dict]:
        for id in self.config.get("live_data_array", []):
            self.path = self.path_template.format(live_data_id=id)
            yield from super().request_records(context)
