import os
import re
import json
import subprocess

def get_boot_id():
	return open('/proc/sys/kernel/random/boot_id').read().strip()

def get_adapters_traffic():
	adapter_lines = open('/proc/net/dev', 'r').readlines()[2:]

	stats = {}
	for line in adapter_lines:
		adapter, traffic = line.split(':')
		adapter = adapter.strip()
		traffic = traffic.strip()

		traffic_split = re.sub('[ ]+', ';', traffic).split(';')
		stats[adapter] = {
			'rx': int(traffic_split[0]),
			'tx': int(traffic_split[8])
		}

	return stats

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
