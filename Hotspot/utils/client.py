from influxdb import InfluxDBClient
from Hotspot.settings import (INFLUX_DB_HOST,
                              INFLUX_DB_NAME,
                              INFLUX_DB_PORT,
                              INFLUX_DB_PASSWORD,
                              INFLUX_DB_USERNAME)

client = InfluxDBClient(
    host=INFLUX_DB_HOST,
    port=INFLUX_DB_PORT,
    username=INFLUX_DB_USERNAME,
    password=INFLUX_DB_PASSWORD,
    database=INFLUX_DB_NAME
)


print(client.get_list_measurements())


print(client.query('''select * from "weibo" where "title_md5" = '65441338db4a8f3200ed889a1f6483ca' '''))