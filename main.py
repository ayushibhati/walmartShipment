import streamlit as sl
from streamlit_folium import st_folium
import searoute as sr
import folium
import pandas as pd
from streamlit_navigation_bar import st_navbar
import openrouteservice as ors
from openrouteservice import convert

page=st_navbar(["  Team Name:  In Blue","Home","Data","Tools"])
sl.write(page)
sl.title("Supply Chain Dashboard")
sl.text('''The application provides insights to management on various options of distributors 
and supply routes to aid in decision making.''')


Delhi=[28.632440, 77.219823]
New_york=[40.651421, -74.035739]
japan=[40.817265, 140.298654]
Ningbo=[29.943321, 121.805404]
Shenzen=[22.480941, 113.879724]
with sl.sidebar:
    name1=sl.text_input('Enter the Walmart Warehouse Code / Name:')
    product=sl.text_input('Enter the Product Code / Name that is required:')
    quantity=sl.text_input('Enter the amount that is reuired (to calculate shipping costs):')
    select=sl.selectbox(
    "Restrictions in supply chain (if any) ",
    ("Swiss-Canal is Closed", "India-China Border is closed", "Kolkata port is closed"),
    index=None)



def main():
    #Initial:
    sl.text("Yellow lines: Air Route, White lines: Sea Route, Green lines: Road Route")
    m=folium.Map(location=Delhi,zoom_start=6)
    #New york to india air:

    origin=New_york
    destination=Delhi

    
    folium.PolyLine(locations=[origin, destination], tooltip="New Jersey to New Delhi (Air)", color='yellow').add_to(m)
    origin=japan
    folium.PolyLine(locations=[origin, destination], tooltip="Japan to New Delhi (Air)", color='yellow').add_to(m)
    origin=Shenzen
    folium.PolyLine(locations=[origin, destination], tooltip="China to New Delhi (Air)", color='yellow').add_to(m)
    # route=sr.searoute(origin,destination)
    # US Suez-canal
    origin=New_york
    destination=[18.965574, 72.837136] #Mumbai
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)
    API_KEY = '5b3ce3597851110001cf624818a0afd37b2649d080bf118e01cee0f2'

    client = ors.Client(key=API_KEY)

    source=(18.965574, 72.837136) #Mumbai
    destination = (28.632440, 77.219823) # Delhi

    # Get directions between the two points
    # Note: OpenRouteService expects (lng, lat) tuples
    directions_coordinates = [tuple(reversed(source)), tuple(reversed(destination))]  
    route = client.directions(coordinates=directions_coordinates, profile='driving-car', format='geojson')

    # extracting only coordinates
    routes_coords= [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]

    # o/p 
    # [[28.280381, 78.013985],
    #  [28.280266, 78.014388],
    #  [28.280192, 78.014739],
    #  [28.280161, 78.014831],
    #  [28.280103, 78.014876],
    #  [28.279703, 78.014801],
    #  [28.279316, 78.014659]] #
    folium.PolyLine(locations=routes_coords,
           color='green',
           weight=4,           # width of polyline
           tooltip="From Mumbai to Delhi",
           smooth_factor=0.1,  #  for making poliyline straight
           ).add_to(m)
    
    #japan to kolkata
    origin=japan
    destination=[21.914871, 88.197271] #kolkata
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)
    API_KEY = '5b3ce3597851110001cf624818a0afd37b2649d080bf118e01cee0f2'

    client = ors.Client(key=API_KEY)

    source=(21.914871, 88.197271) #kolkata
    destination = (28.632440, 77.219823) # Delhi

    # Get directions between the two points
    # Note: OpenRouteService expects (lng, lat) tuples
    directions_coordinates = [tuple(reversed(source)), tuple(reversed(destination))]  
    route = client.directions(coordinates=directions_coordinates, profile='driving-car', format='geojson')

    # extracting only coordinates
    routes_coords= [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]

    # o/p 
    # [[28.280381, 78.013985],
    #  [28.280266, 78.014388],
    #  [28.280192, 78.014739],
    #  [28.280161, 78.014831],
    #  [28.280103, 78.014876],
    #  [28.279703, 78.014801],
    #  [28.279316, 78.014659]] #
    folium.PolyLine(locations=routes_coords,
           color='green',
           weight=4,           # width of polyline
           tooltip="From Mumbai to Delhi",
           smooth_factor=0.1,  #  for making poliyline straight
           ).add_to(m)
    folium.PolyLine(locations=[[21.914871, 88.197271], [21.014871, 88.097271]], color='white').add_to(m)



    # m=folium.Map(location=coordinates[0],zoom_start=6)

    
    
    # By Road china:
    source=(22.480941, 113.879724) #shenzen
    destination=(28.632440, 77.219823) # Delhi
    directions_coordinates = [tuple(reversed(source)), tuple(reversed(destination))]  
    route = client.directions(coordinates=directions_coordinates, profile='driving-car', format='geojson')

    # extracting only coordinates
    routes_coords= [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
    folium.PolyLine(locations=routes_coords,
           color='green',
           weight=4,           # width of polyline
           tooltip="From Shikarpur to Binaur",
           smooth_factor=0.1,  #  for making poliyline straight
           ).add_to(m)
    st_map=st_folium(m, width=700, height=450)

    # china to chennai
    origin=Shenzen
    destination=[13.100826, 80.293689] #chennai
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)

    data = {
        'Origin': ['USA (New York)', 'USA (New York)', 'USA (New York)', 'Japan', 'Japan','Japan','China(Ningbo)','China(Shenzen)','China(Beijing)'],
        'Product': ['Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple'],
        'Shipping Cost (Dollar)': [4000, 1600, 1750, 2100, 800, 820, 750, 1700, 1200],
        'Shipping Time (days)': [3, 25, 45, 2, 14, 15, 12, 2, 14],
        'Route type':['Air','Sea(Suez-Canal)','Sea(Cape of good hope)','Air','Sea','Sea','Sea','Air','Road'],
        'Destination': ['New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi'],
        'Probability to Arrive on Time (%)': [95, 90, 98, 92, 88, 90, 98, 92, 98],
        'Expected Time Range (days)': ['2-4', '23-27', '41-46', '2-3', '14-16','14-16','11-12','2-3','12-16'],
        'Base Price' : [2.6,2.6,2.6,1.7,1.7,1.7,2.0,2.0,2.0],
        'Total Price' : [5300,2900,3050,2950,1650,1670,1750,2700,2200]
    }
    df = pd.DataFrame(data)
    sl.write("Fastest option for the product:")
    sl.write(df[df['Total Price'] == 1650])
    sl.write("Cheapest option for the product:")
    sl.write(df[df['Expected Time Range (days)']=='2-3'])
    sl.write("All available options for the product:")
    sl.write(df)


