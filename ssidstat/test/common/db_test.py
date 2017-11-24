import os
import time
import unittest

import ssidstat.common.db

TEST_DB_PATH = 'test.db'

class SetupDB(unittest.TestCase):
	def setUp(self):
		if os.path.isfile(TEST_DB_PATH):
			raise Exception('Testing db path "{}" already exists.'.format(TEST_DB_PATH))
		
		self.db = ssidstat.common.db.SSIDStatDB(TEST_DB_PATH)

	def tearDown(self):
		os.remove(TEST_DB_PATH)

class QuerySSIDTrafficHistoryTest(SetupDB):
	def setUp(self):
		super(QuerySSIDTrafficHistoryTest, self).setUp()

		self.t = 1483228800

		self.db.add_ssid_traffic_history('adapter0', 'ssid0', 1, 1, timestamp=0*3600+self.t)
		self.db.add_ssid_traffic_history('adapter0', 'ssid0', 2, 2, timestamp=1*3600+self.t)
		self.db.add_ssid_traffic_history('adapter0', 'ssid0', 4, 4, timestamp=2*3600+self.t)
		self.db.add_ssid_traffic_history('adapter0', 'ssid0', 10, 10, timestamp=2*3600+self.t)
		self.db.add_ssid_traffic_history('adapter0', 'ssid1', 100, 100, timestamp=0*3600+self.t)

	def test_query_all_ssid_stat_day(self):
		q = self.db.query_all_ssid_stat(resolution=ssidstat.common.db.DAY, timestamp=24*3600+self.t-1)

		self.assertEqual(len(q), 1)
		self.assertEqual(len(q['adapter0']), 2)

		self.assertEqual(q['adapter0'][0]['ssid'], 'ssid0')
		self.assertEqual(q['adapter0'][0]['rx'], 1 + 2 + 4 + 10)

		self.assertEqual(q['adapter0'][1]['ssid'], 'ssid1')
		self.assertEqual(q['adapter0'][1]['rx'], 100)

	def test_query_all_ssid_stat_month(self):
		self.db.add_ssid_traffic_history('adapter0', 'ssid2', 11, 11, timestamp=1488*3600+self.t)
		self.db.add_ssid_traffic_history('adapter0', 'ssid2', 12, 12, timestamp=1512*3600+self.t)
		q = self.db.query_all_ssid_stat(resolution=ssidstat.common.db.MONTH, timestamp=1536*3600+self.t)

		self.assertEqual(len(q), 1)
		self.assertEqual(len(q['adapter0']), 1)
		self.assertEqual(q['adapter0'][0]['ssid'], 'ssid2')
		self.assertEqual(q['adapter0'][0]['rx'], 11 + 12)

	def test_clear_ssid_stat(self):
		self.db.add_ssid_traffic_history('adapter0', 'ssid0', 1000, 1, timestamp=3600*24*80+self.t+100)

		q = self.db.query_all_ssid_stat(resolution=ssidstat.common.db.DAY, timestamp=3600*24*80+self.t+100)
		self.assertEqual(len(q), 1)
		self.assertEqual(len(q['adapter0']), 1)
		self.assertEqual(q['adapter0'][0]['ssid'], 'ssid0')
		self.assertEqual(q['adapter0'][0]['rx'], 1000)
		self.assertEqual(q['adapter0'][0]['tx'], 1)

if __name__ == '__main__':
	unittest.main()
