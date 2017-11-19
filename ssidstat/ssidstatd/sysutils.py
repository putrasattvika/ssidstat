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

def get_adapters():
	sys_class_net_p = subprocess.Popen(['ls', '-1', '/sys/class/net'], stdout=subprocess.PIPE)
	sys_class_net_out, sys_class_net_err = sys_class_net_p.communicate()

	return sys_class_net_out.split('\n')[:-1]

def get_adapter_ssid(adapter):
	iw_p = subprocess.Popen(['iw {} link | grep -Poe "SSID: .*"'.format(adapter)], stdout=subprocess.PIPE, shell=True)
	iw_out, iw_err = iw_p.communicate()

	ssid = iw_out[6:].strip()
	if len(ssid) == 0:
		ssid = adapter

	return ssid

def get_adapters_ssid():
	adapters = get_adapters()

	connections = {}
	for adapter in adapters:
		connections[adapter] = get_adapter_ssid(adapter)

	return connections
