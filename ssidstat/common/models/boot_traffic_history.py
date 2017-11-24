import time
import sqlite3

from base_model import BaseModel

from datetime import datetime
from contextlib import contextmanager

class BootTrafficHistory(BaseModel):
	def __init__(self, dbfile, table_name):
		super(BootTrafficHistory, self).__init__(dbfile, table_name)

	def init_db(self):
		with self.db_cursor() as c:
			c.execute('''
				CREATE TABLE IF NOT EXISTS {} (
					boot_id text,
					adapter text,
					rx integer,
					tx integer,
					PRIMARY KEY (boot_id, adapter)
				)
			'''.format(self.table_name))

	def update(self, boot_id, adapter, rx, tx):
		with self.db_cursor() as c:
			query = '''
				INSERT OR REPLACE INTO {} (boot_id, adapter, rx, tx)
					VALUES ( ?, ?, ?, ? );
			'''.format(self.table_name)

			c.execute(query, (boot_id, adapter, rx, tx))

	def query(self, boot_id, adapter):
		with self.db_cursor(commit=False) as c:
			query = '''
				SELECT rx, tx
				FROM {}
				WHERE boot_id=? AND adapter=?;
			'''.format(self.table_name)

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

	def clear(self, adapter):
		with self.db_cursor() as c:
			query = '''
				DELETE FROM {}
				WHERE adapter=?;
			'''.format(self.table_name)

			c.execute(query, (adapter, ))
