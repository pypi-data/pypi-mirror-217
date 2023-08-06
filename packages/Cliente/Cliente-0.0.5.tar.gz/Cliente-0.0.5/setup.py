from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

# Lê as dependências do arquivo requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Cliente',
    version='0.0.5',
    description='Módulo que representa a classe Cliente do sistema bancário',
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
)
