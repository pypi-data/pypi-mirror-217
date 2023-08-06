from setuptools import setup

setup(
    name='pyconcurrent',
    version='0.1.0',
    description='A secure python library for parallelizing tasks across several CPU cores',
    author='Anish Kanthamneni',
    author_email='akneni@gmail.com',
    install_requires=[
        'joblib',
    ],
)
