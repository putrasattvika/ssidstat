#!/usr/bin/env python2

import sys
import json
import argparse
import tabulate
import ssidstat

import output
from ssidstat.common import db
from ssidstat.common import sysutils

__DEFAULT_DB_FILE   = '/var/lib/ssidstat/ssidstatd.db'

def main():
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument("--help", action='help', help='print this fabulous help message')
	parser.add_argument("--version", "-v", action="store_true", help="show ssidstat version")
	parser.add_argument("--json", "-j", action="store_true", help="output as json")
	parser.add_argument("--active", "-a", action="store_true", help="only outputs active connection")
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

		stats = None
		filter_criteria = None
		stat_formatter = None
		formatter_params = None
		output_func = None

		if opts.active:
			active_conns = sysutils.get_adapters_ssid()
			filter_criteria = []

			for adapter in active_conns:
				filter_criteria.append( (adapter, active_conns[adapter]) )

		if opts.json:
			output_func = output.json_output
		else:
			output_func = output.tabular_output

		if opts.hour:
			stats = ssidstat_db.query_last_24_hours(opts.ssid)
			stat_formatter = output.hourly
			formatter_params = (opts.ssid,)
		elif opts.day:
			stats = ssidstat_db.query_last_30_days(opts.ssid)
			stat_formatter = output.daily
			formatter_params = (opts.ssid,)
		elif opts.week:
			stats = ssidstat_db.query_last_12_weeks(opts.ssid)
			stat_formatter = output.weekly
			formatter_params = (opts.ssid,)
		elif opts.month:
			stats = ssidstat_db.query_last_12_months(opts.ssid)
			stat_formatter = output.monthly
			formatter_params = (opts.ssid,)
		else:
			stats = ssidstat_db.query_all_ssid_stat()
			stat_formatter = output.default
			formatter_params = ()

		stats = output.filter(stats, adapter_ssid_pairs=filter_criteria)
		formatter_params = formatter_params + (stats,)
		formatted_stats = stat_formatter(*formatter_params)

		print output_func(formatted_stats)
	except Exception as e:
		print 'Error: {}'.format(e.message)
		sys.exit(1)

if __name__ == '__main__':
	main()
