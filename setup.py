from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="AI-AGENT",
    version="0.0.1",
    author="Nasim",
    packages=find_packages(),
    install_requires=requirements
)