import os
import os.path

iwad_names = ['doom', 'doom2', 'plutonia', 'tnt', 'heretic', 'hexen', 'harmony', 'hedon']

if os.name == 'nt':
    main_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'py_gzdoom_launcher')
else:
    main_dir = os.path.join(os.path.expanduser('~'), '.py_gzdoom_launcher')

variables = {
        'configuration_file' : os.path.join(main_dir, 'py_gzdoom_launcher.cfg'),
        'set' : False
        }

def set_defaults():
    global variables

    variables['main_dir'] = main_dir
    variables['profile_dir'] = os.path.join(main_dir, 'profiles')
    variables['config_dir'] = os.path.join(main_dir, 'config')

    if os.name == 'nt':
        variables['wad_dirs'] = ''
        variables['iwad_dir'] = ''
        variables['executable'] = ''
    else:
        variables['wad_dirs'] = '/usr/share/games/doom'
        variables['iwad_dir'] = '/usr/share/games/doom'
        variables['executable'] = '/usr/bin/gzdoom'

    variables['default_iwad'] = 'DOOM2.WAD'
    variables['set'] = True

def read_config(filename):
    global variables

    read_file = open(filename, 'r')
    variables = eval(read_file.read())
    variables['set'] = True

def write_config(filename = None):
    global variables

    if not filename:
        save_filename = variables['configuration_file']
    else:
        save_filename = filename

    os.makedirs(os.path.dirname(save_filename), exist_ok = True)
    write_file = open(save_filename, 'w')
    print(variables, file = write_file)
