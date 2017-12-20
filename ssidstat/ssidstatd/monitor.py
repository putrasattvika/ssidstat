import time
import daemon
 
from ssidstat.common import db
from ssidstat.common import sysutils

class MonitorDaemon(daemon.Daemon):
	def __init__(self, dbfile, pidfile, interval=10, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		daemon.Daemon.__init__(self, pidfile, stdin=stdin, stdout=stdout, stderr=stderr)

		self.dbfile = dbfile
		self.boot_id = sysutils.get_boot_id()
		self.interval = interval

	def run(self):
		self.db = db.SSIDStatDB(self.dbfile)

		while True:
			self.monitor()
			time.sleep(self.interval)

	def monitor(self):
		adapters_ssid = sysutils.get_adapters_ssid()
		adapters_stat = sysutils.get_adapters_traffic()

		for adapter in adapters_ssid:
			ssid = adapters_ssid[adapter]

			recorded_adapter_usage = self.db.query_boot_traffic_history(self.boot_id, adapter)

			if not recorded_adapter_usage:
				self.db.clear_boot_traffic_history(adapter)

				recorded_adapter_usage = {
					'boot_id': self.boot_id,
					'adapter': adapter,
					'rx': 0,
					'tx': 0
				}

			delta_rx = adapters_stat[adapter]['rx'] - recorded_adapter_usage['rx']
			delta_tx = adapters_stat[adapter]['tx'] - recorded_adapter_usage['tx']

			self.db.update_boot_traffic_history(
				self.boot_id, adapter, 
				adapters_stat[adapter]['rx'],
				adapters_stat[adapter]['tx']
			)

			self.db.add_ssid_traffic_history(adapter, ssid, delta_rx, delta_tx)
