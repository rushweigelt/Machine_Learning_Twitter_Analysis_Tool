'''
This script exists to create a heatmap of the user-supplied locations of suspected bot accounts

Rush Weigelt

3/2/20
'''

import pandas as pd
import gmplot
import certifi
import ssl
import geopandas
from geopy.geocoders import Nominatim
import geopy

#requires a list of city locations
def create_heatmap(cities_list):
    #print("hello")
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    #data = ['Los Angeles, CA', 'Philadelphia, PA', 'Pittsburgh, PA', 'Chicago, IL', '', 'earth']
    locator = Nominatim(user_agent="app", scheme='http')
    #fake_data = ['America', 'Litchfield, CT', 'Present', 'Portland, Oregon  USA', 'Charleston, SC', 'Marietta, GA', 'Portland, Oregon  USA', 'Casa Grande,Arizona', 'United States', 'South Carolina, USA', 'United States', 'Columbia, SC', 'Portland, Oregon  USA', 'Myrtle Beach, SC', 'Washington, USA', 'Hallandale Beach', 'In a world of my own.', 'Living in a world of fools', 'Washington, USA', 'Hallandale Beach']
    #location = locator.geocode("Philadelphia, PA")
    #print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))
    lats = []
    longs = []
    for x in cities_list:
        loc = locator.geocode(x)
        if loc != None:
            lats.append(loc.latitude)
            longs.append(loc.longitude)
    #print("longs:")
    #print(longs)
    gmap = gmplot.GoogleMapPlotter(39.9527237, -75.1635262, 10)
    gmap.heatmap(lats, longs)
    map = gmap.draw("tat/templates/tat/heatmap.html")
    return map

#fake_data = ['America', 'Litchfield, CT', 'Present', 'Portland, Oregon  USA', 'Charleston, SC', 'Marietta, GA', 'Portland, Oregon  USA', 'Casa Grande,Arizona', 'United States', 'South Carolina, USA', 'United States', 'Columbia, SC', 'Portland, Oregon  USA', 'Myrtle Beach, SC', 'Washington, USA', 'Hallandale Beach', 'In a world of my own.', 'Living in a world of fools', 'Washington, USA', 'Hallandale Beach']
#create_heatmap(fake_data)