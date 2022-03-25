import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='technical-indicators',
    version='0.1.1',
    author='mniyk',
    author_email='my.name.is.yohei.kono@gmail.com',
    description='technical indicators python library',
    long_description=long_description,
    url='https://github.com/mniyk/technical-indicators.git',
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'six'])
