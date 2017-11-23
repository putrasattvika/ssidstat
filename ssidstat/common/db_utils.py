import time
from datetime import datetime

def truncate_time_hour(timestamp):
	return int(timestamp/3600)*3600

def truncate_time_day(timestamp):
	return int(timestamp/86400)*86400

def truncate_time_week(timestamp):
	return int(timestamp/604800)*604800

def truncate_time_month(timestamp):
	dt_month = datetime.strptime(datetime.strftime(datetime.fromtimestamp(timestamp), '%Y-%m'), '%Y-%m')
	return int((dt_month - datetime.fromtimestamp(0)).total_seconds())
