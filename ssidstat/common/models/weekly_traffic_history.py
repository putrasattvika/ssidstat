import time
from datetime import datetime

from ssid_traffic_history import SSIDTrafficHistory

_WEEKLY_LIMIT_SECS = 3600*24*400

class WeeklyTrafficHistory(SSIDTrafficHistory):
	def __init__(self, dbfile, table_name):
		super(WeeklyTrafficHistory, self).__init__(dbfile, table_name, _WEEKLY_LIMIT_SECS)

	def truncate_time(self, timestamp):
		dt_week = datetime.strptime(datetime.strftime(datetime.fromtimestamp(time.time()), '%Y-%W-1'), '%Y-%W-%w')
		return int((dt_week - datetime.fromtimestamp(0)).total_seconds())

	def query_last_12_weeks(self, ssid, timestamp=None):
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
