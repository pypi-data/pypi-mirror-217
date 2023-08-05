from setuptools import setup

setup(
    name='catplayer',
    version='0.1.0',
    description='MP4 player using moviepy and pygame',
    py_modules=['catplayer'],
    install_requires=['moviepy', 'pygame'],
    entry_points={
        'console_scripts': [
            'catplayer = catplayer:main'
        ]
    },
)

