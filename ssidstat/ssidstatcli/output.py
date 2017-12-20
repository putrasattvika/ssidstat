import json
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

def filter(stats, adapter_ssid_pairs = None):
	if not adapter_ssid_pairs:
		return stats

	filtered_stats = {}
	for adapter in stats:
		filtered_stats[adapter] = []
		for ssid_stat in stats[adapter]:
			if (adapter, ssid_stat['ssid']) in adapter_ssid_pairs:
				filtered_stats[adapter].append(ssid_stat)

	return filtered_stats

def tabular_output(data):
	if len(data) == 0:
		return 'No data'

	headers = data['headers']
	table = []

	for entry in data['data']:
		table.append( [entry[h] for h in headers] )

	output = tabulate.tabulate(table, headers=headers)
	if ('message' in data) and (data['message']) and (len(data['message']) > 0):
		output = data['message'] + output

	return output

def json_output(data):
	return json.dumps(data['data'])

def default(stats):
	result = {}
	result['headers'] = ['Adapter', 'SSID', 'Receive (rx)', 'Transmit (tx)', 'Total']
	result['data'] = []

	for adapter in stats:
		for ssid_stat in stats[adapter]:
			result['data'].append({
				'Adapter': adapter,
				'SSID': ssid_stat['ssid'],
				'Receive (rx)': byte_format(ssid_stat['rx']),
				'Transmit (tx)': byte_format(ssid_stat['tx']),
				'Total': byte_format(ssid_stat['rx'] + ssid_stat['tx'])
			})

	return result

def hourly(ssid, stats):
	result = {}
	result['message'] = 'Hourly traffic for SSID {}\n\n'.format(ssid)
	result['headers'] = ['Time', 'Receive (rx)', 'Transmit (tx)', 'Total']
	result['data'] = []

	for stat in stats:
		result['data'].append({
			'Time': datetime.strftime(datetime.fromtimestamp(stat['timestamp']), '%Y-%m-%d %H:%M'),
			'Receive (rx)': byte_format(stat['rx']),
			'Transmit (tx)': byte_format(stat['tx']),
			'Total': byte_format(stat['rx'] + stat['tx'])
		})

	return result

def daily(ssid, stats):
	result = {}
	result['message'] = 'Daily traffic for SSID {}\n\n'.format(ssid)
	result['headers'] = ['Date', 'Receive (rx)', 'Transmit (tx)', 'Total']
	result['data'] = []

	for stat in stats:
		result['data'].append({
			'Date': datetime.strftime(datetime.fromtimestamp(stat['timestamp']), '%Y-%m-%d'),
			'Receive (rx)': byte_format(stat['rx']),
			'Transmit (tx)': byte_format(stat['tx']),
			'Total': byte_format(stat['rx'] + stat['tx'])
		})

	return result

def weekly(ssid, stats):
	result = {}
	result['message'] = 'Weekly traffic for SSID {}\n\n'.format(ssid)
	result['headers'] = ['Date', 'Receive (rx)', 'Transmit (tx)', 'Total']
	result['data'] = []

	for stat in stats:
		start_date = datetime.fromtimestamp(stat['timestamp'])
		end_date = datetime.fromtimestamp(stat['timestamp'] + 7*24*3600-1)

		result['data'].append({
			'Date': '{} ~ {}'.format(
				datetime.strftime(start_date, '%Y-%m-%d'),
				datetime.strftime(end_date, '%Y-%m-%d'),
			),
			'Receive (rx)': byte_format(stat['rx']),
			'Transmit (tx)': byte_format(stat['tx']),
			'Total': byte_format(stat['rx'] + stat['tx'])
		})

	return result

def monthly(ssid, stats):
	result = {}
	result['message'] = 'Monthly traffic for SSID {}\n\n'.format(ssid)
	result['headers'] = ['Date', 'Receive (rx)', 'Transmit (tx)', 'Total']
	result['data'] = []

	for stat in stats:
		result['data'].append({
			'Date': datetime.strftime(datetime.fromtimestamp(stat['timestamp']), '%B %Y'),
			'Receive (rx)': byte_format(stat['rx']),
			'Transmit (tx)': byte_format(stat['tx']),
			'Total': byte_format(stat['rx'] + stat['tx'])
		})

	return result
