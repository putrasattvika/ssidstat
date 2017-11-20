import os
import unittest

from ssidstat.common.db import SSIDStatDB

TEST_DB_PATH = 'test.db'

class SetupDB(unittest.TestCase):
	def setUp(self):
		if os.path.isfile(TEST_DB_PATH):
			raise Exception('Testing db path "{}" already exists.'.format(TEST_DB_PATH))
		
		self.db = SSIDStatDB(TEST_DB_PATH)

	def tearDown(self):
		os.remove(TEST_DB_PATH)

class UpdateSSIDTrafficHistoryTest(SetupDB):
	def test_update_ssid_traffic_history(self):
		try:
			self.db.update_ssid_traffic_history('adapter_name', 'ssid_name', 100, 200)
		except:
			self.fail()

class QuerySSIDTrafficHistoryTest(SetupDB):
	def setUp(self):
		super(QuerySSIDTrafficHistoryTest, self).setUp()

		self.db.update_ssid_traffic_history('adapter0', 'ssid0', 100, 200)
		self.db.update_ssid_traffic_history('adapter0', 'ssid1', 105, 205)
		self.db.update_ssid_traffic_history('adapter0', 'ssid2', 110, 210)

		self.db.update_ssid_traffic_history('adapter1', 'ssid1', 10, 20)
		self.db.update_ssid_traffic_history('adapter1', 'ssid3', 15, 25)

	def test_query_ssid_stat(self):
		ssid0_stat = self.db.query_ssid_stat('ssid0')

		self.assertEqual(ssid0_stat['ssid'], 'ssid0')
		self.assertEqual(ssid0_stat['rx'], 100)
		self.assertEqual(ssid0_stat['tx'], 200)

	def test_query_all_ssid_stat(self):
		q = self.db.query_all_ssid_stat()

		self.assertEqual(len(q), 2)
		self.assertEqual(len(q['adapter0']), 3)
		self.assertEqual(len(q['adapter1']), 2)
		self.assertEqual(q['adapter0'][0]['ssid'], 'ssid0')
		self.assertEqual(q['adapter0'][0]['rx'], 100)
		self.assertEqual(q['adapter1'][0]['ssid'], 'ssid1')
		self.assertEqual(q['adapter1'][0]['rx'], 10)

if __name__ == '__main__':
	unittest.main()

