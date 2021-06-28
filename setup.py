from setuptools import setup
setup(
    name='bembed',
    version='0.0.1',
    description='Better Embed handling for discord.py',
    py_modules=['bembed', 'log_guilds'],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python 3.9',
        'Operating System :: OS Independant',
    ],
    install_requires = [
        'discord == 1.0.1',
        'discord.py ~= 1.7'
    ]
    )
