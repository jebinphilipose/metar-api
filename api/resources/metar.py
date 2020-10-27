import logging
import re
import requests
from flask import Blueprint, request

metar_resource = Blueprint('metar', __name__)


# Utility for converting wind direction in degrees to cardinal direction
def wind_dir(wind_deg):
    val = int((wind_deg / 22.5) + 0.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


# Define your routes here
@metar_resource.route('/ping')
def ping():
    return {'data': 'pong'}, 200


@metar_resource.route('/info')
def info():
    # Grab the station code
    scode = request.args.get('scode')

    # Return 400 if station code not present in query params
    if scode is None:
        return {'error': 'Station code not provided'}, 400

    scode = scode.upper()

    url = f'https://tgftp.nws.noaa.gov/data/observations/metar/stations/{scode}.TXT'

    try:
        # Make request to National Weather Service
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()

        # Split response into list of lines
        lines = response.text.split("\n")

        # Extract date and time of last observation
        dt_list = lines[0].split(" ")

        # Extract metar string from response
        metar_str = lines[1]

        # Extract temperature information
        temp_match = re.search(r"M?[0-9]{2}\/M?[0-9]{2}", metar_str)
        temp_str = temp_match.group().split(" ")[0].split("/")[0]

        if temp_str[0] == "M":
            celsius = int(temp_str.split("M")[1]) * -1
        else:
            celsius = int(temp_str)

        fahrenheit = round((celsius * 9/5) + 32)

        # Extract wind information
        # Type of wind readings supported -> eg: 32018G29KT, 17004MPS, 00000KT, VRB02KT, 240P99KT, etc.
        wind_match = re.search(r'(\d{3}|VRB)(P?\d{2,3})(?:G(\d+))?(KT|MPS|KMH)(?:.+(\d{3})V(\d{3}))?', metar_str)
        wind_deg, wind_speed, wind_gust, wind_unit, wind_var_from, wind_var_to = wind_match.groups()

        # Parse to integer value
        if wind_deg != "VRB":
            wind_deg = int(wind_deg)
        if wind_speed == "P99" or wind_speed == "P49":
            wind_speed = 99
            wind_unit = "KT"
        else:
            wind_speed = int(wind_speed)
        if wind_gust:
            wind_gust = int(wind_gust)
        if wind_var_from:
            wind_var_from = int(wind_var_from)
        if wind_var_to:
            wind_var_to = int(wind_var_to)

        if wind_unit == "MPS":
            # Convert to KT
            wind_speed = round(wind_speed * 1.94384)
        if wind_gust:
            wind_gust = round(wind_gust * 1.94384)

        elif wind_unit == "KMH":
            # Convert to KT
            wind_speed = round(wind_speed * 0.539957)
        if wind_gust:
            wind_gust = round(wind_gust * 0.539957)

        # Calculate wind speed in mph
        wind_speed_mph = round(wind_speed * 1.15078)
        if wind_gust:
            wind_gust_mph = round(wind_gust * 1.15078)
        else:
            wind_gust_mph = None

        # Build wind information result
        wind_result = ''

        if wind_deg == 0 and wind_speed == 0:
            wind_result = 'Wind is Calm'

        elif wind_deg == "VRB":
            wind_result = f'Wind is variable at {wind_speed_mph} mph ({wind_speed} knots)'

        elif wind_var_from is not None and wind_var_to is not None:
            wind_result = f'Wind is variable from {wind_dir(wind_var_from)} to {wind_dir(wind_var_to)} at {wind_speed_mph} mph ({wind_speed} knots)'
        else:
            wind_result = f'Wind is blowing from due {wind_dir(wind_deg)} at {wind_speed_mph} mph ({wind_speed} knots)'

        if wind_gust is not None:
            wind_result += f' with gusts to {wind_gust_mph} mph ({wind_gust} knots)'

        api_response = {
            'data': {
                'station': scode,
                'last_observation': f'{dt_list[0]} at {dt_list[1]} GMT',
                'temperature': f'{celsius} C ({fahrenheit} F)',
                'wind': wind_result,
            }
        }

        return api_response, 200

    except Exception:
        logging.exception('')
        return {'error': 'Something went wrong'}, 500
