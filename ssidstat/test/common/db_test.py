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

class UpdateTest(SetupDB):
	def test_update(self):
		try:
			self.db.update_db('adapter_name', 'ssid_name', 100, 200)
		except:
			self.fail()

class QueryTest(SetupDB):
	def setUp(self):
		super(QueryTest, self).setUp()

		self.db.update_db('adapter0', 'ssid0', 100, 200)
		self.db.update_db('adapter0', 'ssid1', 105, 205)
		self.db.update_db('adapter0', 'ssid2', 110, 210)

		self.db.update_db('adapter1', 'ssid1', 10, 20)
		self.db.update_db('adapter1', 'ssid3', 15, 25)

	def test_query_adapter_stat(self):
		adapter0_stat = self.db.query_adapter_stat('adapter0')
		adapter1_stat = self.db.query_adapter_stat('adapter1')

		self.assertEqual(len(adapter0_stat), 4)
		self.assertEqual(len(adapter1_stat), 4)

		self.assertEqual(adapter0_stat['adapter'], 'adapter0')
		self.assertEqual(adapter0_stat['rx'], 315)
		self.assertEqual(adapter0_stat['tx'], 615)

		self.assertEqual(adapter1_stat['adapter'], 'adapter1')
		self.assertEqual(adapter1_stat['rx'], 25)
		self.assertEqual(adapter1_stat['tx'], 45)

	def test_query_ssid_stat(self):
		ssid0_stat = self.db.query_ssid_stat('ssid0')

		self.assertEqual(ssid0_stat['ssid'], 'ssid0')
		self.assertEqual(ssid0_stat['rx'], 100)
		self.assertEqual(ssid0_stat['tx'], 200)

	def test_query_all_ssid_stat(self):
		q = self.db.query_all_ssid_stat()

		self.assertEqual(len(q), 4)
		self.assertEqual(q['ssid0']['rx'], 100)
		self.assertEqual(q['ssid1']['rx'], 115)

if __name__ == '__main__':
	unittest.main()

