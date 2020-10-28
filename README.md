# METAR API

## Project Overview

To design and implement REST API endpoints to parse METAR codes.

## Getting Started

### Prerequisites

* Python 3.6+
* Git
* Redis

### Project Setup

1. Clone this repo: `$ git clone https://github.com/jebinphilipose/metar-api.git && cd metar-api`
2. Create a `.env` file in project root, see `metar-api/api/settings.py` for list of all variables
3. Create a virtual environment: `$ python3 -m venv ./venv`
4. Activate virtualenv: `$ source venv/bin/activate`
5. Upgrade pip and install dependencies: `$ pip install --upgrade pip && pip install -r requirements.txt`
6. Run the server: `$ deactivate && source venv/bin/activate && flask run`


## API Endpoints

* GET [/api/v1/metar/ping/](http://localhost:8000/api/v1/metar/ping/) --> Returns response `{'data': 'PONG'}`
* GET [/api/v1/metar/info/](http://localhost:8000/api/v1/metar/info/) --> Returns JSON of parsed METAR code

  * Query params:
    
    1. scode (Required) - If provided will return METAR info for that particular station, else 400
    2. nocache (Optional) - If `nocache=1` is provided, API will fetch live data and refresh cache

  Note:
  * All API responses are cached for 5 minutes in Redis cache
  * For wind readings following units are supported: KT, MPS, KMH
  * All types of wind reports are covered including calm wind, wind with variable direction and wind with gust
  * For production, the application can be Dockerized and Nginx can be used as a web server to load balance app servers running behind gunicorn workers
