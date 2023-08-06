from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))


VERSION = '0.0.1'
DESCRIPTION = 'WordPress Usernames Enumerator'


# Setting up
setup(
    name="WPNames",
    version=VERSION,
    author="CyberTitus",
    author_email="<cybertitus@proton.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'WordPress', 'WPScan', 'WP', 'WordPress-Usernames', 'Usernames', 'Cyber-Security'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)