def main_good():
    #Initial:
    m=folium.Map(location=Delhi,zoom_start=6)
    #New york to india air:

    origin=New_york
    destination=Delhi

    
    folium.PolyLine(locations=[origin, destination], tooltip="New Jersey to New Delhi (Air)", color='yellow').add_to(m)
    origin=japan
    folium.PolyLine(locations=[origin, destination], tooltip="Japan to New Delhi (Air)", color='yellow').add_to(m)
    origin=Shenzen
    folium.PolyLine(locations=[origin, destination], tooltip="China to New Delhi (Air)", color='yellow').add_to(m)
    # route=sr.searoute(origin,destination)
    # US Suez-canal
    origin=[-33.957077, 18.378381] # New_york
    destination=[18.965574, 72.837136] #Mumbai
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)
    origin=New_york
    destination=[-33.957077, 18.378381] #cape
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)
    API_KEY = '5b3ce3597851110001cf624818a0afd37b2649d080bf118e01cee0f2'

    client = ors.Client(key=API_KEY)

    source=(18.965574, 72.837136) #Mumbai
    destination = (28.632440, 77.219823) # Delhi

    # Get directions between the two points
    # Note: OpenRouteService expects (lng, lat) tuples
    directions_coordinates = [tuple(reversed(source)), tuple(reversed(destination))]  
    route = client.directions(coordinates=directions_coordinates, profile='driving-car', format='geojson')

    # extracting only coordinates
    routes_coords= [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]

    # o/p 
    # [[28.280381, 78.013985],
    #  [28.280266, 78.014388],
    #  [28.280192, 78.014739],
    #  [28.280161, 78.014831],
    #  [28.280103, 78.014876],
    #  [28.279703, 78.014801],
    #  [28.279316, 78.014659]] #
    folium.PolyLine(locations=routes_coords,
           color='green',
           weight=4,           # width of polyline
           tooltip="From Mumbai to Delhi",
           smooth_factor=0.1,  #  for making poliyline straight
           ).add_to(m)
    
    #japan to kolkata
    origin=japan
    destination=[21.914871, 88.197271] #kolkata
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)
    API_KEY = '5b3ce3597851110001cf624818a0afd37b2649d080bf118e01cee0f2'

    client = ors.Client(key=API_KEY)

    source=(21.914871, 88.197271) #kolkata
    destination = (28.632440, 77.219823) # Delhi

    # Get directions between the two points
    # Note: OpenRouteService expects (lng, lat) tuples
    directions_coordinates = [tuple(reversed(source)), tuple(reversed(destination))]  
    route = client.directions(coordinates=directions_coordinates, profile='driving-car', format='geojson')

    # extracting only coordinates
    routes_coords= [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]

    # o/p 
    # [[28.280381, 78.013985],
    #  [28.280266, 78.014388],
    #  [28.280192, 78.014739],
    #  [28.280161, 78.014831],
    #  [28.280103, 78.014876],
    #  [28.279703, 78.014801],
    #  [28.279316, 78.014659]] #
    folium.PolyLine(locations=routes_coords,
           color='green',
           weight=4,           # width of polyline
           tooltip="From Mumbai to Delhi",
           smooth_factor=0.1,  #  for making poliyline straight
           ).add_to(m)
    folium.PolyLine(locations=[[21.914871, 88.197271], [21.014871, 88.097271]], color='white').add_to(m)



    # m=folium.Map(location=coordinates[0],zoom_start=6)

    
    
    # By Road china:
    source=(22.480941, 113.879724) #shenzen
    destination=(28.632440, 77.219823) # Delhi
    directions_coordinates = [tuple(reversed(source)), tuple(reversed(destination))]  
    route = client.directions(coordinates=directions_coordinates, profile='driving-car', format='geojson')

    # extracting only coordinates
    routes_coords= [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
    folium.PolyLine(locations=routes_coords,
           color='green',
           weight=4,           # width of polyline
           tooltip="From Shikarpur to Binaur",
           smooth_factor=0.1,  #  for making poliyline straight
           ).add_to(m)
    st_map=st_folium(m, width=700, height=450)

    # china to chennai
    origin=Shenzen
    destination=[13.100826, 80.293689] #chennai
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)

    data = {
        'Origin': ['USA (New York)', 'USA (New York)', 'USA (New York)', 'Japan', 'Japan','Japan','China(Ningbo)','China(Shenzen)','China(Beijing)'],
        'Product': ['Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple'],
        'Shipping Cost (Dollar)': [4000, 1600, 1750, 2100, 800, 820, 750, 1700, 1200],
        'Shipping Time (days)': [3, 25, 45, 2, 14, 15, 12, 2, 14],
        'Route type':['Air','Sea(Suez-Canal)','Sea(Cape of good hope)','Air','Sea','Sea','Sea','Air','Road'],
        'Destination': ['New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi'],
        'Probability to Arrive on Time (%)': [95, 90, 98, 92, 88, 90, 98, 92, 98],
        'Expected Time Range (days)': ['2-4', '23-27', '41-46', '2-3', '14-16','14-16','11-12','2-3','12-16'],
        'Base Price' : [2.6,2.6,2.6,1.7,1.7,1.7,2.0,2.0,2.0],
        'Total Price' : [5300,2900,3050,2950,1650,1670,1750,2700,2200]
    }
    df = pd.DataFrame(data)
    sl.write("Fastest option for the product:")
    sl.write(df[df['Total Price'] == 1650])
    sl.write("Cheapest option for the product:")
    sl.write(df[df['Expected Time Range (days)']=='2-3'])
    sl.write("All available options for the product:")
    sl.write(df)


