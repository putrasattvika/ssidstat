#!/usr/bin/env python2

import sys
import argparse
import tabulate
import ssidstat

from ssidstat.common import db

__DEFAULT_DB_FILE   = '/var/lib/ssidstat/ssidstatd.db'

def byte_format(size):
	prefixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB']

	result = '{:.2f} {}'.format(size, prefixes[0])
	for i in xrange(len(prefixes)):
		if size/(2.0**(10*i)) >= 1:
			result = '{:.2f} {}'.format(size/(2.0**(10*i)), prefixes[i])
		else:
			break

	return result

def output(stats):
	headers = ['Adapter', 'SSID', 'Receive (rx)', 'Transmit (tx)', 'Total']
	table = []

	for adapter in stats:
		for ssid_stat in stats[adapter]:
			table.append([
				adapter,
				ssid_stat['ssid'],
				byte_format(ssid_stat['rx']),
				byte_format(ssid_stat['tx']),
				byte_format(ssid_stat['rx'] + ssid_stat['tx'])
			])

	print tabulate.tabulate(table, headers=headers)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--version", action="store_true", help="show ssidstat version")
	parser.add_argument("--db", help="database file, default is {}".format(__DEFAULT_DB_FILE), default=__DEFAULT_DB_FILE)
	parser.add_argument("--interface", "-i", help="select one specific interface", default="all")

	opts = parser.parse_args()

	if opts.version:
		print 'SSIDStat/SSIDStatd v{}'.format(ssidstat.__version__)
		return

	try:
		ssidstat_db = db.SSIDStatDB(opts.db)
		output(ssidstat_db.query_all_ssid_stat())
	except Exception as e:
		print 'Error on opening DB file {}: {}'.format(opts.db, e.message)
		sys.exit(1)

if __name__ == '__main__':
	main()
