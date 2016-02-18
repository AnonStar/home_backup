from distutils.core import setup

setup(
    name='home_backup',
    version='1.0',
    packages=['home_backup'],
    license='GPL 3.0',
    author='Pascal Laub',
    author_email='anonstar@agsserver.de',
    description='simple python backup script with mail-log option',
    long_description=open('README.md').read()
)
