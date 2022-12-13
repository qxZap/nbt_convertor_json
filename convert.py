import os
import shutil

INPUT_FOLDER = "input/"
OUTPUT_FOLDER = "output/"

NBT_EXT = ".nbt"
JSON_EXT = ".json"
TEMP_FILE = "tmp.tmp"

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

NBT_TO_JSON_COMMAND = "nbt -r {} --pretty --json > {}"
JSON_TO_NBT_COMMAND = "nbt -s {} -w {}"

input_files = get_input_files()
for input_file in input_files:
    new_file_name = get_new_file_name(input_file)
    if input_file.endswith(NBT_EXT):
        command = NBT_TO_JSON_COMMAND.format(input_file,new_file_name)
    elif input_file.endswith(JSON_EXT):
        command = JSON_TO_NBT_COMMAND.format(input_file,new_file_name).replace(OUTPUT_FOLDER,'')
    os.system(command)
    # shutil.move(new_file_name.replace(OUTPUT_FOLDER,''),new_file_name)

