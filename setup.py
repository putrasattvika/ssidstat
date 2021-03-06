#!/usr/bin/env python

from setuptools import setup

# set version
execfile('ssidstat/version.py')

# setup
setup(
	name				= 'ssidstat',
	version				= __version__,
	description			= 'Simple per-SSID bandwidth usage monitor',
	author				= 'Putra Sattvika',
	author_email		= 'sattvikaputra@gmail.com',
	packages			= [
							'ssidstat',
							'ssidstat.common',
							'ssidstat.common.models',
							'ssidstat.ssidstatcli',
							'ssidstat.ssidstatd'
						  ],
	scripts				= ['scripts/ssidstat', 'scripts/ssidstatd'],
	install_requires	= ['tabulate']
)
