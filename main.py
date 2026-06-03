import os
import shutil
from pathlib import Path
import questionary

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
    error_info = {"error_type" : "", "error_message" : ""}
    origin_path = input("Ingresa la ruta de LA CARPETA donde se encuentran los archivos\n")
    # se valida si la ruta existe o si está bien ingresada, si no se vuelve a pedir la ruta
    while not Path(origin_path).exists():
        error_info["error_type"] = "RUTA_INVALIDA"
        error_info["error_message"] = "La ruta indicada no existe, copia la ruta directo desde el explorador de archivos\n"
        origin_path = input(f"{error_info["error_type"], error_info["error_message"]}")
    #se solicita ruta de destino, se puede utilizar el mismo directorio u otro nuevo que se solicita y valida 
    destination_options = questionary.select(
        "¿Donde deseas distribuir los archivos?",
        choices=[
            "En esta misma carpeta, separadas en carpetas distintas según su extensión",
            "En un nuevo directorio",
            "Salir"
        ]
    ).ask()
    if destination_options == "En un nuevo directorio":
        destination_path = input("Ingresa la ruta de LA CARPETA hacía donde se deseas mover los archivos\n")
        # se valida si la ruta existe o si está bien ingresada, si no se vuelve a pedir la ruta
        while not Path(destination_path).exists():
            error_info["error_type"] = "RUTA_INVALIDA"
            error_info["error_message"] = "La ruta indicada no existe, copia la ruta directo desde el explorador de archivos\n"
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