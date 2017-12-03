import time
import sqlite3

from base_model import BaseModel

from datetime import datetime
from contextlib import contextmanager

class SSIDTrafficHistory(BaseModel):
	def __init__(self, dbfile, table_name, time_limit):
		super(SSIDTrafficHistory, self).__init__(dbfile, table_name)

		self.time_limit = time_limit

	def init_db(self):
		with self.db_cursor() as c:
			c.execute('''
				CREATE TABLE IF NOT EXISTS {} (
					timestamp integer,
					adapter text,
					ssid text,
					rx integer,
					tx integer,
					PRIMARY KEY (timestamp, adapter, ssid)
				)
			'''.format(self.table_name))

	def truncate_time(timestamp):
		raise NotImplementedError

	def query(self, adapter, ssid, timestamp=None):
		if not timestamp:
			timestamp = time.time()

		with self.db_cursor(commit=False) as c:
			query = '''
				SELECT timestamp, adapter, ssid, rx, tx
				FROM {}
				WHERE adapter=? AND ssid=? AND timestamp=?;
			'''.format(self.table_name)

			c.execute(query, (adapter, ssid, self.truncate_time(timestamp)))
			result = c.fetchone()

		if result == None:
			result = (self.truncate_time(timestamp), adapter, ssid, 0, 0)

		return {
			'timestamp': self.truncate_time(timestamp),
			'adapter': adapter,
			'ssid': ssid,
			'rx': result[3],
			'tx': result[4]
		}

	def query_all(self, start_time=None, end_time=None, timestamp=None):
		if not timestamp:
			timestamp = time.time()

		if not end_time:
			end_time = timestamp

		if not start_time:
			start_time = self.truncate_time(end_time)

		with self.db_cursor(commit=False) as c:
			query = '''
				SELECT timestamp, adapter, ssid, sum(rx), sum(tx)
				FROM {}
				WHERE timestamp >= ? AND timestamp <= ?
				GROUP BY adapter, ssid
				ORDER BY adapter, ssid;
			'''.format(self.table_name)

			c.execute(query, (start_time, end_time))
			results = c.fetchall()

		query_result = {}

		for r in results:
			ts, adapter, ssid, rx, tx = r

			if adapter not in query_result:
				query_result[adapter] = []

			query_result[adapter].append({
				'timestamp': ts,
				'adapter': adapter,
				'ssid': ssid,
				'rx': rx,
				'tx': tx
			})

		return query_result

	def update(self, adapter, ssid, rx, tx, timestamp=None):
		if not timestamp:
			timestamp = time.time()

		with self.db_cursor() as c:
			query = '''
				INSERT OR REPLACE INTO {} (timestamp, adapter, ssid, rx, tx)
					VALUES ( ?, ?, ?, ?, ? );
			'''.format(self.table_name)

			c.execute(query, (self.truncate_time(timestamp), adapter, ssid, rx, tx))

	def add(self, adapter, ssid, delta_rx, delta_tx, timestamp=None):
		if not timestamp:
			timestamp = time.time()

		prev = self.query(adapter, ssid, timestamp=timestamp)

		self.update(
			adapter, ssid,
			prev['rx']+delta_rx, prev['tx']+delta_tx,
			timestamp=timestamp
		)

		self.clear(timestamp=timestamp)

	def clear(self, timestamp=None):
		if not timestamp:
			timestamp = time.time()

		with self.db_cursor() as c:
			query = '''
				DELETE FROM {}
				WHERE timestamp < ?;
			'''.format(self.table_name)

			c.execute(query, (timestamp - self.time_limit, ))
