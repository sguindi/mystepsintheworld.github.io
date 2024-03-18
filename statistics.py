import datetime
import os
import xml.etree.ElementTree as ET
from math import radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):
        # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    
    # Calculate the change in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
     # Haversine formula to calculate distance
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
    
    
def extract_totals(gpx_file_path):
    tree = ET.parse(gpx_file_path)
    root = tree.getroot()
    
    total_distance = 0.0
    total_time = 0
    total_elevation_gain = 0.0
    
    prev_elevation = None
    
    # Iterate over track segments
    for trkseg in root.findall('.//{http://www.topografix.com/GPX/1/1}trkseg'):
        prev_point = None
        prev_time = None
        
        
        for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
            lat = float(trkpt.attrib['lat'])
            lon = float(trkpt.attrib['lon'])
            
            if prev_point :
                total_distance += calculate_distance(prev_point[0],prev_point[1],lat,lon)
            prev_point = (lat,lon)
            
            time_element = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
            if time_element is not None and time_element.text:
                 timestamp = datetime.datetime.strptime(time_element.text, "%Y-%m-%dT%H:%M:%SZ")
                 if prev_time:
                     time_diff = (timestamp-prev_time).total_seconds()
                     total_time += time_diff
                 prev_time = timestamp
                 
            elevation_element = trkpt.find('{http://www.topografix.com/GPX/1/1}ele')
            if elevation_element is not None and elevation_element.text:
                elevation = float(elevation_element.text)
                # Calculate elevation gain if we have previous elevation data
                if prev_elevation is not None:
                   elevation_gain = max(0, elevation - prev_elevation)
                   total_elevation_gain += elevation_gain
                prev_elevation = elevation
            
                
    return total_time, total_distance, total_elevation_gain
 
    

def open_gpx_files():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    total_distance = 0.0
    total_time = 0.0
    total_elevation_gain = 0.0
    
    try:
    # Iterate over all files in the directory
        for filename in os.listdir(script_dir):
            if filename.endswith(".gpx") and filename != 'All_shvil-israel.gpx':
                # Construct the full path to the GPX file
                gpx_file_path = os.path.join(script_dir,filename)
                
                time , distance, elevation_gain = extract_totals(gpx_file_path)
                total_distance += distance
                total_time += time
                total_hours = int(total_time // 3600)
                total_elevation_gain += elevation_gain
        print(f"Total distance in all files : {total_distance} kilometers")
        print(f"Total time in all files : {total_hours} hours")
        print(f"Total elevation in all files : {total_elevation_gain} meters")
                    
    except FileNotFoundError:
        print("Error: No file found")
        
if __name__ == "__main__":
    open_gpx_files()