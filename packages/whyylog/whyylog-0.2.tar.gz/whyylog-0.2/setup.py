from setuptools import setup, find_packages

VERSION = '0.2' 
DESCRIPTION = 'Prints out a log message to terminal in color'
with open('README.md', 'r') as r:
    LONG_DESCRIPTION = r.read()

# Setting up
setup(
       # the name must match the folder name 'simpleopers'
        name = "whyylog", 
        version = VERSION,
        authors = "iamlrk",
        author_email="<lepakshiramkiran@hotmail.com>",
        url = 'https://github.com/iamlrk/ylog',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        packages=find_packages(),

        keywords=['python', 'logging', 'log', 'print'],
        classifiers= [
            "License :: OSI Approved :: MIT License",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ]
)