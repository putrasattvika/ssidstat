import json
import sqlite3

from datetime import datetime

class SSIDStatDB(object):
	def __init__(self, dbfile):
		super(SSIDStatDB, self).__init__()

		self.dbfile = dbfile
		self.init_db()

	def date_to_str(self, date, format='%Y-%m-%d'):
		return datetime.strftime(date, format)

	def init_db(self):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			CREATE TABLE IF NOT EXISTS ssidstat (
				date text,
				adapter text,
				ssid text,
				rx integer,
				tx integer,
				PRIMARY KEY (date, adapter, ssid)
			)
		'''

		c.execute(query)

		conn.commit()
		conn.close()

	def update_db(self, adapter, ssid, rx, tx, date=datetime.now()):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			INSERT OR REPLACE INTO ssidstat (date, adapter, ssid, rx, tx) 
				VALUES ( ?, ?, ?, ?, ? );
		'''

		c.execute(query, (self.date_to_str(date), adapter, ssid, rx, tx))

		conn.commit()
		conn.close()

	def query_adapter_stat(self, adapter, date=datetime.now()):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			SELECT date, adapter, sum(rx), sum(tx)
			FROM ssidstat
			WHERE adapter=? AND date=?
			GROUP BY date, adapter;
		'''

		c.execute(query, (adapter, self.date_to_str(date)))
		result = c.fetchone()
		conn.close()

		if result == None:
			result = (self.date_to_str(date), adapter, 0, 0)

		return {
			'date': date,
			'adapter': adapter,
			'rx': result[2],
			'tx': result[3]
		}

	def query_ssid_stat(self, ssid, date=datetime.now()):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			SELECT date, ssid, sum(rx), sum(tx)
			FROM ssidstat
			WHERE ssid=? AND date=?
			GROUP BY date, ssid;
		'''

		c.execute(query, (ssid, self.date_to_str(date)))
		result = c.fetchone()
		conn.close()	

		if result == None:
			result = (self.date_to_str(date), ssid, 0, 0)

		return {
			'date': date,
			'ssid': ssid,
			'rx': result[2],
			'tx': result[3]
		}