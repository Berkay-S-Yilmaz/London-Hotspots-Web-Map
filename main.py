#modules
import folium
import pandas
from geopy.distance import geodesic as dist

#importing coordinates from txt file
data = pandas.read_csv("Hotspots.txt")
lat = list(data["Latitude"])
lon = list(data["Longitude"])
location = list(data["Location"])
postcode = list(data["Postcode"])

#function for color coding icon based on distance from the centre of london
def icon_color(lat, longt):
    london_centre = (51.51003599103894, -0.12969475620475707)
    other_place = (lat, longt) 
    distance = (dist(london_centre, other_place))
    if distance < 2:
        return "green"
    elif distance < 7:
        return "yellow"
    elif distance < 11:
        return "orange"
    else:
        return "red"

#Starting Location, & Zoom amount
map = folium.Map(location=[51.50912964729368, -0.11419922737620807], zoom_start=11)


#Zipped for loop to iterate through through items in Hotspot.txt
hotspots = folium.FeatureGroup(name= "Hotspots")
for latit, longt, loc, post in zip(lat, lon, location, postcode):
    #Icon based on latitude, longtitude, radius of marker, hover on market displays location, popup display postcode
    hotspots.add_child(folium.CircleMarker(location=[latit, longt], radius = 7, tooltip= loc, popup= post,
    #Customization of icons, using the icon_color function, grey outline, & opacity of icon marker 
    fill_color = icon_color(latit, longt), color = "grey", fill_opacity=0.745))

#Feature group for layer control of borders
london_borders = folium.FeatureGroup(name = "Borders")

#london json file containing borders or london boroughs
london_borders.add_child(folium.GeoJson(data=open("london.json", "r", encoding='utf-8-sig').read()))


map.add_child(hotspots)
map.add_child(london_borders)
#layer control for 'Hotspots' & 'Borders' accessed throught the child class
map.add_child(folium.LayerControl())


#save method. Uploading into HTML file
map.save("London Hotspots Map.html")