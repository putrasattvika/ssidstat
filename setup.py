#!/usr/bin/env python

from setuptools import setup

setup(
	name				= 'ssidstat',
	version				= '0.1',
	description			= 'Simple per-SSID bandwidth usage monitor',
	author				= 'Putra Sattvika',
	author_email		= 'sattvikaputra@gmail.com',
	packages			= ['ssidstat', 'ssidstat.common', 'ssidstat.ssidstatcli', 'ssidstat.ssidstatd'],
	scripts				= ['scripts/ssidstat', 'scripts/ssidstatd'],
	install_requires	= ['tabulate']
)
