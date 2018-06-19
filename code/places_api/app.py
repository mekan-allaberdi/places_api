#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from places_api.resources.place import Place

def run_app():
	app = Flask(__name__)
	api = Api(app)
	api.add_resource(Place, '/place')
	app.run(host='0.0.0.0', port=1818, debug=True)

if __name__ == '__main__':
	run_app()
	