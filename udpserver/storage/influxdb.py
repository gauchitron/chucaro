from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS


def get_influxdb_client():
    """
    Returns an InfluxDB client.

    Configuration is done using environment vars:
        INFLUXDB_V2_URL - the url to connect to InfluxDB
        INFLUXDB_V2_ORG - default destination organization for writes and queries
        INFLUXDB_V2_TOKEN - the token to use for the authorization
        INFLUXDB_V2_TIMEOUT - socket timeout in ms (default value is 10000)
    """
    client = InfluxDBClient.from_env_properties()
    write_api = client.write_api(write_options=ASYNCHRONOUS)
    return write_api
