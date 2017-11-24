import time
import sqlite3

from datetime import datetime
from contextlib import contextmanager

class BaseModel(object):
	def __init__(self, dbfile, table_name):
		super(BaseModel, self).__init__()

		self.dbfile = dbfile
		self.table_name = table_name
		self.init_db()

	@contextmanager
	def db_cursor(self, commit=True):
		conn = sqlite3.connect(self.dbfile)

		yield conn.cursor()

		if commit: conn.commit()
		conn.close()

	def init_db(self):
		raise NotImplementedError
