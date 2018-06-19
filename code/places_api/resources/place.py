#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from flask import request, jsonify
from flask_restful import Resource
from places_api.providers import controller

class Place(Resource):
	def get(self):
		lat = request.args.get('lat', '').strip()
		lng = request.args.get('lng', '').strip()
		results = controller.proceed(lat, lng)

		return jsonify({'results': results})

        

