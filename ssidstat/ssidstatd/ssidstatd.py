#!/usr/bin/env python2

import monitor
import argparse

__DEFAULT_INTERVAL  = 10
__DEFAULT_PID_FILE  = '/var/lib/ssidstat/ssidstatd.pid'
__DEFAULT_OUT_FILE  = '/var/lib/ssidstat/ssidstatd.out'
__DEFAULT_ERR_FILE  = '/var/lib/ssidstat/ssidstatd.err'
__DEFAULT_DB_FILE   = '/var/lib/ssidstat/ssidstatd.db'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--pidfile", help="pidfile, default is {}".format(__DEFAULT_PID_FILE), default=__DEFAULT_PID_FILE)
	parser.add_argument("--db", help="database file, default is {}".format(__DEFAULT_DB_FILE), default=__DEFAULT_DB_FILE)
	parser.add_argument("--outlog", help="standard output file, default is {}".format(__DEFAULT_OUT_FILE), default=__DEFAULT_OUT_FILE)
	parser.add_argument("--errlog", help="standard error file, default is {}".format(__DEFAULT_ERR_FILE), default=__DEFAULT_ERR_FILE)
	parser.add_argument("--interval", help="polling interval (secs), default is {} seconds".format(__DEFAULT_INTERVAL), default=__DEFAULT_INTERVAL)
	parser.add_argument("--status", action="store_true", help="check whether ssidstat daemon is running or not")
	parser.add_argument("--stop", action="store_true", help="stop running ssidstat daemon")
	parser.add_argument("--restart", action="store_true", help="restart running ssidstat daemon")

	opts = parser.parse_args()
	monitord = monitor.MonitorDaemon(opts.db, opts.pidfile, opts.interval, stdout=opts.outlog, stderr=opts.errlog)

	if opts.status:
		if monitord.is_running():
			print 'ssidstat daemon is running'
		else:
			print 'ssidstat daemon is not running'

		return

	if opts.stop:
		monitord.stop()
	elif opts.restart:
		monitord.restart()
	else:
		monitord.start()

if __name__ == '__main__':
	main()
