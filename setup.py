from setuptools import setup
from os.path import join, dirname

execfile(join(dirname(__file__), 'OracleLibrary', 'version.py'))


setup(
    name='robotframework-OracleLibrary',
    version=VERSION,
    author='Jules Barnes',
    author_email='jules@julesbarnes.com',
    packages=['OracleLibrary'],
    url='https://code.google.com/p/robotframework-OracleLibrary/',
    license='LICENSE.txt',
    description='Robot Framework Library to run sql queries against and Oracle DB',
    long_description=open('README.txt').read(),
    install_requires=[
                      'robotframework >= 2.8.3',
                      'cx_Oracle >= 5.1.2',
                      ],
)