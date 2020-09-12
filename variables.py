import os
import os.path

iwad_names = ['doom', 'doom2', 'plutonia', 'tnt', 'heretic', 'hexen', 'harmony', 'hedon']

main_dir = os.path.join(os.path.expanduser('~'), '.py_gzdoom_launcher')
variables = {
        'configuration_file' : os.path.join(main_dir, 'py_gzdoom_launcher.cfg')
        }

def set_defaults(main_dir, config_file):
    global variables

    variables = {
        'main_dir'           : main_dir,
        'profile_dir'        : os.path.join(main_dir, 'profiles'),
        'config_dir'         : os.path.join(main_dir, 'config'),
        'wad_dirs'           : '/usr/share/games/doom',
        'executable'         : '/usr/bin/gzdoom',
        'default_iwad'       : 'DOOM2.WAD'
        }

def read_config(filename):
    global variables

    read_file = open(filename, 'r')
    variables = eval(read_file.read())

def write_config(filename = None):
    global variables

    if not filename:
        save_filename = variables['configuration_file']
    else:
        save_filename = filename

    write_file = open(save_filename, 'w')
    print(variables, file = write_file)
