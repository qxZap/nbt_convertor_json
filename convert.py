import os
import shutil
import json
import copy

INPUT_FOLDER = "input/"
OUTPUT_FOLDER = "output/"
ENTITY_FOLDER = "entity_injection/"

FOLDERS = [INPUT_FOLDER,OUTPUT_FOLDER,ENTITY_FOLDER]

NBT_EXT = ".nbt"
JSON_EXT = ".json"
TEMP_FILE = "tmp.tmp"

NBT_TO_JSON_COMMAND = "nbt -r {} --pretty --json > {}"
JSON_TO_NBT_COMMAND = "nbt -s {} -w {}"

def get_new_file_name(file_name):
    if file_name.endswith(NBT_EXT):
        return file_name.replace(NBT_EXT,JSON_EXT).replace(INPUT_FOLDER,OUTPUT_FOLDER)
    else:
        return file_name.replace(JSON_EXT,NBT_EXT).replace(INPUT_FOLDER,OUTPUT_FOLDER)

def get_input_files():
    input_files = []
    input_files_from_folder = os.listdir(INPUT_FOLDER)
    for input_file_from_folder in input_files_from_folder:
        input_files.append(INPUT_FOLDER+input_file_from_folder)
    return input_files

def does_file_exist(filepath):
    return os.path.exists(filepath)

def create_folder_if_not_existent(folder):
    try:
        os.mkdir(folder)
    except Exception:
        pass

def create_needed_folders():
    for folder in FOLDERS:
        create_folder_if_not_existent(folder)

def get_json_data(filepath):
    file = open(filepath,"r")
    str_data = file.read()
    file.close()
    json_data = json.loads(str_data)
    return json_data

def set_entities_in_json_data(json_data,entity_json_data):
    return_data = copy.deepcopy(json_data)
    return_data[""]["entities"] = entity_json_data["entities"]
    return return_data

def inject_entyties_if_present(input_file_path):
    possible_entity_file_path = input_file_path.replace(INPUT_FOLDER,ENTITY_FOLDER)
    if does_file_exist(possible_entity_file_path):
        entity_file = open(possible_entity_file_path,"r")
        entity_str_data = entity_file.read()
        entity_file.close()
        entity_json_data = json.loads(entity_str_data)

        input_file = open(input_file_path,"r")
        str_data = input_file.read()
        input_file.close()
        json_data = json.loads(str_data)

        if "entities" not in json_data[""]:
            json_data[""]["entities"] = []

        new_json_data = set_entities_in_json_data(json_data,entity_json_data)
        
        if json_data[""]["entities"] != new_json_data[""]["entities"]:
            with open(input_file_path, "w") as write_file:
                json.dump(new_json_data, write_file, indent=4)

create_needed_folders()
input_files = get_input_files()
for input_file in input_files:
    new_file_name = get_new_file_name(input_file)
    if input_file.endswith(NBT_EXT):
        command = NBT_TO_JSON_COMMAND.format(input_file,new_file_name)
    
    elif input_file.endswith(JSON_EXT):
        json_data = get_json_data(input_file)
        inject_entyties_if_present(input_file)
        command = JSON_TO_NBT_COMMAND.format(input_file,new_file_name).replace(OUTPUT_FOLDER,'')

    if does_file_exist(new_file_name.replace(OUTPUT_FOLDER,'')):
        os.remove(new_file_name.replace(OUTPUT_FOLDER,''))
    if does_file_exist(new_file_name):
        os.remove(new_file_name)
    
    os.system(command)
    if does_file_exist(new_file_name.replace(OUTPUT_FOLDER,'')):
        shutil.move(new_file_name.replace(OUTPUT_FOLDER,''),new_file_name)

