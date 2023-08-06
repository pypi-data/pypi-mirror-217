"""InfluxDB Sink connector configuration.

See https://docs.lenses.io/connectors/sink/influx.html.
"""

__all__ = ["InfluxConfig"]

from dataclasses import dataclass
from typing import Set

from kafkaconnect.config import ConnectorConfig


@dataclass
class InfluxConfig(ConnectorConfig):
    """InfluxDB connector configuration."""

    name: str
    """Name of the connector."""

    connect_influx_url: str
    """InfluxDB connection URL."""

    connect_influx_db: str
    """InfluxDB database name."""

    tasks_max: int
    """Number of Kafka Connect tasks."""

    connect_influx_username: str
    """InfluxDB username."""

    connect_influx_password: str
    """InfluxDB password."""

    connect_influx_error_policy: str
    """Connector error policy configuration."""

    connect_influx_max_retries: str
    """Connector error policy configuration."""

    connect_influx_retry_interval: str
    """Connector error policy configuration."""

    connect_progress_enabled: bool
    """Enables the output for how many records have been processed."""

    tags: str
    """Fields to be used as tags."""

    remove_prefix: str
    """Prefix to remove from topic name to use as measurement name."""

    # Attributes with defaults are not configurable via click
    topics: str = ""
    """Comma separated list of Kafka topics to read from."""

    connect_influx_kcql: str = ""
    """KCQL queries to extract fields from topics. Computed.

    We assume that a topic has a flat structure so that `SELECT * FROM` will
    retrieve all topic fields. This is configuration is derived from the list
    of topics and from the timestamp to use as the InfluxDB time.
    """

    connector_class: str = (
        "com.datamountaineer.streamreactor.connect.influx.InfluxSinkConnector"
    )
    """Stream reactor InfluxDB Sink connector class."""

    def update_config(self, topics: Set[str], timestamp: str = "") -> None:
        """Update connector config.

        Parameters
        ----------
        topics : `Set`
            List of kafka topics.

        timestamp : `str`
            Timestamp used as influxDB time.
        """
        sorted_topics = sorted(topics)
        self.topics = ",".join(sorted_topics)

        tags = ""
        if self.tags:
            tags = f" WITHTAG({self.tags})"

        queries = []
        for topic in sorted_topics:
            if self.remove_prefix:
                measurement = topic[len(self.remove_prefix) :]
            else:
                measurement = topic

            query = (
                f"INSERT INTO {measurement} SELECT * FROM {topic} "
                f"WITHTIMESTAMP {timestamp} TIMESTAMPUNIT=MICROSECONDS{tags}"
            )

            queries.append(query)

        self.connect_influx_kcql = ";".join(queries)
