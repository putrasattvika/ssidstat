import os
import json
import subprocess

def get_adapters_stats():
	vnstat_p = subprocess.Popen(['vnstat', '--json'], stdout=subprocess.PIPE)
	out, err = vnstat_p.communicate()

	return json.loads(out)

def get_todays_traffic(adapter):
	stat = get_adapters_stats()

	for iface in stat['interfaces']:
		if iface['id'] == adapter:
			return iface['traffic']['days'][0]

	return None

def get_adapters_ssid():
	nmcli_p = subprocess.Popen(['nmcli', '-t', 'connection', 'show', '--active'], stdout=subprocess.PIPE)
	out, err = nmcli_p.communicate()

	connections_str = out.split('\n')[:-1]

	connections = {}
	for conn in connections_str:
		ssid = conn.split(':')[0]
		adapter = conn.split(':')[-1]

		connections[adapter] = ssid

	return connections