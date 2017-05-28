import sqlalchemy
from datetime import date, datetime
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

WEATHER_READING_TEMP = 'temp'
WEATHER_READING_HUMID = 'humid'
WEATHER_READING_RAINFALL = 'rain'
WEATHER_READING_PRESSURE = 'pressure'

# Static agent table - id is weatherstation id
# data elements are mac
AGENTS = {
    'WSTATION-0' : {
    'mac_addr': '00:11:22:33:44:55',
    'last_update': 0,
    'sw_version': "0.0.1"}
}

agent_parser = reqparse.RequestParser()
agent_parser.add_argument('mac_addr',
    help='MAC address of the weather station')

# Static readings table - fields are
READINGS = {
    '0' : {
    'weatherstation-id' : 'WSTATION-0',
    'reading_type' : 'temp',
    'reading_value' : 23.5,
    'timestamp' : 0}
}

# Parser for weather readings
reading_parser = reqparse.RequestParser()
reading_parser.add_argument('weatherstation-id',
    help='ID of the weatherstation that generating this reading',
    required=True)
reading_parser.add_argument('reading_type',
    help='The type of reading this is - options are temp, humid, rain, pressure',
    required=True)
reading_parser.add_argument('reading_value', type=float,
    help='The value of the reading being provided - floating point number',
    required=True)
reading_parser.add_argument('timestamp', type=int,
    help='The timestamp that the reading was taken - Posix timestamp')


def error_no_reading(reading_id):
    if reading_id not in READINGS:
        abort(404, message="Reading {} does not exist".format(reading_id))

# The WeatherReading class represents a single datapoint
class WeatherReading(Resource):
    def get(self, reading_id):
        error_no_reading(reading_id)
        return READINGS[reading_id]

class WeatherReadingList(Resource):
    def get(self):
        return READINGS

api.add_resource(WeatherReading, '/readings/<reading_id>')
api.add_resource(WeatherReadingList, '/readings')

if __name__ =='__main__':
    app.run(debug=True)
