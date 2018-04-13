import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "blinky-iot",
    version = "0.0.1",
    author = "Jason Walker",
    author_email = "ungood@onetrue.name"
    description = ("An AWS IoT device intended to display information on a Blinky Tape LED strip.")
    keywords = "aws iot blinky",
    url = "http://github.com/ungood/blinky-iot",
    packages=['blinky', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)