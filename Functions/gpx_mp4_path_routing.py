import os
import warnings
import re

### **Descripción:**
"""
Recorre solo el primer nivel del directorio 'dataset' y guarda las rutas completas de los subdirectorios y archivos.

**Parámetros:**

- dataset (str): La ruta del directorio a explorar.

**Retorna:**

- paths (list): Una lista de rutas completas de los subdirectorios y archivos en el primer nivel del directorio.
"""
def print_first_level_paths(dataset):
    paths = []
    # Recorre solo el primer nivel del directorio 'dataset'
    for root, dirs, files in os.walk(dataset):
        # 'root' es la ruta del directorio actual
        # 'dirs' es una lista de subdirectorios en el directorio actual
        # 'files' es una lista de archivos en el directorio actual
        
        # Itera sobre todos los subdirectorios en el directorio actual
        for name in dirs:
            # Imprime la ruta completa del subdirectorio
            full_path = os.path.join(root, name)
            print(f"Directory: {full_path}")
            # Guarda la ruta completa del subdirectorio
            paths.append(full_path)
        
        # Itera sobre todos los archivos en el directorio actual
        for name in files:
            # Imprime la ruta completa del archivo
            full_path = os.path.join(root, name)
            print(f"File: {full_path}")
            # Guarda la ruta completa del archivo
            paths.append(full_path)
        
        # Solo queremos el primer nivel, así que rompemos el bucle después del primer directorio
        break
    return paths

### **Descripción:**
"""
Busca una ruta que contenga un número específico dentro de la lista de rutas.

**Parámetros:**

- paths (list): Lista de rutas completas.
- number (int): El número específico a buscar en las rutas.

**Retorna:**

- path (str): La ruta que contiene el número especificado, o None si no se encuentra ninguna.
def fetch_path_with_number(paths, number):
    # Convierte el número a cadena para buscarlo en las rutas
    number_str = str(number)
    print(f"Number to search: {number_str}")
    print(f"Total paths to check: {len(paths)}")
    for path in paths:
        # Imprime la ruta actual para depuración
        #print(f"Checking path: {path}")
        # Verifica si el número está en la ruta (insensible a mayúsculas y minúsculas, y sin espacios)
        if number_str in os.path.basename(path).replace(" ", "").lower():
            print(f"Found matching path: {path}")
            return path
    print(f"No matching path found for number: {number}")
    return None

"""
def fetch_path_with_number(paths, number):
    number_str = f"{number}_"
    pattern = re.compile(rf"^{number}_")
    for path in paths:
        if pattern.match(os.path.basename(path)):
            return path
    return None

### **Descripción:**
"""
Recorre todo el árbol de directorios comenzando desde 'path' y guarda las rutas de los archivos .gpx y .mp4 en listas separadas.

**Parámetros:**

- path (str): La ruta del directorio a explorar.

**Retorna:**

- gpx_files (list): Lista de rutas completas de los archivos .gpx.
- mp4_files (list): Lista de rutas completas de los archivos .mp4.
"""
def get_gpx_and_mp4_files(path):
    gpx_files = []
    mp4_files = []
    # Recorre todo el árbol de directorios comenzando desde 'path'
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith('.gpx'):
                gpx_files.append(os.path.join(root, file))
            elif file.lower().endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))
    return gpx_files, mp4_files

### **Descripción:**
"""
Empareja archivos .gpx y .mp4 que tienen el mismo nombre base y genera advertencias si no hay coincidencias.

**Parámetros:**

- gpx_files (list): Lista de rutas completas de los archivos .gpx.
- mp4_files (list): Lista de rutas completas de los archivos .mp4.

**Retorna:**

- matched_files (list): Lista de tuplas con las rutas emparejadas de archivos .gpx y .mp4.
"""
def match_gpx_and_mp4_files(gpx_files, mp4_files):
    matched_files = []
    # Separa el nombre del archivo de su extensión y toma solo el nombre (sin la extensión)
    # Crea un diccionario donde la clave es el nombre del archivo sin la extensión y el valor es la ruta completa del archivo.
    gpx_dict = {os.path.splitext(os.path.basename(gpx))[0]: gpx for gpx in gpx_files} 
    mp4_dict = {os.path.splitext(os.path.basename(mp4))[0]: mp4 for mp4 in mp4_files}

    for gpx_key, gpx_path in gpx_dict.items():
        if gpx_key in mp4_dict:
            matched_files.append((gpx_path, mp4_dict[gpx_key]))
        else:
            warnings.warn(f"No matching MP4 file for GPX file: {gpx_path}")

    for mp4_key, mp4_path in mp4_dict.items():
        if mp4_key not in gpx_dict:
            warnings.warn(f"No matching GPX file for MP4 file: {mp4_path}")

    return matched_files