#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import json, requests
from places_api.util.helper import get_response, json_status_ok, parse_attributes
from places_api.util.thread_pool import ThreadPool

from places_api.util.constants import RADIUS


class Provider(object):
    """
    Attributes:
        lat, lng (string) : latitude and longitude location value.
    """
    def run(self, lat, lng):
        self.location =  ','.join([lat, lng])
        return self.proceed()

class GooglePlaces(Provider):
    """
    Attributes:
        url (string) : URL address of API.
        key (string) : Google Places API key
    """
    def __init__(self):
        self.url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        self.key = 'AIzaSyAUTaT6h_6gfvmrM7hF_f3yP0sWtlZX6G4'

    def get_places_json(self):
        """
        Gets places json value from API.

        Returns:
            json
        """
        params = {}
        params['location'] = self.location
        params['radius'] = RADIUS
        params['key'] = self.key
        data = get_response(self.url, params)
        return data

    def get_place_id_list(self, places):
        """
        Parses and get place_id values from json.

        Returns:
            place_id list
        """
        place_id_list = [place['place_id'] for place in places if 'place_id' in place]
        return place_id_list

    def get_place_detail_list(self, place_id_list):
        """
        Gets place's details, parsing required fields.

        Returns:
            place details list
        """
        num_of_places = len(place_id_list)
        pool = ThreadPool(num_of_places)
        for i in range(num_of_places):
            google_place_details = GooglePlaceDetails(place_id_list[i])
            pool.add_task(google_place_details.get_details)

        result = pool.get_result()
        return result

    def proceed(self):
        """
        Root method of class.

        Returns:
            list of place details
        """
        places_json = self.get_places_json()
        if places_json['status'] != 'OK':
            return []

        data = places_json['results']
        place_id_list = self.get_place_id_list(data)

        get_place_detail_list = self.get_place_detail_list(place_id_list)
        return get_place_detail_list


class GooglePlaceDetails():
    """
    Attributes:
        place_id : id of place from GooglePlaces API.
        url (string) : URL address of API.
        key (string) : Google Places API key
        attributes (dict) : Required attribute from json. 
    """
    def __init__(self, place_id):
        self.place_id = place_id
        self.key = 'AIzaSyAUTaT6h_6gfvmrM7hF_f3yP0sWtlZX6G4'
        self.url = 'https://maps.googleapis.com/maps/api/place/details/json'
        self.attributes = {
        'id': 'place_id',
        'provider': 'scope',
        'name': 'name',
        'description': 'types',
        'loaction': ['geometry', 'location'],
        'address': 'formatted_address',
        'uri': 'website'
        }

    def get_details(self):
        """
        Gets detail of place from Api.

        Returns:
            place details dict
        """
        params = {}
        params['placeid'] = self.place_id
        params['key'] = self.key
        place_json = get_response(self.url, params)
        if place_json['status'] != 'OK':
            return []
        data = place_json['result']
        place_details = parse_attributes(data, self.attributes)
        return place_details


class Foursquare(Provider):
    """
    Attributes:
        url (string) : URL address of API.
        client_id (string) : Foursquare API client id
        client_secret (string) : Foursquare API client secret
        version (string) : Foursquare API date version. Format = YYYYMMDD
    """

    def __init__(self):
        self.url = "https://api.foursquare.com/v2/venues/search"
        self.oauth_token = 'KKFOT40HS4NHXZ3S5MZCJ3010VSEHL5YFNDMEV23OE2AB3H5'
        self.version = '20180622'
        self.attributes = {
            'id': 'id',
            'name': 'name',
            'description': ['categories', 0, 'name'],
            'location': ['location', ['lat', 'lng']],
            'address': ['location', 'formattedAddress']
        }

    def get_places_json(self):
        """
        Gets places json value from API.

        Returns:
            json
        """
        params = {}
        params['ll'] = self.location
        params['oauth_token'] = self.oauth_token
        params['v'] = self.version
        data = get_response(self.url, params)
        return data

    def proceed(self):
        """
        Root method of class.

        Returns:
            list of place details
        """
        places_json = self.get_places_json()
        code = places_json['meta']['code']
        if code != 200:
            return []

        place_detail_list = []
        data = places_json['response']['venues']
        for place_data in data:
            place_details = parse_attributes(place_data, self.attributes)
            place_details['provider'] = 'foursquare'
            place_detail_list.append(place_details)

        return place_detail_list



