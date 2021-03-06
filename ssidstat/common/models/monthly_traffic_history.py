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

	def query_last_12_months(self, ssid, timestamp=None):
		if not timestamp:
			timestamp = time.time()

		with self.db_cursor() as c:
			query = '''
				SELECT timestamp, ssid, sum(rx), sum(tx)
				FROM {}
				WHERE ssid = ?
				GROUP BY timestamp
				ORDER BY timestamp ASC
				LIMIT 12
			'''.format(self.table_name)

			c.execute(query, (ssid, ))
			query_results = c.fetchall()

		results = []
		for r in query_results:
			ts, ssid, rx, tx = r

			results.append({
				'timestamp': ts,
				'ssid': ssid,
				'rx': rx,
				'tx': tx
			})

		return results
