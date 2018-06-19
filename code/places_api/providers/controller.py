#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from places_api.providers.models import Provider
from places_api.util.thread_pool import ThreadPool
from functools import reduce

def proceed(lat, lng):
	"""
    Gets places matching location (lat, lng) from different providers.

    Returns:
        list of results from all providers
    """
    
	providers = [sub_class() for sub_class in Provider.__subclasses__()]
	num_of_providers = len(providers)

	pool = ThreadPool(num_of_providers)
	for i in range(num_of_providers):
		pool.add_task(providers[i].run, lat, lng)
	providers_results_list = pool.get_result()

	providers_results = reduce(lambda x,y :x+y , providers_results_list)   # putting all provider's result in one list
	return providers_results
