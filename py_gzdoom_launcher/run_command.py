import os 
import re
import glob
from py_gzdoom_launcher import variables

def get_list_of_wad_files(wad_dirs):
    if os.name == 'nt':
        filelist = os.listdir(wad_dirs)
    else:
        filelist = [item for wad_dir in variables.variables['wad_dirs'].split(':') for item in os.listdir(wad_dir)]

    regex = re.compile(r'.*\.wad', re.IGNORECASE)
    selected_files = list(filter(regex.match, filelist))

    wad_files  = []
    iwad_files = []

    for n, filename in enumerate(selected_files):
        lc_filename = filename.lower().replace('.wad', '')

        if lc_filename in variables.iwad_names:
            iwad_files.append(filename)
        else:
            wad_files.append(filename)

    wad_files  = sorted(wad_files)
    iwad_files = sorted(iwad_files)

    return wad_files, iwad_files

def get_list_of_pk3_files(wad_dirs):
    if os.name == 'nt':
        filelist = [wad_dirs]
    else:
        filelist = [item for wad_dir in wad_dirs.split(':') for item in os.listdir(wad_dir)]

    regex = re.compile(r'.*\.pk3', re.IGNORECASE)
    selected_files = list(filter(regex.match, filelist))

    return selected_files

def backup_profile(profile_name):
    profile_filename = profile_name + '.gzd'
    bak_filename = '.' + profile_filename + '.bak'
    bak_filename_numbered = bak_filename
    n = 0
    while os.path.exists(os.path.join(variables.variables['profile_dir'], bak_filename_numbered)):
        n+=1
        bak_filename_numbered = bak_filename + '.' + str(n)

    os.rename(
            os.path.join(variables.variables['profile_dir'], profile_name + '.gzd'), 
            os.path.join(variables.variables['profile_dir'], bak_filename_numbered)
            )

def detect_profiles():
    profile_filenames = glob.glob(os.path.join(variables.variables['profile_dir'], '*.gzd'))
    profile_names = sorted([os.path.splitext(os.path.basename(filename))[0] for filename in profile_filenames])

    return profile_names

def launch_gzdoom(profile):
    command = variables.variables['executable']
    command += ' -iwad {}'.format(profile.iwad)

    for wad in profile.wads:
        command += ' -file {}'.format(os.path.join(variables.variables['wad_dirs'], wad))

    command += ' -config {}'.format(profile.config_file)
    command += ' +set dmflags {} +set dmflags2 {}'.format(profile.dmflags, profile.dmflags2)

    print('Running gzdoom with the following command...')
    print(command)

    os.system(command)
    quit()
