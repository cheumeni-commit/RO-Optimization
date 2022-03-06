from setuptools import setup

with open("./README.md") as fp:
    long_description = fp.read()

with open("./requirements.txt") as fp:
    dependencies = [line.strip() for line in fp.readlines()]

setup(
    name="RO-Optimization",
    version="0.2",
    description="Operationnal research",
    long_description=long_description,
    author="cheumeni",
    author_email="cheumenijean@yahoo.fr",
    packages=["src"],
    install_requires=dependencies
)