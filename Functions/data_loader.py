import gpxpy
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point




### **Descripcón:**
"""
**Parámetros:**

- gpx_path (str): La ruta del archivo GPX.
- geojson_path (str): La ruta del archivo GeoJSON.
    
**Retorna:**

- geo_gpx_df (GeoDataFrame): Un GeoDataFrame que contiene los puntos del GPX con su geometría y una columna de tiempo relativa al primer punto.
- geojson_df (GeoDataFrame): Un GeoDataFrame que contiene los datos del archivo GeoJSON.
"""
def geojson_loader(geojson_path):
    # Read the GeoJSON file
    geojson_df = gpd.read_file(geojson_path)
    return geojson_df

def gpx_loader(gpx_path):

    # Leer el archivo GPX
    with open(gpx_path, 'r') as gpx_file:
        gpx_data = gpxpy.parse(gpx_file)

    gpx_points = []
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpx_points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'timestamp': point.time
                })

    geometry = [Point(xy) for xy in zip([p['longitude'] for p in gpx_points], [p['latitude'] for p in gpx_points])]
    geo_gpx_df = gpd.GeoDataFrame(gpx_points, geometry=geometry)
    geo_pd_df = pd.DataFrame(gpx_points)

    # Verificar si geo_gpx_df tiene un CRS asignado
    if geo_gpx_df.crs is None:
        geo_gpx_df = geo_gpx_df.set_crs("EPSG:4326")

        # Convert timestamps to datetime if they aren't already
    if not pd.api.types.is_datetime64_any_dtype(geo_gpx_df['timestamp']):
        geo_gpx_df['timestamp'] = pd.to_datetime(geo_gpx_df['timestamp'])

    # Calculate the 'time' column in seconds relative to the first timestamp
    if geo_gpx_df['timestamp'].isnull().any():
        raise ValueError("Some points are missing timestamps.")
    
    first_time = geo_gpx_df['timestamp'].iloc[0]
    geo_gpx_df['time'] = (geo_gpx_df['timestamp'] - first_time).dt.total_seconds()

    # Print the head of the DataFrame after adding 'time' column
    print("\nDataFrame with 'time' column:")
    print(geo_gpx_df.head())
    
    return geo_gpx_df