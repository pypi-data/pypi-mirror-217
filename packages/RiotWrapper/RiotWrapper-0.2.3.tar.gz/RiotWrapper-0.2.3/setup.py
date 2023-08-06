from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='RiotWrapper', version='0.2.3', packages=find_packages(), install_requires=requirements)