from setuptools import setup, find_packages

setup(
    name="cors-finder",
    version= '1.0.0',
    author= 'Hariharan',
    description= 'The cors-finder package is used to find the vulnerable CORS domains',
    keywords= ['cors', 'cors-finder', 'cors misconfiguration', 'cors exploit', 'cors vulnerability'],
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
    ],
)