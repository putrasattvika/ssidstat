import time
from datetime import datetime

from ssid_traffic_history import SSIDTrafficHistory

_DAILY_LIMIT_SECS = 3600*24*400

class DailyTrafficHistory(SSIDTrafficHistory):
	def __init__(self, dbfile, table_name):
		super(DailyTrafficHistory, self).__init__(dbfile, table_name, _DAILY_LIMIT_SECS)

	def truncate_time(self, timestamp):
		return int(timestamp/(24*3600))*(24*3600)

	def query_last_30_days(self, ssid, timestamp=None):
		if not timestamp:
			timestamp = time.time()

		with self.db_cursor() as c:
			query = '''
				SELECT timestamp, ssid, sum(rx), sum(tx)
				FROM {}
				WHERE ssid = ?
				GROUP BY timestamp
				ORDER BY timestamp ASC
				LIMIT 30
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
