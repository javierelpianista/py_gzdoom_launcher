import os 
import re
import glob
from variables import iwad_names, profile_dir

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

def backup_profile(profile_name):
    profile_filename = profile_name + '.gzd'
    bak_filename = '.' + profile_filename + '.bak'
    bak_filename_numbered = bak_filename
    n = 0
    while os.path.exists(os.path.join(profile_dir, bak_filename_numbered)):
        n+=1
        bak_filename_numbered = bak_filename + '.' + str(n)

    os.rename(
            os.path.join(profile_dir, profile_name + '.gzd'), 
            os.path.join(profile_dir, bak_filename_numbered)
            )

def detect_profiles():
    profile_filenames = glob.glob(os.path.join(profile_dir, '*.gzd'))
    profile_names = sorted([os.path.splitext(os.path.basename(filename))[0] for filename in profile_filenames])

    return profile_names

