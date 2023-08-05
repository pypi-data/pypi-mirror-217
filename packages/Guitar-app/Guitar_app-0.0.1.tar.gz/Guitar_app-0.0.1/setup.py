from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))



VERSION = '0.0.1'
DESCRIPTION = 'Guitar_app For learning guitar notes/fretboard'


# Setting up
setup(
    name="Guitar_app",
    version=VERSION,
    author="cliveapple265",
    author_email="<cliveapple265@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['playsound~=1.2.2'],
    keywords=['python',],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)