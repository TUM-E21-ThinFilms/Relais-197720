import sys

from setuptools import setup, find_packages

requires = []

desc = ('An implementation of the Conrad Relais 197720 card')

setup(
    name='relais',
    version=__import__('relais').__version__,
    author='Alexander Book',
    author_email='alexander.book@frm2.tum.de',
    license = 'GNU General Public License (GPL), Version 3',
    url='https://github.com/TUM-E21-ThinFilms/relais-197720',
    description=desc,
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
