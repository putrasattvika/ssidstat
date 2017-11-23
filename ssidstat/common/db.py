import json
import sqlite3

from datetime import datetime
from contextlib import contextmanager

class SSIDStatDB(object):
	def __init__(self, dbfile):
		super(SSIDStatDB, self).__init__()

		self.dbfile = dbfile
		self.init_db()

	def date_to_str(self, date, format='%Y-%m-%d'):
		return datetime.strftime(date, format)

	@contextmanager
	def db_cursor(self, commit=True):
		conn = sqlite3.connect(self.dbfile)

		yield conn.cursor()

		if commit: conn.commit()
		conn.close()

	def init_db(self):
		with self.db_cursor() as c:
			c.execute('''
				CREATE TABLE IF NOT EXISTS ssid_traffic_history (
					date text,
					adapter text,
					ssid text,
					rx integer,
					tx integer,
					PRIMARY KEY (date, adapter, ssid)
				)
			''')

			c.execute('''
				CREATE TABLE IF NOT EXISTS boot_traffic_history (
					boot_id text,
					adapter text,
					rx integer,
					tx integer,
					PRIMARY KEY (boot_id, adapter)
				)
			''')

	def update_ssid_traffic_history(self, adapter, ssid, rx, tx, date=datetime.now()):
		with self.db_cursor() as c:
			query = '''
				INSERT OR REPLACE INTO ssid_traffic_history (date, adapter, ssid, rx, tx)
					VALUES ( ?, ?, ?, ?, ? );
			'''

			c.execute(query, (self.date_to_str(date), adapter, ssid, rx, tx))

	def query_ssid_stat(self, ssid, date=datetime.now()):
		with self.db_cursor(commit=False) as c:
			query = '''
				SELECT date, ssid, rx, tx
				FROM ssid_traffic_history
				WHERE ssid=? AND date=?;
			'''

			c.execute(query, (ssid, self.date_to_str(date)))
			result = c.fetchone()

		if result == None:
			result = (self.date_to_str(date), ssid, 0, 0)

		return {
			'date': date,
			'ssid': ssid,
			'rx': result[2],
			'tx': result[3]
		}

	def query_all_ssid_stat(self, date=datetime.now()):
		with self.db_cursor(commit=False) as c:
			query = '''
				SELECT date, ssid, rx, tx, adapter
				FROM ssid_traffic_history
				WHERE date=?
				ORDER BY adapter, ssid;
			'''

			c.execute(query, (self.date_to_str(date),))
			results = c.fetchall()

		d_result = {}

		for r in results:
			date, ssid, rx, tx, adapter = r

			if adapter not in d_result:
				d_result[adapter] = []

			d_result[adapter].append({
				'ssid': ssid,
				'date': date,
				'adapter': adapter,
				'rx': rx,
				'tx': tx
			})

		return d_result

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
