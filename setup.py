from distutils.core import setup

setup(
    name='home_backup',
    version='2.0',
    packages=['home_backup'],
    url='http://zufallsheld.de/2013/09/29/python-backup-script-with-rsync/',
    license='GPL 3.0',
    author='René Pascal Laub',
    author_email='dev@pascal-laub-de',
    description='advanced rsync backup script written in python',
    long_description=open('README.md').read()
)
