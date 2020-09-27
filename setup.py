from setuptools import setup, find_packages

setup(
        name     = 'py_gzdoom_launcher',
        version  = '0.0.14',
        entry_points = {
            'gui_scripts' : [
                'pygzdl = py_gzdoom_launcher.main:main'
                ],
            'console_scripts' : [
                'pygzdl-run = py_gzdoom_launcher.main:run_profile'
                ]
            },
        author   = 'Javier Garcia', 
        author_email = 'javier.garcia.tw@hotmail.com',
        description  = 'A simple launcher for GZDoom',
        long_description = open('README.md', 'r').read(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/javierelpianista/py_gzdoom_launcher',
        classifiers = [
            'Programming Language :: Python :: 3',
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)'
            ],
        packages = find_packages()
        )
