from ssid_traffic_history import SSIDTrafficHistory

_HOURLY_LIMIT_SECS = 3600*24*40

class HourlyTrafficHistory(SSIDTrafficHistory):
	def __init__(self, dbfile, table_name):
		super(HourlyTrafficHistory, self).__init__(dbfile, table_name, _HOURLY_LIMIT_SECS)

	def truncate_time(self, timestamp):
		return int(timestamp/3600)*3600
