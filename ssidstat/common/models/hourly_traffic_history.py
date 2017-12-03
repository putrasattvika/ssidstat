import time
from datetime import datetime

from ssid_traffic_history import SSIDTrafficHistory

_HOURLY_LIMIT_SECS = 3600*24*40

class HourlyTrafficHistory(SSIDTrafficHistory):
	def __init__(self, dbfile, table_name):
		super(HourlyTrafficHistory, self).__init__(dbfile, table_name, _HOURLY_LIMIT_SECS)

	def truncate_time(self, timestamp):
		return int(timestamp/3600)*3600

	def truncate_time_day(self, timestamp):
		return int(timestamp/(24*3600))*(24*3600)

	def truncate_time_week(self, timestamp):
		dt_week = datetime.strptime(datetime.strftime(datetime.fromtimestamp(time.time()), '%Y-%W-1'), '%Y-%W-%w')
		return int((dt_week - datetime.fromtimestamp(0)).total_seconds())

	def query_last_24_hours(self, ssid, timestamp=None):
		if not timestamp:
			timestamp = time.time()

		with self.db_cursor() as c:
			query = '''
				SELECT timestamp, ssid, sum(rx), sum(tx)
				FROM {}
				WHERE 
					timestamp >= ? AND
					ssid = ?
				GROUP BY timestamp
				ORDER BY timestamp ASC
			'''.format(self.table_name)

			c.execute(query, (self.truncate_time_day(timestamp), ssid))
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

	# def query_last_4_weeks(self, ssid, timestamp=None):
	# 	if not timestamp:
	# 		timestamp = time.time()

	# 	start_of_this_week = self.truncate_time_week(timestamp)

	# 	query_results = []
	# 	for i in xrange(0, 4):
	# 		start_of_week = start_of_this_week - i*(7*24*3600)
	# 		start_of_next_week = start_of_week + (7*24*3600)

	# 		with self.db_cursor() as c:
	# 			query = '''
	# 				SELECT timestamp, ssid, sum(rx), sum(tx)
	# 				FROM {}
	# 				WHERE 
	# 					timestamp >= ? AND
	# 					timestamp < ? AND
	# 					ssid = ?
	# 			'''.format(self.table_name)

	# 			c.execute(query, (start_of_week, start_of_next_week, ssid))

	# 			res = c.fetchone()
	# 			if res[0]:
	# 				query_results.append((start_of_week, start_of_next_week-1) + res)

	# 	results = []
	# 	for r in query_results:
	# 		start_ts, end_ts, ts, ssid, rx, tx = r

	# 		results.append({
	# 			'start_ts': start_ts,
	# 			'end_ts': end_ts,
	# 			'ssid': ssid,
	# 			'rx': rx,
	# 			'tx': tx
	# 		})

	# 	return results
