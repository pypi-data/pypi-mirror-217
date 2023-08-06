from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="cors-detector",
    version= '1.0.0',
    author= 'Hariharan',
    description= 'The cors-detector package is used to find the vulnerable CORS domains',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords= ['cors', 'cors-finder', 'cors misconfiguration', 'cors exploit', 'cors vulnerability'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cors-detector = lib.cors:main',
        ]
    },
    install_requires=[
        'requests',
        'colorama',
        'getpass',
    ],
    
    
)