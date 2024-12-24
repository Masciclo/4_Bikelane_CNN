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
**Parámetros:**

- geo_gpx_df (GeoDataFrame): Un GeoDataFrame que contiene los puntos del GPX.
- geojson_df (GeoDataFrame): Un GeoDataFrame que contiene los datos del archivo GeoJSON.
- condition (str): Una condición lógica para filtrar los datos del GeoJSON.
- buffer_size (float): El tamaño del buffer a aplicar a los datos del GeoJSON en metros.
    
**Retorna:**

- final_result (GeoDataFrame): Un GeoDataFrame con los resultados de la unión espacial entre 
  los puntos del GPX y los datos del GeoJSON con buffer, filtrados según la condición dada.
"""


def filter_gpx_data(geo_gpx_df,geojson_df,condition,buffer_size):

    # Condition construction
    updated_condition_string = condition.replace("df", "geojson_df")
    condition_eval = eval(updated_condition_string)
    #Filter by column geojson_df
    filtered_geojson_data = eval("geojson_df")[condition_eval][['ci_o_cr', 'senaliz', 'pintado', 'geometry', 'tipci', 'op_ci']]
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
        ax.set_title(f"{condition} with buffer size {buffer_size} meters")

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
                                                                    'senaliz', 'pintado', 'tipci', 'op_ci']]
        print(f"Largo df filtrada: {len(filtered_geojson_data)}")
        return final_result


