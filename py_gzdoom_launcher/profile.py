import os
import shutil
from py_gzdoom_launcher import variables

class Profile:
    def __init__(self, **kwargs):
        self.name         = ''
        self.iwad         = ''
        self.wads         = ''
        self.config_file  = ''
        self.dmflags      = None
        self.dmflags2     = None

        for key, val in kwargs.items():
            if key == 'name'       : self.name = val
            if key == 'iwad'       : self.iwad = val
            if key == 'wads'       : self.wads = val       
            if key == 'dmflags'    : self.dmflags = val    
            if key == 'dmflags2'   : self.dmflags2 = val   
            if key == 'config_file': self.config_file = val

    def dict(self):
        return {
                'name'        : self.name,
                'iwad'        : self.iwad,
                'wads'        : self.wads,
                'dmflags'     : self.dmflags,
                'dmflags2'    : self.dmflags2,
                'config_file' : self.config_file
                }

    @classmethod
    def default(cls):
        kwargs = {
                'name'        : 'default',
                'iwad'        : variables.variables['default_iwad'],
                'wads'        : '',
                'config_file' : variables.variables['configuration_file'],
                'dmflags'     : 0,
                'dmflags2'    : 0
                }
        profile = cls(**kwargs)

        return profile

    @classmethod
    def from_file(cls, filename):
        kwargs = {}
        read_file = open(filename, 'r')
        profile_dict = eval(read_file.read())
        return cls(**profile_dict)

    @classmethod
    def from_name(cls, profile_name):
        filename = os.path.join(variables.variables['profile_dir'], profile_name + '.gzd')
        return cls.from_file(filename)

    def get_info(self):
        info = ''
        info += '{:20}{}\n'.format('Profile name:', self.name)
        info += '{:20}{}\n'.format('IWAD:', self.iwad)
        nwads = len(self.wads)
        if nwads:
            info += ('{:20}' + '{}, '*(nwads - 1)  + '{}' + '\n').format('WADs:', *self.wads)
        else:
            info += ('{:20}\n').format('WADs:')
        info += '{:20}{}\n'.format('Configuration file:', self.config_file)
        info += '{:20}{}\n'.format('dmflags:',self.dmflags)
        info += '{:20}{}\n'.format('dmflags2:',self.dmflags2)

        return info

    def save(self, filename):
        print(self.dict(), file = open(filename, 'w'))

    def copy(self, new_name, copy_config = False):
        profile2 = Profile()

        profile2.name = new_name
        profile2.iwad = self.iwad       
        profile2.wads = self.wads       
        profile2.config_file = os.path.join(variables.variables['config_dir'], new_name + '.ini')
        profile2.dmflags = self.dmflags    
        profile2.dmflags2 = self.dmflags2   

        if copy_config:
            shutil.copyfile(
                    os.path.join(variables.variables['config_dir'], self.name + '.ini'),
                    os.path.join(variables.variables['config_dir'], new_name  + '.ini')
            )

        profile2.save(os.path.join(variables.variables['profile_dir'], new_name + '.gzd'))
