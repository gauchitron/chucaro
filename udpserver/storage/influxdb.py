from influxdb_client import InfluxDBClient


def get_influxdb_client():
    """
    Returns an InfluxDB client.

    Configuration is done using environment vars:
        INFLUXDB_V2_URL - the url to connect to InfluxDB
        INFLUXDB_V2_ORG - default destination organization for writes and queries
        INFLUXDB_V2_TOKEN - the token to use for the authorization
        INFLUXDB_V2_TIMEOUT - socket timeout in ms (default value is 10000)
    """
    return InfluxDBClient.from_env_properties()
