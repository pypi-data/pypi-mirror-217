from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='flask_project_builder-python',
    version='0.0.1',
    license='MIT License',
    author='Carlos Eduardo Ferreia Fernandes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='carloseduardo082005@icloud.com',
    keywords='flask project builder',
    description=u'Projeto para facilitar a criação de projetos Flask',
    packages=['flask_project_builder'],)