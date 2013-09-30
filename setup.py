from distutils.core import setup

setup(
	name='home_backup',
	version='1.0',
	packages=['home_backup'],
	url='http://zufallsheld.de/2013/09/29/python-backup-script-with-rsync/',
	license='GPL 3.0',
	author='Sebastian Gumprich',
	author_email='sebastian.gumprich@38.de',
	description='simple python backup script',
    long_description=open('README.txt').read()
)
