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

type_counter = {
    "png_images": 0,
    "images": 0,
    "videos": 0,
    "documents": 0,
    "others": 0
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
    return types.get(ext, "others")

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
    counter = 0
    for item in files_data:
        filename = item.get("filename")
        category = item.get("filecategory")
        counter += 1
        type_counter[category] += 1
        current_path = Path.cwd()/path
        category_path = Path.cwd()/path/category
        folder = Path(path) / category
        if folder.exists():
            print("Ya existe carpeta de " + category)
        else:
            print("No existe la carpeta de " + category)
            print("Creando carpeta...")
            folder.mkdir()
            print("Carpeta creada con exito!")
        move_item(current_path/filename, category_path, filename)
    print(f"Total de archivos organizados: {counter}")
    for category, count in type_counter.items():
        print(f"{category}: {count}")
    return

def move_item(item_origin_path, item_destiny_path, filename):
    if  Path(item_destiny_path/filename).exists():
        print("El archivo ya existe" , item_origin_path)
    else:
        print("El archivo no existe, preparando para copiar...")
        shutil.copy(item_origin_path, item_destiny_path)
        print("Archivo copiado con exito!")
# organize_files()

def rename_item(tag = "", item = {}):
    item_path = Path(path)/item.get("filename")
    _, file_extension = os.path.splitext(item.get("filename"))
    counter = 1
    new_name=  f"{tag}{counter}{file_extension}"
    item_path.rename(new_name)
    counter += 1 