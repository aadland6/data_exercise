# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 08:33:59 2016

@author: aadlandma
"""
import csv
import geocoder 
import folium
path = "C:/Users/aadlandma/Desktop/deloitte_exercise/"
rows = []
with open(path + "femalesRaw.csv", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
        
male_rows = []
with open(path + "males.csv", "rb") as f:
        reader = csv.reader(f)
        for row in reader:
            male_rows.append(row)

def geocode_rows(rows):
    rows_geo = []
    for row in rows:
        try:
            g = geocoder.google(row[6])
            row += g.latlng
            rows_geo.append(row)
        except:
            row += [0,0]
            rows_geo.append(row)
    return rows_geo

def second_pass(geocoded_rows):
    locations = []
    for each in geocoded_rows:
        try:
            location =  [each[14],each[15]]
            locations.append(location) 
        except IndexError:
            # try again with arc
            g = geocoder.arcgis(each[6])
            if g.latlng:
                location = g.latlng
                locations.append(location)
            else:
                locations.append([0,0]) # give up 
    return locations 
        
def fix_silverspring(locations,df):
    for i in range(len(locations)):
        if df[i][6] == 'Silver Spring M':
            locations[i] = [38.9907, -77.0261]
        elif df[i][6] == 'Montgomery Vill':
            locations[i] = [40.2473, -75.2438]
        else:
            pass 
    return locations 
    
        
    
geocoded_females = geocode_rows(rows)
geocoded_males = geocode_rows(male_rows)
locations = second_pass(geocoded_females)
male_locations = second_pass(geocoded_males)
male_locations = fix_silverspring(geocoded_males,male_rows)
rockville = [39.0840,-77.15283]
females_map = folium.Map(location=rockville, zoom_start=5)
males_map = folium.Map(location=rockville, zoom_start=5)

# map1.add_children(my_marker_cluster1)
map1 = folium.Map(location=rockville,zoom_start=9)
my_marker_cluster1 = folium.MarkerCluster()
for i in range(len(locations)):
    folium.Marker(location=locations[i],popup=geocoded_females[i][4]).add_to(my_marker_cluster1)
map1.add_children(my_marker_cluster1)
map1.save("females2.html")

map2 = folium.Map(location=rockville,zoom_start=9)
my_marker_cluster2 = folium.MarkerCluster()
for i in range(len(male_locations)):
    try:
        folium.Marker(location=[male_locations[i][14],male_locations[i][15]]
        ,popup=geocoded_males[i][4]).add_to(my_marker_cluster2)
    except:
        # the popup can't handle unicode-pass with try/except
        folium.Marker(location=male_locations[i],popup='').add_to(my_marker_cluster2)
map2.add_children(my_marker_cluster2)
map2.save("males.html")

