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

def move_item(item_origin_path, item_destiny_path, filename):
    if  Path(item_destiny_path/filename).exists():
        print("El archivo ya existe" , item_origin_path)
    else:
        print("El archivo no existe, preparando para copiar...")
        shutil.copy(item_origin_path, item_destiny_path)
        print("Archivo copiado con exito!")

def rename_item(tag = "", item=None, counter=1, filter=""):
    item_path = Path(path)/item.get("filename")
    old_name, file_extension = os.path.splitext(item.get("filename"))
    count_format = f"{counter:03}"
    new_name = f"{tag}{count_format}{file_extension}"
    success_rename = 0
    if file_extension == filter:
        item_path.rename(new_name)
        print("Se ha modificado el siguiente archivo:", old_name, "con nuevo nombre:", new_name)
        success_rename += 1
    return success_rename
#rename_item("probando_rename", {"filename": "Esencial.jpg", "category": "jpg"})

def organize_files():
    files_data = browse_folder()
    count = 0
    rename_count = 0
    source_folder = Path(path)
    for item in files_data:
        filename, category = item
        destination_folder = source_folder / category
        if not destination_folder.exists():
            print(f"Creando carpeta: {category}")
            destination_folder.mkdir()
        rename_count += rename_item("vacaciones", item, count, ".jpg")
        count += 1
        # move_item(
        #     source_folder / filename,
        #     destination_folder,
        #     filename
        # )
        # for category, count in type_counter.items():
        #     print(f"{category}: {count}")
    print("Se han editado:",rename_count,"archivos")
                                                                            
organize_files()