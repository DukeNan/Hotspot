from influxdb import InfluxDBClient
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

client = InfluxDBClient(
            host=settings['INFLUX_DB_HOST'],
            port=settings['INFLUX_DB_PORT'],
            username=settings['INFLUX_DB_USERNAME'],
            password=settings['INFLUX_DB_PASSWORD'],
            database=settings['INFLUX_DB_NAME']
        )


