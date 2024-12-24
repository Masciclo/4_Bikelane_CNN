import geopandas as gpd

### **Descripcón:**
"""
**Parámetros:**

- gpx_path (str): La ruta del archivo GPX.
    
**Retorna:**

- geo_gpx_df (GeoDataFrame): Un GeoDataFrame que contiene los puntos del GPX con su geometría y una columna de tiempo relativa al primer punto.
"""

def geojson_loader(geojson_path,n_ciclo):
    gdf = gpd.read_file(geojson_path)
    filtered_gdf = gdf[gdf['n_ciclo'] == n_ciclo]
    return filtered_gdf