def main_k():
    #Initial:
    m=folium.Map(location=Delhi,zoom_start=6)
    #New york to india air:

    origin=New_york
    destination=Delhi

    
    folium.PolyLine(locations=[origin, destination], tooltip="New Jersey to New Delhi (Air)", color='yellow').add_to(m)
    origin=japan
    folium.PolyLine(locations=[origin, destination], tooltip="Japan to New Delhi (Air)", color='yellow').add_to(m)
    origin=Shenzen
    folium.PolyLine(locations=[origin, destination], tooltip="China to New Delhi (Air)", color='yellow').add_to(m)
    # route=sr.searoute(origin,destination)
    # US Suez-canal
    origin=New_york
    destination=[18.965574, 72.837136] #Mumbai
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)
    API_KEY = '5b3ce3597851110001cf624818a0afd37b2649d080bf118e01cee0f2'

    client = ors.Client(key=API_KEY)

    source=(18.965574, 72.837136) #Mumbai
    destination = (28.632440, 77.219823) # Delhi

    # Get directions between the two points
    # Note: OpenRouteService expects (lng, lat) tuples
    directions_coordinates = [tuple(reversed(source)), tuple(reversed(destination))]  
    route = client.directions(coordinates=directions_coordinates, profile='driving-car', format='geojson')

    # extracting only coordinates
    routes_coords= [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]

    # o/p 
    # [[28.280381, 78.013985],
    #  [28.280266, 78.014388],
    #  [28.280192, 78.014739],
    #  [28.280161, 78.014831],
    #  [28.280103, 78.014876],
    #  [28.279703, 78.014801],
    #  [28.279316, 78.014659]] #
    folium.PolyLine(locations=routes_coords,
           color='green',
           weight=4,           # width of polyline
           tooltip="From Mumbai to Delhi",
           smooth_factor=0.1,  #  for making poliyline straight
           ).add_to(m)
    



    # m=folium.Map(location=coordinates[0],zoom_start=6)

    
    
    # By Road china:
    source=(22.480941, 113.879724) #shenzen
    destination=(28.632440, 77.219823) # Delhi
    directions_coordinates = [tuple(reversed(source)), tuple(reversed(destination))]  
    route = client.directions(coordinates=directions_coordinates, profile='driving-car', format='geojson')

    # extracting only coordinates
    routes_coords= [list(reversed(coord)) for coord in route['features'][0]['geometry']['coordinates']]
    folium.PolyLine(locations=routes_coords,
           color='green',
           weight=4,           # width of polyline
           tooltip="From Shikarpur to Binaur",
           smooth_factor=0.1,  #  for making poliyline straight
           ).add_to(m)
    st_map=st_folium(m, width=700, height=450)

    # china to chennai
    origin=Shenzen
    destination=[13.100826, 80.293689] #chennai
    origin[0],origin[1]=origin[1],origin[0]
    destination[0],destination[1]=destination[1],destination[0]

    route = sr.searoute(origin, destination, speed_knot=12.5,units='naut',return_passages=True)

    coordinates=route['geometry']['coordinates']

    coordinates=[[coord[1],coord[0]] for coord in coordinates]
    # m=folium.Map(location=coordinates[0],zoom_start=6)

    for coord in coordinates:
        folium.CircleMarker(location=coord, radius=0.0001, fill_color='white',color='white').add_to(m)
    folium.PolyLine(locations=coordinates,color="white",weight=5).add_to(m)

    data = {
        'Origin': ['USA (New York)', 'USA (New York)', 'USA (New York)', 'Japan', 'Japan','Japan','China(Ningbo)','China(Shenzen)','China(Beijing)'],
        'Product': ['Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple', 'Apple'],
        'Shipping Cost (Dollar)': [4000, 1600, 1750, 2100, 800, 820, 750, 1700, 1200],
        'Shipping Time (days)': [3, 25, 45, 2, 14, 15, 12, 2, 14],
        'Route type':['Air','Sea(Suez-Canal)','Sea(Cape of good hope)','Air','Sea','Sea','Sea','Air','Road'],
        'Destination': ['New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi', 'New Delhi'],
        'Probability to Arrive on Time (%)': [95, 90, 98, 92, 88, 90, 98, 92, 98],
        'Expected Time Range (days)': ['2-4', '23-27', '41-46', '2-3', '14-16','14-16','11-12','2-3','12-16'],
        'Base Price' : [2.6,2.6,2.6,1.7,1.7,1.7,2.0,2.0,2.0],
        'Total Price' : [5300,2900,3050,2950,1650,1670,1750,2700,2200]
    }
    df = pd.DataFrame(data)
    sl.write("Fastest option for the product:")
    sl.write(df[df['Total Price'] == 1650])
    sl.write("Cheapest option for the product:")
    sl.write(df[df['Expected Time Range (days)']=='2-3'])
    sl.write("All available options for the product:")
    sl.write(df)
if product=="Apple":
    if __name__ == "__main__":
        if select=='Swiss-Canal is Closed':
            main_good()
        elif select=="Kolkata port is closed":
            main_k()
        else:
            main()
