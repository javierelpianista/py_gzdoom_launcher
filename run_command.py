import os 
import re

def get_list_of_wad_files(wad_dirs):
    filelist = [item for wad_dir in wad_dirs.split(':') for item in os.listdir(wad_dir)]

    regex = re.compile(r'.*\.wad', re.IGNORECASE)
    selected_files = list(filter(regex.match, filelist))

    return selected_files

def get_list_of_pk3_files(wad_dirs):
    filelist = [item for wad_dir in wad_dirs.split(':') for item in os.listdir(wad_dir)]

    regex = re.compile(r'.*\.pk3', re.IGNORECASE)
    selected_files = list(filter(regex.match, filelist))

    return selected_files
