import time
from datetime import datetime

from ssid_traffic_history import SSIDTrafficHistory

_MONTHLY_LIMIT_SECS = 3600*24*400

class MonthlyTrafficHistory(SSIDTrafficHistory):
	def __init__(self, dbfile, table_name):
		super(MonthlyTrafficHistory, self).__init__(dbfile, table_name, _MONTHLY_LIMIT_SECS)

	def truncate_time(self, timestamp):
		dt_month = datetime.strptime(datetime.strftime(datetime.fromtimestamp(timestamp), '%Y-%m'), '%Y-%m')
		return int((dt_month - datetime.fromtimestamp(0)).total_seconds())
