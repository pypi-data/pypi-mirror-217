from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='cep-range',
    version='0.0.1',
    license='MIT License',
    author='Gabriel Gontijo',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='gontijogabr@gmail.com',
    keywords='cep coordenadas geograficas enderecos postalcode address',
    description=u'',
    packages=['cep_range'],
    install_requires=['geopy', 'selenium'],)
