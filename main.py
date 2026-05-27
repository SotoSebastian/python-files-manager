import os
import shutil
from pathlib import Path

path = "test_folder"
types = {
    ".png": "png_images",
    ".jpg": "images",
    ".mp4": "videos",
    ".pdf": "documents"
}

def get_files():
    files = []
    for item in Path(path).iterdir():
        if item.is_file():
            files.append(item.name)
            
    return files

def get_extension(archivo):
    _, ext = os.path.splitext(archivo)
    ext = ext.lower()
    return types.get(ext, "ot")

def browse_folder():
    list_files = get_files()
    files_data = []
    for file in list_files:
        category = get_extension(file)
        item = {
            "filename" : file, 
            "filecategory" : category
            }
        files_data.append(item)
    return(files_data)

def organize_files():
    files_data = browse_folder()
    for item in files_data:
        filename = item.get("filename")
        category = item.get("filecategory")
        current_path = Path.cwd()/path
        category_path = Path.cwd()/path/category
        folder = Path(path) / category
        if folder.exists():
            print("Ya existe carpeta de " + category)
        else:
            print("No existe la carpeta de " + category)
            print("Creando carpeta...")
            folder.mkdir()
            print("Car  peta creada con exito!")
        move_item(current_path/filename, category_path, filename)
    return

def move_item(item_origin_path, item_destiny_path, filename):
    if  Path(item_destiny_path/filename).exists():
        print("El archivo ya existe" , item_origin_path)
    else:
        print("El archivo no existe, preparando para copiar...")
        shutil.copy(item_origin_path, item_destiny_path)
        print("Archivo copiado con exito!")
organize_files()
