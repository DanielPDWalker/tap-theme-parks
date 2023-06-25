"""Stream type classes for tap-themeparks."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_themeparks.client import themeparksStream


class DestinationsStream(themeparksStream):
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
        return {"entity_id": record["id"]}


class DestinationDetailsStream(themeparksStream):
    """Define destination details stream"""

    parent_stream_type = DestinationsStream
    name = "destination_detail"
    path = "/entity/{entity_id}"
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


class DestinationChildrenStream(themeparksStream):
    """Define destination children stream"""

    parent_stream_type = DestinationsStream
    name = "destination_children"
    path = "/entity/{entity_id}/children"
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


class LiveDataStream(themeparksStream):
    """Define live data stream"""

    name = "live_data"
    path = "/entity/{live_data_id}/live"
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
