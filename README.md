# Places API

## Description
List places matching a location  from multiple providers on the internet (e.g. Google Places, Yelp, and/or Foursquare).

Project have three main modules:
- Providers
    - Suuported providers for places search.
- Resources
    - Resources for Rest-Api (Place Resource) 
- Util
    - Common infrastructure

I tried to make project extendable, so we can easily add new Place Search Providers without core changes. For providers we have *Provider* class which is parent class of all Place Search Providers. To run all providers , I get all subclasses of *Provider* class and run them, so only new Place Search Provider class with methods and attributes needed to add. As we are getting Api responses and parsing them, solution can be slower. To make it faster I used Threads. To demonstrate extensibility side of project by adding new Providers, without core changes.


## Directory tree
```code(root)
└───places_api
    └───providers
    └───resources
    └───util
│   setup.py
```

## Installation

### Environment 
- Python 3.6

### Virtual environment
    $ cd code  # root directory
    $ virtualenv -p python3 venv
    $ source venv/bin/activate

### Dependicies
    $ python setup.py install

## Running
    $ python places_api/app.py 

or

    $ main

## Usage
 - http://0.0.0.0:1818/place?lat=37.95&lng=58.38333
