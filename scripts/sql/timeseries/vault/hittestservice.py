''' VAULT Proposal python module for addressing Technical Scenario objective 1

    | 1) Determine the “hits” where a satellite has geodetic overlap of any vessel(s) 
    |    at any point(s) in time. For simplicity, it may be assumed that a satellite has 
    |    full view of half the earth (regardless of satellite type or its elevation above 
    |    the earth). However, additional accuracy models with rationale is allowed.

    We are using the additional accuracy of actual visiblity of satellite, which also
    happens to result in more interesting looking outputs and made the problem slightly
    more technically challenging

    pip install Flask
    pip install flask-restplus
    pip install Werkzeug==0.16.1
'''

from .hittest import HitTest

from datetime import datetime
from flask import Flask
from flask import request
try:
    # restplus is dead: https://github.com/noirbizarre/flask-restplus/issues/770
    from flask_restx import Resource, Api
    from flask_restx import reqparse
except ImportError:
    try:
        from flask_restplus import Resource, Api
    except ImportError:
        # Bitten by https://github.com/jarus/flask-testing/issues/143
        # Bigger issue: flask_restplus is dead
        import werkzeug
        werkzeug.cached_property = werkzeug.utils.cached_property
        from flask_restplus import Resource, Api
        from flask_restplus import reqparse
from markupsafe import escape
import json

DAY_FILE_PATHS="../data/VAULT_Data/TLE_daily"

app = Flask(__name__)
api = Api(app)

# e.g.: http://127.0.0.1:5000/eval?ts=1467244800&lat=45.0&lon=-176.0

@api.route('/eval')
class HitTestService(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ts', type=int, help='unix epoch seconds')
        parser.add_argument('lat', type=float, help='datetime in unix time format')
        parser.add_argument('lon', type=float, help='datetime in unix time format')
        args = parser.parse_args()

        dt = datetime.fromtimestamp(args["ts"])

        hittest = HitTest(dt, DAY_FILE_PATH)

        result = {"response": hittest.invoke(dt, args["lat"], args["lon"])}

        return result
