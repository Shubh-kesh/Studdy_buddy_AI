from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="studdy_buddy",
    version="0.1",
    author="shubhansh kesharwani",
    packages=find_packages(),
    install_requires = requirements,
)