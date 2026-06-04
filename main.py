import os
import shutil
from pathlib import Path
import questionary
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

option = questionary.select(
    "¿Qué deseas hacer?",
    choices=[
        "Organizar archivos",
        "Renombrar archivos",
        "Salir"
    ]
).ask()

print(option)


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


def list_categories(list):
    categories = {}
    for item in list:
        if item in categories:
            categories[item] += 1
        else:
            categories[item] = 1
    return categories
    

def process_list_files(path):
    list_files = get_files(path)
    files_data = []
    for file in list_files:
        category = ""
        item = {
            "filename" : file, 
            "filecategory" : category,
            }
        files_data.append(item)
    return files_data

def process_list_categories(files_data):
    list_categories = []
    for file in files_data:
        category = get_extension(file)
        list_categories.append(category)
    category_data = list_categories(list_categories)
    return category_data

def action_move_item(item):
    item_origin_path = item.get("item_origin_path")
    item_destination_path = item.get("item_destination_path")
    filename = item_origin_path.name
    if  Path(item_destination_path/filename).exists():
        print("El archivo ya existe" , item_origin_path)
        return False
    else:
        print("El archivo no existe, preparando para copiar...")
        shutil.move(item_origin_path, item_destination_path)
        print("Archivo copiado con exito!")
        return True

def action_rename_item(item):
    tag = item.get("tag")
    file = item.get("file")
    counter = item.get("counter")
    filter = item.get("filter")
    path = item.get("path")
    item_path = Path(path)/file.get("filename")
    old_name, file_extension = os.path.splitext(file.get("filename"))
    count_format = f"{counter:03}"
    new_name = f"{tag}{count_format}{file_extension}"
    success_rename = 0
    if file_extension == filter:
        item_path.rename(new_name)
        print("Se ha modificado el siguiente archivo:", old_name, "con nuevo nombre:", new_name)
        success_rename += 1
    return success_rename

def action_create_logs(action, info_status):
    now_status, old_status = info_status
    date = datetime.now()
    date_format = f"{"["}{date.strftime("%Y-%m-%d %H:%M:%S")}{"]"}"
    action_format = f"{"["}{action}{"]"}"
    with open("logs.txt", "a") as archivo:
        archivo.write(f"{date_format} {action_format} {old_status} {"->"} {now_status}" "\n")

def process_action_move(destination, source, item):
    category = item.get("filecategory")
    filename = item.get("filename")
    source_folder = Path(source)/filename 
    destination_folder = Path(destination)/category
    item_info = {"item_origin_path" :source_folder,"item_destination_path":destination_folder, "filename": filename}

    if not destination_folder.exists():
        print(f"Creando carpeta: {category}")
        destination_folder.mkdir()
    move_info_status = {f"{str(source_folder)}/{filename}",str(destination_folder/filename)}
    print("Se moveran archivos....")
    success = action_move_item(item_info)
    action_create_logs("MOVE",move_info_status)
    print("Se ha creado el archivo logs")
    return success

def process_action_rename():


def organize_files(source, destination_path, action):
    files_data = process_list_files(source)
    
    rename_count = 0
    move_count = 0
    for item in files_data:
        if action == "MOVE":
            move_count += process_action_move(source, destination_path, item)
        if action == "RENAME":
            rename_count += process_action_rename(source, destination_path, item)
            rename_info_status = {
                "tag" : "vacaciones",
                "file" : item,
                "action" : "RENAME",
                "counter" : files_worked_count,
                "filter" : ".jpg",
                "path" : source
            }
            success_status = action_rename_item(tag, file )
            files_worked_count += 1
            print("Se renombrarán archivos....")
            action_create_logs(action,move_info_status)
            print("Se ha creado el archivo logs")
            rename_count += success_status
    print("Se han editado:",rename_count,"archivos")
#ToDo: trabajar esta sección para que funcione con move y rename

#organize_files(r"C:\downloads-organizer\test_folder")
def main():
    if option == 'Organizar archivos':
        origin_path = input("Ingresa la ruta de la carpeta DONDE/ORIGEN se encuentran los archivos ")
        while not origin_path.strip() or not Path(origin_path).is_dir():
            error_info = { "error_type" : "RUTA_INVALIDA" , "error_message" : "La ruta indicada no existe, copia la ruta directo desde el explorador de archivos y pegala aquí:"}
            origin_path = input(f"\n {error_info["error_type"]}" f"\n {error_info["error_message"]} \n ")
        
        category_data = process_list_categories(get_files(origin_path))
        for category, category_count in category_data.items():
            print(f"{category}: {category_count}")
        input("Se han detectado los siguientes archivos, presiona enter para continuar y ctrl+C para cancelar \n")
        destination_options = questionary.select(
            "¿Donde deseas distribuir los archivos?",
            choices=[
                "En esta misma carpeta, separadas en carpetas distintas según su extensión",
                "En un nuevo directorio",
                "Salir"
            ]
        ).ask()



        if destination_options == "En un nuevo directorio":
            destination_path = input("Ingresa la ruta de la carpeta HACIA/DESTINATION donde se deseas mover los archivos")
            while not destination_path.strip() or not Path(destination_path).is_dir():
                error_info = { "error_type" : "RUTA_INVALIDA" , "error_message" : "La ruta indicada no existe, copia la ruta directo desde el explorador de archivos y pegala aquí:"}
                destination_path = input(f"\n {error_info["error_type"]}" f"\n {error_info["error_message"]} \n ")
        elif destination_options == "En esta misma carpeta, separadas en carpetas distintas según su extensión":
            destination_path = origin_path
            print("Iniciando proceso...")
        organize_files(origin_path, destination_path,"MOVE")

    elif option == 'Renombrar archivos':

        print("RENOMBRAR ARCHIVOS proceso...")   # preguntar si se desea editar un solo archivo o todos los archivos de la carpeta, y luego pedir el tag a agregar al nombre del archivo


    elif option == 'Salir':
        print("CHAU")