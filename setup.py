from setuptools import setup

setup(name='pghost',
	version='1.0',
	description='Help you to migrate Pelican\'s posts and tags to Ghost Edit Add topics',
	keywords='blog pelican ghost migrate json',
	url='https://github.com/ken8203/pghost',
	download_url='https://github.com/ken8203/pghost/archive/1.0.tar.gz',
	author='Jay Chung',
	author_email='ken8203@gmail.com',
	scripts=['bin/pghost'],
	packages=['pghost'],
	include_package_data=True,
	zip_safe=False,
	license='Apache2')
