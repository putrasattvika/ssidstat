import time

import daemon
import sysutils
 
from ssidstat.common import db

class MonitorDaemon(daemon.Daemon):
	def __init__(self, dbfile, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		daemon.Daemon.__init__(self, pidfile, stdin=stdin, stdout=stdout, stderr=stderr)

		self.dbfile = dbfile

	def run(self):
		self.db = db.SSIDStatDB(self.dbfile)

		while True:
			self.monitor()

			time.sleep(30)

	def monitor(self):
		adapters = sysutils.get_adapters_ssid()

		for adapter in adapters:
			ssid = adapters[adapter]
			
			vnstat_adapter_usage = sysutils.get_todays_traffic(adapter)

			if vnstat_adapter_usage == None:
				continue

			recorded_adapter_usage = self.db.query_adapter_stat(adapter)
			recorded_ssid_usage = self.db.query_ssid_stat(ssid)

			delta_rx = vnstat_adapter_usage['rx'] - recorded_adapter_usage['rx']
			delta_tx = vnstat_adapter_usage['tx'] - recorded_adapter_usage['tx']

			new_rx = recorded_ssid_usage['rx'] + delta_rx
			new_tx = recorded_ssid_usage['tx'] + delta_tx

			self.db.update_db(adapter, ssid, new_rx, new_tx)