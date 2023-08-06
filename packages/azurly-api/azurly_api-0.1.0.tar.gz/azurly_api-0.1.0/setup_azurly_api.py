from setuptools import setup, find_packages

setup(
    name='azurly_api',
    version='0.1.0',
    package_dir={'': 'packages'},
    packages=find_packages(where='packages', include=['azurly_api']),
    install_requires=[
    ],
)
