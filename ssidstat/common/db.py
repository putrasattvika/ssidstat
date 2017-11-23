import json
import time
import sqlite3

import db_utils

from datetime import datetime
from contextlib import contextmanager

# hour table limit: 40 days
_HOURLY_LIMIT_SECS = 3600*24*40

# month table limit: 400 days
_MONTHLY_LIMIT_SECS = 3600*24*400

# constants
HOUR  = 0
DAY   = 1
WEEK  = 2
MONTH = 3

_truncate_func_map = {
	HOUR:  db_utils.truncate_time_hour,
	DAY:   db_utils.truncate_time_day,
	WEEK:  db_utils.truncate_time_week,
	MONTH: db_utils.truncate_time_month
}

class SSIDStatDB(object):
	def __init__(self, dbfile):
		super(SSIDStatDB, self).__init__()

		self.dbfile = dbfile
		self.init_db()

	@contextmanager
	def db_cursor(self, commit=True):
		conn = sqlite3.connect(self.dbfile)

		yield conn.cursor()

		if commit: conn.commit()
		conn.close()

	def init_db(self):
		with self.db_cursor() as c:
			# hourly SSID traffic history
			c.execute('''
				CREATE TABLE IF NOT EXISTS hourly_ssid_traffic_history (
					hour_ts integer,
					adapter text,
					ssid text,
					rx integer,
					tx integer,
					PRIMARY KEY (hour_ts, adapter, ssid)
				)
			''')

			# monthly SSID traffic history
			c.execute('''
				CREATE TABLE IF NOT EXISTS monthly_ssid_traffic_history (
					month_ts integer,
					adapter text,
					ssid text,
					rx integer,
					tx integer,
					PRIMARY KEY (month_ts, adapter, ssid)
				)
			''')

			# per-boot adapter traffic history
			c.execute('''
				CREATE TABLE IF NOT EXISTS boot_traffic_history (
					boot_id text,
					adapter text,
					rx integer,
					tx integer,
					PRIMARY KEY (boot_id, adapter)
				)
			''')

	def update_ssid_traffic_history(self, adapter, ssid, rx, tx, use_hourly_table=True, timestamp=time.time()):
		if use_hourly_table:
			table_name = 'hourly_ssid_traffic_history'
			pk = 'hour_ts'
			trunc_func = db_utils.truncate_time_hour
		else:
			table_name = 'monthly_ssid_traffic_history'
			pk = 'month_ts'
			trunc_func = db_utils.truncate_time_month

		with self.db_cursor() as c:
			query = '''
				INSERT OR REPLACE INTO {} ({}, adapter, ssid, rx, tx)
					VALUES ( ?, ?, ?, ?, ? );
			'''.format(table_name, pk)

			c.execute(query, (trunc_func(timestamp), adapter, ssid, rx, tx))

	def add_ssid_traffic_history(self, adapter, ssid, delta_rx, delta_tx, timestamp=time.time()):
		hourly_prev = self.query_adapter_ssid_stat(adapter, ssid, use_hourly_table=True, timestamp=timestamp)
		monthly_prev = self.query_adapter_ssid_stat(adapter, ssid, use_hourly_table=False, timestamp=timestamp)

		self.update_ssid_traffic_history(
			adapter, ssid,
			hourly_prev['rx']+delta_rx, hourly_prev['tx']+delta_tx,
			use_hourly_table=True, timestamp=timestamp
		)

		self.update_ssid_traffic_history(
			adapter, ssid,
			monthly_prev['rx']+delta_rx, monthly_prev['tx']+delta_tx,
			use_hourly_table=False, timestamp=timestamp
		)

		self.clear_ssid_traffic_history(timestamp=timestamp)

	def query_adapter_ssid_stat(self, adapter, ssid, use_hourly_table=True, timestamp=time.time()):
		if use_hourly_table:
			table_name = 'hourly_ssid_traffic_history'
			pk = 'hour_ts'
			trunc_func = db_utils.truncate_time_hour
		else:
			table_name = 'monthly_ssid_traffic_history'
			pk = 'month_ts'
			trunc_func = db_utils.truncate_time_month

		with self.db_cursor(commit=False) as c:
			query = '''
				SELECT {0}, adapter, ssid, rx, tx
				FROM {1}
				WHERE adapter=? AND ssid=? AND {0}=?;
			'''.format(pk, table_name)

			c.execute(query, (adapter, ssid, trunc_func(timestamp)))
			result = c.fetchone()

		if result == None:
			result = (trunc_func(timestamp), adapter, ssid, 0, 0)

		return {
			'timestamp': trunc_func(timestamp),
			'adapter': adapter,
			'ssid': ssid,
			'rx': result[3],
			'tx': result[4]
		}

	def query_all_ssid_stat(self, resolution=DAY, timestamp=time.time()):
		with self.db_cursor(commit=False) as c:
			query = '''
				SELECT hour_ts, ssid, sum(rx), sum(tx), adapter
				FROM hourly_ssid_traffic_history
				WHERE hour_ts >= ?
				GROUP BY adapter, ssid
				ORDER BY adapter, ssid;
			'''

			c.execute(query, (_truncate_func_map[resolution](timestamp),))
			results = c.fetchall()

		d_result = {}

		for r in results:
			hour_ts, ssid, rx, tx, adapter = r

			if adapter not in d_result:
				d_result[adapter] = []

			d_result[adapter].append({
				'ssid': ssid,
				'hour_ts': hour_ts,
				'adapter': adapter,
				'rx': rx,
				'tx': tx
			})

		return d_result

	def clear_ssid_traffic_history(self, timestamp=time.time()):
		with self.db_cursor() as c:
			query = '''
				DELETE FROM hourly_ssid_traffic_history
				WHERE hour_ts < ?;
			'''
			c.execute(query, (timestamp - _HOURLY_LIMIT_SECS, ))

			query = '''
				DELETE FROM monthly_ssid_traffic_history
				WHERE month_ts < ?;
			'''
			c.execute(query, (timestamp - _MONTHLY_LIMIT_SECS, ))


	def update_boot_traffic_history(self, boot_id, adapter, rx, tx):
		with self.db_cursor() as c:
			query = '''
				INSERT OR REPLACE INTO boot_traffic_history (boot_id, adapter, rx, tx)
					VALUES ( ?, ?, ?, ? );
			'''

			c.execute(query, (boot_id, adapter, rx, tx))

	def query_boot_traffic_history(self, boot_id, adapter):
		with self.db_cursor(commit=False) as c:
			query = '''
				SELECT rx, tx
				FROM boot_traffic_history
				WHERE boot_id=? AND adapter=?;
			'''

			c.execute(query, (boot_id, adapter))
			result = c.fetchone()

		if result == None:
			return None

		return {
			'boot_id': boot_id,
			'adapter': adapter,
			'rx': result[0],
			'tx': result[1]
		}

	def clear_boot_traffic_history(self, adapter):
		with self.db_cursor() as c:
			query = '''
				DELETE FROM boot_traffic_history
				WHERE adapter=?;
			'''

			c.execute(query, (adapter, ))
