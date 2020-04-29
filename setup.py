
"""
Installation file for python avs module
"""

from setuptools import setup, find_packages
from pathlib import Path

name    = 'avorion-obj-exporter'
module  = 'avorion_obj_exporter'
version = '0.1.0'

requirements = ['appdirs', 'argparse', 'pathlib', 'numpy', 'vtk', 'pyvista']

readme = (Path(__file__).resolve().parent / 'README.md').read_text(encoding='utf-8')

setup(
    name=name,
    version=version,
    description='Avorion ShipXML Exporter based on pyVista/VTK',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https:github.com/jgerst/avorion-obj-exporter',
    author='Janick Gerstenberger',
    entry_points= {
        'console_scripts': [
            f'{name} = {module}.app:main',
            f'aoe = {module}.app:main',
        ],
    },
    keywords='avorion exporter',
    install_requires=requirements,
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 3.7',
        'Topic:: Games/Entertainment',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src')
)
