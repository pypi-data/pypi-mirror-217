from setuptools import setup, find_packages

setup(
    name='data_merge',
    version='0.1.1',
    description='Python package for merging Excel and CSV files',
    author='Ojo Ilesanmi',
    author_email='ojoilesanmi89@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pytest'
    ],
)
