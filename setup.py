import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='kivy_python_checkers',
    version='0.8',
    url='https://github.com/WesBAn/kivy_python_checkers',
    license='MIT License',
    author='mcwesban',
    author_email='wesban1@gmail.com',
    description='Simple checkers game realized with kivy + python3',
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Topic :: Games/Entertainment :: Board Games",
        "Natural Language :: Russian"
    ],
)
