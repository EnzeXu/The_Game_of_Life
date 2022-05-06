from setuptools import setup

APP = ['run.py']
DATA_FILES = [
    ('image/', ['image/leaf.ico', 'image/background4.png', 'image/empty.png', 'image/gol.png', 'image/tmp.png']),
    ('font/', ['font/times.ttf', 'font/DancingScript-Regular.otf'])
]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'image/leaf.ico'
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

