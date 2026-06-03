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

if option == 'Organizar archivos':
    origin_path = input("Ingresa la ruta de LA CARPETA donde se encuentran los archivos ")
    # se valida si la ruta existe o si está bien ingresada, si no se vuelve a pedir la ruta 
    while not origin_path.strip() or not Path(origin_path).is_dir():
        error_info = { "error_type" : "RUTA_INVALIDA" , "error_message" : "La ruta indicada no existe, copia la ruta directo desde el explorador de archivos y pegala aquí:"}
        origin_path = input(f"\n {error_info["error_type"]}" f"\n {error_info["error_message"]} \n ")
    # se solicita ruta de destino, se puede utilizar el mismo directorio u otro nuevo que se solicita y valida 

    destination_options = questionary.select(
        "¿Donde deseas distribuir los archivos?",
        choices=[
            "En esta misma carpeta, separadas en carpetas distintas según su extensión",
            "En un nuevo directorio",
            "Salir"
        ]
    ).ask()

    if destination_options == "En un nuevo directorio":
        destination_path = input("Ingresa la ruta de LA CARPETA hacía donde se deseas mover los archivos")
        # se valida si la ruta existe o si está bien ingresada, si no se vuelve a pedir la ruta
        while not Path(destination_path).is_dir():
           
            destination_path = input(f"{error_info["error_type"], error_info["error_message"]}")
        # luego se solicita la ruta de destino, se valida si existe, si no existe se ofrece crear la carpeta o utilizar la misma carpeta de origen.
        destination_path = input("Ingresa la ruta de destino")
    elif destination_options == "En esta misma carpeta, separadas en carpetas distintas según su extensión":
        destination_path = Path.cwd

elif option == 'Renombrar archivos':
    print("")   # preguntar si se desea editar un solo archivo o todos los archivos de la carpeta, y luego pedir el tag a agregar al nombre del archivo
elif option == 'Salir':
    print("")


def get_files():
    files = []
    for item in Path("test_folder").iterdir():
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
    success_rename = 0
    if  Path(item_destination_path/filename).exists():
        print("El archivo ya existe" , item_origin_path)
    else:
        print("El archivo no existe, preparando para copiar...")
        shutil.move(item_origin_path, item_destination_path)
        print("Archivo copiado con exito!")
        success_rename += 1
    return success_rename

def rename_item(item):
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

def create_logs(action, info_status):
    now_status, old_status = info_status
    date = datetime.now()
    date_format = f"{"["}{date.strftime("%Y-%m-%d %H:%M:%S")}{"]"}"
    action_format = f"{"["}{action}{"]"}"
    with open("logs.txt", "a") as archivo:
        archivo.write(f"{date_format} {action_format} {old_status} {"->"} {now_status}" "\n")

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
        move_info_status = {f"{str(source_folder)}/{filename}",str(destination_folder/filename)}
        rename_info_status = {
            "tag" : "vacaciones",
            "file" : item,
            "action" : "RENAME",
            "counter" : count,
            "filter" : ".jpg",
            "path" : source
        }
        success_status = rename_item(rename_info_status)
        #success_status = move_item(item_info)
        rename_count += success_status
        if success_status: 
            create_logs("MOVE",move_info_status)
            print("Se ha creado el archivo logs")
    print("Se han editado:",rename_count,"archivos")


#organize_files(r"C:\downloads-organizer\test_folder")
