#!/usr/bin/env python2

import monitor
import argparse

__DEFAULT_PID_FILE  = '/var/lib/ssidstat/ssidstatd.pid'
__DEFAULT_DB_FILE   = '/var/lib/ssidstat/ssidstatd.db'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--pidfile", help="pidfile, default is {}".format(__DEFAULT_PID_FILE), default=__DEFAULT_PID_FILE)
	parser.add_argument("--db", help="database file, default is {}".format(__DEFAULT_DB_FILE), default=__DEFAULT_DB_FILE)
	parser.add_argument("--status", action="store_true", help="check whether ssidstat daemon is running or not")
	parser.add_argument("--stop", action="store_true", help="stop running ssidstat daemon")
	parser.add_argument("--restart", action="store_true", help="restart running ssidstat daemon")

	opts = parser.parse_args()
	monitord = monitor.MonitorDaemon(opts.db, opts.pidfile, stdout='/var/lib/ssidstat/ssidstatd.out', stderr='/var/lib/ssidstat/ssidstatd.err')

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
