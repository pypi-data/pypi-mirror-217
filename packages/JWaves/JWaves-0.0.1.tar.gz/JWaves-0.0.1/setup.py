from setuptools import setup
import setuptools
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(_here, 'README.md')) as f:
    long_description = f.read()



installFolder = os.path.abspath(os.path.join(os.path.split(setuptools.__file__)[0],'..'))
pythonPath =  os.path.relpath(os.path.join(installFolder,'MJOLNIR'),sys.base_prefix)

setup(
    name='JWaves',
    version='0.0.1',
    description=('Random Phase Approximation for Spin Waves and Dispersive Crystal Electric Fields'),
    long_description=long_description,
    author='Jakob Lass',
    author_email='lass.jakob@gmail.com',
    #url='https://github.com/jakob-lass/MJOLNIR',
    license='MPL-2.0',
    data_files = [(pythonPath, ["LICENSE.txt"])],
    python_requires='>=3.5',
    install_requires=['matplotlib>=3','numpy>=1.14'], # ,'ufit','sip','PyQt5-sip','PyQt5<=5.12'
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Visualization',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'],
    )
