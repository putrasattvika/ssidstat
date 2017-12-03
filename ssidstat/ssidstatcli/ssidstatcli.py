#!/usr/bin/env python2

import sys
import argparse
import tabulate
import ssidstat

import output
from ssidstat.common import db

__DEFAULT_DB_FILE   = '/var/lib/ssidstat/ssidstatd.db'

def main():
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument("--help", action='help', help='print this fabulous help message')
	parser.add_argument("-v", "--version", action="store_true", help="show ssidstat version")
	parser.add_argument("--db", help="database file, default is {}".format(__DEFAULT_DB_FILE), default=__DEFAULT_DB_FILE)
	parser.add_argument("--ssid", "-s", help="select one specific SSID. Used in conjuction with -h, -d, -w, or -m")
	parser.add_argument("--hour", "-h", action="store_true", help="show hourly statistics")
	parser.add_argument("--day", "-d", action="store_true", help="show daily statistics")
	parser.add_argument("--week", "-w", action="store_true", help="show weekly statistics")
	parser.add_argument("--month", "-m", action="store_true", help="show monthly statistics")

	opts = parser.parse_args()

	if opts.version:
		print 'SSIDStat/SSIDStatd v{}'.format(ssidstat.__version__)
		return

	try:
		ssidstat_db = db.SSIDStatDB(opts.db)

		if not opts.ssid and (opts.hour or opts.day or opts.week or opts.month):
			raise Exception('parameter --ssid not defined')

		if opts.hour:
			print output.hourly(opts.ssid, ssidstat_db.query_last_24_hours(opts.ssid))
		elif opts.day:
			print output.daily(opts.ssid, ssidstat_db.query_last_30_days(opts.ssid))
		elif opts.week:
			print output.weekly(opts.ssid, ssidstat_db.query_last_12_weeks(opts.ssid))
		elif opts.month:
			print output.monthly(opts.ssid, ssidstat_db.query_last_12_months(opts.ssid))
		else:
			print output.default(ssidstat_db.query_all_ssid_stat())
	except Exception as e:
		print 'Error: {}'.format(e.message)
		sys.exit(1)

if __name__ == '__main__':
	main()
