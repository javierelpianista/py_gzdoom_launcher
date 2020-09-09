import os 
import re
from variables import iwad_names

def get_list_of_wad_files(wad_dirs):
    filelist = [item for wad_dir in wad_dirs.split(':') for item in os.listdir(wad_dir)]

    regex = re.compile(r'.*\.wad', re.IGNORECASE)
    selected_files = list(filter(regex.match, filelist))

    wad_files  = []
    iwad_files = []
    for n, filename in enumerate(selected_files):
        lc_filename = filename.lower().replace('.wad', '')

        if lc_filename in iwad_names:
            iwad_files.append(filename)
        else:
            wad_files.append(filename)

    return wad_files, iwad_files

def get_list_of_pk3_files(wad_dirs):
    filelist = [item for wad_dir in wad_dirs.split(':') for item in os.listdir(wad_dir)]

    regex = re.compile(r'.*\.pk3', re.IGNORECASE)
    selected_files = list(filter(regex.match, filelist))

    return selected_files
