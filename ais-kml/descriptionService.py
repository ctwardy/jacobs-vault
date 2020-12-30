
from datetime import datetime
from flask import Flask
from flask import request

from flask import send_file


try:
    # restplus is dead: https://github.com/noirbizarre/flask-restplus/issues/770
    from flask_restx import Resource, Api
    from flask_restx import reqparse
except ImportError:
    try:
        from flask_restplus import Resource, Api
    except ImportError:

        import werkzeug
        werkzeug.cached_property = werkzeug.utils.cached_property
        from flask_restplus import Resource, Api
        from flask_restplus import reqparse
from markupsafe import escape
import json

app = Flask(__name__)
api = Api(app)

# e.g.: http://127.0.0.1:5000/test?ts=1467244800&lat=45.0&lon=-176.0

@api.route('/test')
class TestService(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('ts', type=int, help='unix epoch seconds')
        parser.add_argument('lat', type=float, help='datetime in unix time format')
        parser.add_argument('lon', type=float, help='datetime in unix time format')
        args = parser.parse_args()

        dt = datetime.fromtimestamp(args["ts"])
        result = {"response" : "HelloWorld"}
        return result

@api.route('/get_image')
class ImageService(Resource):
    def get(self):
        icon1="icons/circle-xl.png"
        return send_file(icon1, mimetype='image/png')
