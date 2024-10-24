# Importar librerias
import os as os
import sys as sys
import gpxpy as gpxpy
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

### **Descripcón:**
"""
    Esta es la consolda de una función procesa un archivo GPX y un archivo GeoJSON, y aplica un buffer a los datos del GeoJSON.
        
    **Parámetros:**

    - gpx_path (str): La ruta del archivo GPX.
    - geojson_path (str): La ruta del archivo GeoJSON.
    - buffer_size (float): El tamaño del buffer a aplicar a los datos del GeoJSON en metros.
        
    **Retorna:**

    - Directorios: Por cada filtro produce una carpeta que contiene los resultados de la funcion.
    - GeoDataFrame: Por cada uno de los filtros establecidos el programa retorna un GeoDataFrame con los resultados de la unión espacial entre los puntos del GPX y los datos del GeoJSON con buffer.
    - Grafico: Por cada filtro se crea un grafico con la union espacial que se realizo
"""

def gpx_geojson_loader(gpx_path, geojson_path):

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
    
    geojson_df = gpd.read_file(geojson_path)
    return geo_gpx_df, geojson_df

def filter_gpx_data(geo_gpx_df,geojson_df,condition,buffer_size):

    # Condition construction
    updated_condition_string = condition.replace("df", "geojson_df")
    condition_eval = eval(updated_condition_string)
    #Filter by column geojson_df
    filtered_geojson_data = eval("geojson_df")[condition_eval][['ci_o_cr', 'senalzd', 'pintado', 'geometry', 'tipci', 'op_ci']]
    print(f"Este es la columna filtro: {updated_condition_string}")
    print(f"Largo de resultado: {len(filtered_geojson_data)}")
    
    # Check if the length of filtered_geojson_data is 0

    if len(filtered_geojson_data) == 0:
        print("No data found for this condition. Skipping the rest of the function.")
        final_result = None
        return final_result
    else:

        # Convertir a un CRS que use metros
        filtered_geojson_data = filtered_geojson_data.to_crs("EPSG:3857")

        # Crear un buffer alrededor de los datos filtrados del GeoJSON
        buffered_geojson = filtered_geojson_data.buffer(buffer_size)

        # Convertir de nuevo a "EPSG:4326"
        buffered_geojson = buffered_geojson.to_crs("EPSG:4326")
        filtered_geojson_data = filtered_geojson_data.to_crs("EPSG:4326")

        # Graficar los datos del GeoJSON
        fig, ax = plt.subplots()
        filtered_geojson_data.plot(ax=ax, color='red', edgecolor='black', label='Filtered Data')
        buffered_geojson.plot(ax=ax, color='none', edgecolor='green', label='Buffer')
        geo_gpx_df.plot(ax=ax, color='blue', marker='o', label='GPX Points')
        ax.set_title(condition)

        plt.legend()
        plt.show()

        # Crear un GeoDataFrame para el buffer
        buffered_geojson_gdf = gpd.GeoDataFrame(geometry=buffered_geojson)

        # Realizar la unión espacial
        intersection_result = gpd.sjoin(buffered_geojson_gdf, filtered_geojson_data)
        intersection_result.drop(columns=["index_right"], inplace=True)
        final_result = gpd.sjoin(geo_gpx_df, intersection_result, how="left")

        # Condition construction para el loop de condiciones
        updated_condition_string = condition.replace("df", "final_result")
        condition_eval = eval(updated_condition_string) 
        final_result = eval("final_result")[condition_eval][['latitude', 'longitude', 'time', 'geometry', 'index_right', 'ci_o_cr',
                                                                    'senalzd', 'pintado', 'tipci', 'op_ci']]
        print(f"Largo df filtrada: {len(filtered_geojson_data)}")
        return final_result


