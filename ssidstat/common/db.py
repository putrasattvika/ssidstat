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

		conn.commit()
		conn.close()

	def update_ssid_traffic_history(self, adapter, ssid, rx, tx, date=datetime.now()):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			INSERT OR REPLACE INTO ssid_traffic_history (date, adapter, ssid, rx, tx) 
				VALUES ( ?, ?, ?, ?, ? );
		'''

		c.execute(query, (self.date_to_str(date), adapter, ssid, rx, tx))

		conn.commit()
		conn.close()

	def query_ssid_stat(self, ssid, date=datetime.now()):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			SELECT date, ssid, rx, tx
			FROM ssid_traffic_history
			WHERE ssid=? AND date=?;
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

	def query_all_ssid_stat(self, date=datetime.now()):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			SELECT date, ssid, rx, tx, adapter
			FROM ssid_traffic_history
			WHERE date=?
			ORDER BY adapter, ssid;
		'''

		c.execute(query, (self.date_to_str(date),))
		results = c.fetchall()
		conn.close()

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
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			INSERT OR REPLACE INTO boot_traffic_history (boot_id, adapter, rx, tx) 
				VALUES ( ?, ?, ?, ? );
		'''

		c.execute(query, (boot_id, adapter, rx, tx))

		conn.commit()
		conn.close()

	def query_boot_traffic_history(self, boot_id, adapter):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			SELECT rx, tx
			FROM boot_traffic_history
			WHERE boot_id=? AND adapter=?;
		'''

		c.execute(query, (boot_id, adapter))
		result = c.fetchone()
		conn.close()	

		if result == None:
			return None

		return {
			'boot_id': boot_id,
			'adapter': adapter,
			'rx': result[0],
			'tx': result[1]
		}

	def clear_boot_traffic_history(self, adapter):
		conn = sqlite3.connect(self.dbfile)
		c = conn.cursor()

		query = '''
			DELETE FROM boot_traffic_history
			WHERE adapter=?;
		'''

		c.execute(query, (adapter, ))

		conn.commit()
		conn.close()
