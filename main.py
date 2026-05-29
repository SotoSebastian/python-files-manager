import os
import shutil
from pathlib import Path
from datetime import datetime

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

def get_extension(item):
    _, ext = os.path.splitext(item)
    ext = ext.lower()
    return types.get(ext, "others")



def browse_folder():
    list_files = get_files()
    files_data = []
    list_category = []
    for file in list_files:
        category = get_extension(file)
        item = {
            "filename" : file, 
            "filecategory" : category,
            }
        for category in list_category:
            if not item.get("filecategory") == category:
                list_category.append(category)
        files_data.append(item)
    print("Escaneando archivos...")
    print(list_category)

    return files_data

def move_item(item):
    item_origin_path = item.get("item_origin_path")
    item_destination_path = item.get("item_destination_path")
    filename = item.get("filename") 
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

def organize_files():
    files_data = browse_folder()
    count = 0
    rename_count = 0
    source_folder = Path(path)
    for item in files_data:
        filename = item.get("filename")
        category = item.get("filecategory")
        destination_folder = source_folder /category
        print(filename,category)
        if not destination_folder.exists():
            print(f"Creando carpeta: {category}")
            destination_folder.mkdir()
        # success_status = rename_item("vacaciones", item, count, ".jpg")
        # info_status = {f"{str(source_folder)}/{filename}",str(destination_folder/filename)}
        item_info = {"item_origin_path" : f"{str(source_folder)}/{filename}","item_destination_path":destination_folder, "filename": filename}
        count += 1
        success_status = move_item(item_info)
        rename_count += success_status
        for category, count in type_counter.items():
            print(f"{category}: {count}")
        # if success_status: 
        #     create_logs("MOVE",info_status)
        #     print("Se ha creado el archivo logs")
    print("Se han editado:",rename_count,"archivos")

organize_files()