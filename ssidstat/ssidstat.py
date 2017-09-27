#!/usr/bin/env python2

import db
import sys
import argparse
import tabulate

__DEFAULT_DB_FILE   = '/var/lib/ssidstat/ssidstatd.db'

def byte_format(size):
	size *= 1024
	prefixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB']

	result = ''
	for i in xrange(len(prefixes)):
		if size/(2.0**(10*i)) >= 1:
			result = '{:.2f} {}'.format(size/(2.0**(10*i)), prefixes[i])
		else:
			break

	return result

def output(stats):
	headers = ['SSID', 'Receive (rx)', 'Transmit (tx)', 'Total']
	table = [[ssid, byte_format(stats[ssid]['rx']), byte_format(stats[ssid]['tx']), 
				byte_format(stats[ssid]['rx'] + stats[ssid]['tx'])] for ssid in stats]

	print tabulate.tabulate(table, headers=headers)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--db", help="database file, default is {}".format(__DEFAULT_DB_FILE), default=__DEFAULT_DB_FILE)
	parser.add_argument("--interface", "-i", help="select one specific interface", default="all")

	opts = parser.parse_args()

	try:
		ssidstat_db = db.SSIDStatDB(opts.db)
		output(ssidstat_db.query_all_ssid_stat())
	except:
		print 'Error opening DB file {}'.format(opts.db)
		sys.exit(1)

if __name__ == '__main__':
	main()
