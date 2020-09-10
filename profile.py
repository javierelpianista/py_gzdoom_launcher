from variables import default_config_filename

class Profile:
    def __init__(self, **kwargs):
        self.iwad         = ''
        self.wads         = ''
        self.config_file  = ''
        self.dmflags      = None
        self.dmflags2     = None

        for key, val in kwargs.items():
            if key == 'iwad'       : self.iwad = val
            if key == 'wads'       : self.wads = val       
            if key == 'dmflags'    : self.dmflags = val    
            if key == 'dmflags2'   : self.dmflags2 = val   
            if key == 'config_file': self.config_file = val

    @classmethod
    def default(cls):
        kwargs = {
                'iwad'        : 'doom2',
                'wads'        : '',
                'config_file' : default_config_filename,
                'dmflags'     : 0,
                'dmflags2'    : 0
                }
        profile = Profile(**kwargs)

        return profile

    @classmethod
    def from_file(cls, filename):
        kwargs = {}
        read_file = open(filename, 'r')

        for line in read_file.readlines():
            data = line.strip().split(':')
            if data[0].strip() == 'IWAD'              : kwargs['iwad']        = data[1].strip()
            if data[0].strip() == 'WADs'              : kwargs['wads']        = [x.strip() for x in data[1].split(',')]
            if data[0].strip() == 'dmflags'           : kwargs['dmflags']     = data[1].strip()
            if data[0].strip() == 'dmflags2'          : kwargs['dmflags2']    = data[1].strip()
            if data[0].strip() == 'Configuration file': kwargs['config_file'] = data[1].strip()

        profile = Profile(**kwargs)

        return profile

    def get_info(self):
        info = ''
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
        info = self.get_info()

        open(filename, 'w').write(self.get_info())


    #command = 'gzdoom' 
    #for wad in selected_wads_list:
    #    command += ' -file {}'.format(wad)

    #iwad_name = selected_iwads_list[0]
    #command += ' -iwad {}'.format(iwad_name)

    #config_filename = config_file_entry.get()
    #command += ' -config {}'.format(config_filename)

    #print('Running gzdoom with the following command...')
    #print(command)
    #os.system(command)
