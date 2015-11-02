import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bitgo'))
import version

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = ['requests==2.7.0', 'lxml==3.4.4']

setup(
    name='BitGoPY',
    version=version.VERSION,
    description='BitGo Unnofficial API Client Library for Python',
    author='Erik Dominguez',
    author_email='erik.dominguez1003@gmail.com',
    url='https://bitgo.com/',
    packages=['bitgo'],
    package_data={'bitgo': ['../VERSION']},
    install_requires=install_requires,
    test_suite='test'
)
