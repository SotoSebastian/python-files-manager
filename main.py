import os
import shutil
from pathlib import Path
from datetime import datetime

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

def get_files(path):
    files = []
    for item in Path(path).iterdir():
        if item.is_file():
            files.append(item.name)
            
    return files

def get_extension(item):
    _, ext = os.path.splitext(item)
    ext = ext.lower()
    return types.get(ext, "others")



def listar_archivos(path):
    list_files = get_files(path)
    files_data = []
    list_category = []  #creamos la lista
    for file in list_files:
        category = get_extension(file)
        list_category.append(category)
        item = {
            "filename" : file, 
            "filecategory" : category,
            }
        files_data.append(item)
    print("Escaneando archivos...")
    category_data = listar_categorias(list_category)
    return files_data, category_data

def listar_categorias(list_category):
    categorias = {}
    for item_category in list_category:
        if item_category in categorias:
            categorias[item_category] += 1
        else:
            categorias[item_category] = 1
    return categorias
        
def move_item(item):
    item_origin_path = item.get("item_origin_path")
    item_destination_path = item.get("item_destination_path")
    filename = item_origin_path.name
    print(item_origin_path, Path(item_destination_path)/filename)
    success_rename = 0
    if  Path(item_destination_path/filename).exists():
        print("El archivo ya existe" , item_origin_path)
    else:
        print("El archivo no existe, preparando para copiar...")
        shutil.move(item_origin_path, item_destination_path)
        print("Archivo copiado con exito!")
        success_rename += 1
    return success_rename

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

def create_logs(action, info_status):
    now_status, old_status = info_status
    date = datetime.now()
    date_format = f"{"["}{date.strftime("%Y-%m-%d %H:%M:%S")}{"]"}"
    action_format = f"{"["}{action}{"]"}"
    with open("logs.txt", "a") as archivo:
        archivo.write(f"{date_format} {action_format} {old_status} {"->"} {now_status}" "\n")
    print (info_status)

def organize_files(source):
    files_data, category_data = listar_archivos(source)
    count = 0
    rename_count = 0
    for category, count in category_data.items():
        print(f"{category}: {count}")
    for item in files_data:
        category = item.get("filecategory")
        filename = item.get("filename")
        source_folder = Path(source)/filename 
        destination_folder = Path(source)/category
        if not destination_folder.exists():
            print(f"Creando carpeta: {category}")
            destination_folder.mkdir()
        item_info = {"item_origin_path" :source_folder,"item_destination_path":destination_folder, "filename": filename}
        count += 1
        # success_status = rename_item("vacaciones", item, count, ".jpg")
        # info_status = {f"{str(source_folder)}/{filename}",str(destination_folder/filename)}
        success_status = move_item(item_info)
        rename_count += success_status
        if success_status: 
            # create_logs("MOVE",info_status)
            print("Se ha creado el archivo logs")
    print("Se han editado:",rename_count,"archivos")


organize_files(r"C:\downloads-organizer\test_folder")