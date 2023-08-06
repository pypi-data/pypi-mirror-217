"""Tests for the command-line interface."""

from click.testing import CliRunner

from kafkaconnect.cli import main


def test_help() -> None:
    """Test help for main commands and subcommands."""
    runner = CliRunner()

    result = runner.invoke(main, ["-h"])
    assert result.exit_code == 0
    assert "Commands:" in result.output

    result = runner.invoke(main, ["help"])
    assert result.exit_code == 0
    assert "Commands:" in result.output

    result = runner.invoke(main, ["help", "list"])
    assert result.exit_code == 0
    assert "Commands:" not in result.output
    assert "Options:" in result.output

    result = runner.invoke(main, ["help", "unknown-command"])
    assert result.exit_code != 0
    assert "Unknown help topic unknown-command" in result.output


def test_failed_connection_message() -> None:
    """Fails with a specific message if Connect API URL is invalid.

    Also test passing context with the Connect API URL.
    """
    runner = CliRunner()
    # test failed connection with kafka connect
    result = runner.invoke(
        main, ["--connect", "http://invalid-connect-url", "list"]
    )
    assert result.exit_code == 0
    assert (
        "Failed to establish connection with the Connect "
        "API http://invalid-connect-url.\n" in result.output
    )


def test_create_influxdb_sink() -> None:
    """Test create influxdb-sink connector with default configuration."""
    runner = CliRunner()
    result = runner.invoke(
        main, ["create", "influxdb-sink", "--dry-run", "t1"]
    )
    assert result.exit_code == 0
    # This query is built by InfluxConfig.update_influx_kcql()
    assert (
        '"connect.influx.kcql": '
        '"INSERT INTO t1 SELECT * FROM t1 WITHTIMESTAMP sys_time() '
        'TIMESTAMPUNIT=MICROSECONDS"' in result.output
    )
    # Topics are added by ConnectConfig.update_config()
    assert '"topics": "t1"' in result.output


def test_influxdb_tags() -> None:
    """Test influxdb-sink with tags support."""
    runner = CliRunner()
    result = runner.invoke(
        main, ["create", "influxdb-sink", "--dry-run", "--tags", "test", "t1"]
    )
    assert result.exit_code == 0
    # Add WITHTAG clause to the influx kcql query when using tags
    assert (
        '"connect.influx.kcql": '
        '"INSERT INTO t1 SELECT * FROM t1 WITHTIMESTAMP sys_time() '
        'TIMESTAMPUNIT=MICROSECONDS WITHTAG(test)"' in result.output
    )


def test_remove_prefix() -> None:
    """Test influxdb-sink with remove_prefix support."""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "create",
            "influxdb-sink",
            "--dry-run",
            "--remove-prefix",
            "abc.",
            "abc.t1",
        ],
    )
    assert result.exit_code == 0
    # Add WITHTAG clause to the influx kcql query when using tags
    assert (
        '"connect.influx.kcql": '
        '"INSERT INTO t1 SELECT * FROM abc.t1 WITHTIMESTAMP sys_time() '
        'TIMESTAMPUNIT=MICROSECONDS"' in result.output
    )


def test_password_from_env() -> None:
    """Test getting the influxdb password from the environment."""
    env = {"KAFKA_CONNECT_INFLUXDB_PASSWORD": "envpasswd"}
    runner = CliRunner()
    result = runner.invoke(
        main, args=["create", "influxdb-sink", "--dry-run", "t1"], env=env
    )
    assert result.exit_code == 0
    assert "envpasswd" in result.output
