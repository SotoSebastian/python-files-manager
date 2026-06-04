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

def main():
    option = questionary.select(
        "¿Qué deseas hacer?",
        choices=[
            "Organizar archivos",
            "Renombrar archivos",
            "Salir"
        ]
    ).ask()

    print(option)
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
        origin_path = input("Ingresa la ruta de la carpeta DONDE/ORIGEN se encuentran los archivos ")
        while not origin_path.strip() or not Path(origin_path).is_dir():
            error_info = { "error_type" : "RUTA_INVALIDA" , "error_message" : "La ruta indicada no existe, copia la ruta directo desde el explorador de archivos y pegala aquí:"}
            origin_path = input(f"\n {error_info["error_type"]}" f"\n {error_info["error_message"]} \n ")
        print("RENOMBRAR ARCHIVOS proceso...")   # preguntar si se desea editar un solo archivo o todos los archivos de la carpeta, y luego pedir el tag a agregar al nombre del archivo
        print("Se han encontrado los siguientes tipos de archivos:")
        
        extension_data = get_files_extension(origin_path)
        # print("Se han detectado los siguientes archivos con extensión: ")
        # for ext in extension_data:
        #     print (ext)


    elif option == 'Salir':
        print("CHAU")

def get_files(path):
    files = []
    for item in Path(path).iterdir():
        if item.is_file():
            files.append(item.name)
    return files

def get_file_category(item):
    _, ext = os.path.splitext(item)
    ext = ext.lower()
    return types.get(ext, "others")

def get_files_extension(path):
    list_extensions = []
    for item in Path(path).iterdir():
        _, ext = os.path.splitext(item)
        ext = ext.lower()
        if ext not in list_extensions:
            list_extensions.append(ext)
    return list_extensions

def list_categories(categories_list):
    categories = {}
    for item in categories_list:
        if item in categories:
            categories[item] += 1
        else:
            categories[item] = 1
    return categories
    

def process_list_files(path):
    list_files = get_files(path)
    files_data = []
    for file in list_files:
        item = {
            "filename" : file, 
            "filecategory" : get_file_category(file),
            }   
        files_data.append(item)
    return files_data

def process_list_categories(files_data):
    categories_list = []
    for file in files_data:
        category = get_file_category(file)
        categories_list.append(category)
    category_data = list_categories(categories_list)
    return category_data

def process_action_move(destination, source, item):
    category = item.get("filecategory")
    filename = item.get("filename")
    source_file = Path(source)/filename 
    destination_folder = Path(destination)/category
    item_info = {"item_origin_path" :source_file,"item_destination_path":destination_folder, "filename": filename}

    if not destination_folder.exists():
        print(f"Creando carpeta: {category}")
        destination_folder.mkdir()
    move_info_status = (
        str(source_file),
        str(destination_folder / filename)
    )
    print("Se moveran archivos....")
    success = action_move_item(item_info)
    action_create_logs("MOVE",move_info_status)
    print("Se ha creado el archivo logs")
    return success

def process_action_rename(source, destination, item, tag, filter, counter):
    print("Se renombrarán archivos....")
    success, old_name, new_name = action_rename_item(tag, item, filter, source, counter )
    rename_info_status = (
        str(source)/old_name, 
        str(destination/new_name)
    )
    action_create_logs("RENAME",rename_info_status)
    print("Se ha creado el archivo logs")
    return success

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

def action_rename_item(tag, file, filter, path, counter):
    item_path = Path(path)/file.get("filename")
    old_name, file_extension = os.path.splitext(file.get("filename"))
    count_format = f"{counter:03}"
    new_name = f"{tag}{count_format}{file_extension}"
    success_rename = 0
    if file_extension == filter:
        item_path.rename(new_name)
        print("Se ha modificado el siguiente archivo:", old_name, "con nuevo nombre:", new_name)
        success_rename += 1
    return success_rename, old_name, new_name

def action_create_logs(action, info_status):
    origin, destination = info_status
    date = datetime.now()
    date_format = f"{"["}{date.strftime("%Y-%m-%d %H:%M:%S")}{"]"}"
    action_format = f"{"["}{action}{"]"}"
    with open("logs.txt", "a") as archivo:
        archivo.write(
        f"{date_format} {action_format} {origin} -> {destination}\n"
    )


def organize_files(source, destination_path, action):
    files_data = process_list_files(source)
    move_count = 0
    rename_count = 0
    if action == "MOVE":
        for item in files_data:
            move_count += process_action_move(destination_path, source, item)
        print("Se han movido:",move_count,"archivos")
    if action == "RENAME":
        tag = input("Ingrese la etiqueta de nuevos archivos, se utilizará para renombrar y clasificar los archivos")
        filter = questionary.select(
            "Se detectaron los siguientes tipos de archivos, por favor selecciona que tipo de archivo deseas renombrar: \n",
                choices=[
                    ".jpg",
                    ".docs",
                    ".mp4",
                    ".docs",
                    "Salir"
                ]
        ).ask()
        for counter, item in enumerate(files_data,start = 1):
            rename_count += process_action_rename(source, destination_path, item, tag, filter, counter)
        print("Se han editado:",rename_count,"archivos")

if __name__ == "__main__":
    main()