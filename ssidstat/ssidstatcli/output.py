import tabulate
from datetime import datetime

def byte_format(size):
	prefixes = ['B', 'KiB', 'MiB', 'GiB', 'TiB']

	result = '{:.2f} {}'.format(size, prefixes[0])
	for i in xrange(len(prefixes)):
		if size/(2.0**(10*i)) >= 1:
			result = '{:.2f} {}'.format(size/(2.0**(10*i)), prefixes[i])
		else:
			break

	return result

def default(stats):
	headers = ['Adapter', 'SSID', 'Receive (rx)', 'Transmit (tx)', 'Total']
	table = []

	for adapter in stats:
		for ssid_stat in stats[adapter]:
			table.append([
				adapter,
				ssid_stat['ssid'],
				byte_format(ssid_stat['rx']),
				byte_format(ssid_stat['tx']),
				byte_format(ssid_stat['rx'] + ssid_stat['tx'])
			])

	return tabulate.tabulate(table, headers=headers)

def hourly(ssid, stats):
	headers = ['Time', 'Receive (rx)', 'Transmit (tx)', 'Total']
	table = []

	for stat in stats:
		table.append([
			datetime.strftime(datetime.fromtimestamp(stat['timestamp']), '%Y-%m-%d %H:%M'),
			byte_format(stat['rx']),
			byte_format(stat['tx']),
			byte_format(stat['rx'] + stat['tx'])
		])

	output  = 'Hourly traffic for SSID {}\n\n'.format(ssid)
	output += tabulate.tabulate(table, headers=headers)
	return output

def daily(ssid, stats):
	headers = ['Date', 'Receive (rx)', 'Transmit (tx)', 'Total']
	table = []

	for stat in stats:
		table.append([
			datetime.strftime(datetime.fromtimestamp(stat['timestamp']), '%Y-%m-%d'),
			byte_format(stat['rx']),
			byte_format(stat['tx']),
			byte_format(stat['rx'] + stat['tx'])
		])

	output  = 'Daily traffic for SSID {}\n\n'.format(ssid)
	output += tabulate.tabulate(table, headers=headers)
	return output

def weekly(ssid, stats):
	headers = ['Date', 'Receive (rx)', 'Transmit (tx)', 'Total']
	table = []

	for stat in stats:
		start_date = datetime.fromtimestamp(stat['timestamp'])
		end_date = datetime.fromtimestamp(stat['timestamp'] + 7*24*3600-1)

		table.append([
			'{} ~ {}'.format(
				datetime.strftime(start_date, '%Y-%m-%d'),
				datetime.strftime(end_date, '%Y-%m-%d'),
			),
			byte_format(stat['rx']),
			byte_format(stat['tx']),
			byte_format(stat['rx'] + stat['tx'])
		])

	output  = 'Weekly traffic for SSID {}\n\n'.format(ssid)
	output += tabulate.tabulate(table, headers=headers)
	return output

def monthly(ssid, stats):
	headers = ['Date', 'Receive (rx)', 'Transmit (tx)', 'Total']
	table = []

	for stat in stats:
		table.append([
			datetime.strftime(datetime.fromtimestamp(stat['timestamp']), '%B %Y'),
			byte_format(stat['rx']),
			byte_format(stat['tx']),
			byte_format(stat['rx'] + stat['tx'])
		])

	output  = 'Monthly traffic for SSID {}\n\n'.format(ssid)
	output += tabulate.tabulate(table, headers=headers)
	return output
