import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0'
PACKAGE_NAME = 'nombres' #Debe coincidir con el nombre de la carpeta 
AUTHOR = 'ItzelFranco' #Modificar con vuestros datos
AUTHOR_EMAIL = 'itzel_fd1@tesch.edu.mx' #Modificar con vuestros datos
URL = 'https://github.com/itzelfd98' #Modificar con vuestros datos

LICENSE = 'GNU GPL' #Tipo de licencia
DESCRIPTION = 'Library to obtain names of Spanish men and women as well as surnames'

#Paquetes necesarios para que funcione la libreía. Se instalarán a la vez si no lo tuvieras ya instalado
INSTALL_REQUIRES = [
    'pandas'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
