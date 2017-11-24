import json
import time
import sqlite3

import db_utils

from datetime import datetime
from contextlib import contextmanager

from models.boot_traffic_history import BootTrafficHistory
from models.hourly_traffic_history import HourlyTrafficHistory
from models.monthly_traffic_history import MonthlyTrafficHistory

# table names
_BOOT_TABLE_NAME = 'boot_traffic_history'
_HOURLY_TABLE_NAME = 'hourly_ssid_traffic_history'
_MONTHLY_TABLE_NAME = 'monthly_ssid_traffic_history'

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
		self.boot_traffic_history = BootTrafficHistory(self.dbfile, _BOOT_TABLE_NAME)
		self.hourly_traffic_history = HourlyTrafficHistory(self.dbfile, _HOURLY_TABLE_NAME)
		self.monthly_traffic_history = MonthlyTrafficHistory(self.dbfile, _MONTHLY_TABLE_NAME)

	def add_ssid_traffic_history(self, adapter, ssid, delta_rx, delta_tx, timestamp=time.time()):
		self.hourly_traffic_history.add(adapter, ssid, delta_rx, delta_tx, timestamp=timestamp)
		self.monthly_traffic_history.add(adapter, ssid, delta_rx, delta_tx, timestamp=timestamp)

	def query_all_ssid_stat(self, resolution=DAY, timestamp=time.time()):
		start_time = _truncate_func_map[resolution](timestamp)
		end_time = timestamp

		return self.hourly_traffic_history.query_all(start_time=start_time, end_time=end_time, timestamp=timestamp)

	def update_boot_traffic_history(self, boot_id, adapter, rx, tx):
		self.boot_traffic_history.update(boot_id, adapter, rx, tx)

	def query_boot_traffic_history(self, boot_id, adapter):
		return self.boot_traffic_history.query(boot_id, adapter)

	def clear_boot_traffic_history(self, adapter):
		self.boot_traffic_history.clear(adapter)
