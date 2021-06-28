from setuptools import setup
setup(
    name='bembed',
    version='0.0.1',
    description='Better Embed handling for discord.py',
    py_modules=['bembed', 'log_guilds'],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independant',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'Topic :: Multimedia',
        'Topic :: Software Development',
    ],
    install_requires = [
        'discord == 1.0.1',
        'discord.py ~= 1.7'
    ]
    )
