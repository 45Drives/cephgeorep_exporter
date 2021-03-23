import time
import json
import argparse
import subprocess
import sys
import os
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

def get_status():
	status_path = "/run/cephgeorep/status"
	if not os.path.exists(status_path):
		return None
	f = open(status_path, "r")
	status_str = f.readline()
	f.close()
	try:
		status = int(status_str)
	except ValueError:
		return None
	return status

class CephgeorepCollector(object):
	def __init__(self):
		pass
	
	def collect(self):
		status = get_status()
		cephgeorep_status = GaugeMetricFamily("cephgeorep_status", 'Status of cephgeorep', labels=['field'])
		if status != None:
			cephgeorep_status.add_metric(["status-code"], status)
		yield cephgeorep_status

def parse_args():
	parser = argparse.ArgumentParser(description = 'Prometheus metrics exporter for cephgeorep.')
	parser.add_argument('-p', '--port', required = True, help = 'Port for server')
	return parser.parse_args()

def main():
	try:
		args = parse_args()
		port = None
		try:
			port = int(args.port)
		except ValueError:
			print("Invalid port: ", args.port)
			sys.exit(1)
		if port > 65535 or port <= 1023:
			print("Invalid port range: ", args.port)
			sys.exit(1)
		print("Serving cephgeorep metrics to {}".format(port))
		start_http_server(port)
		REGISTRY.register(CephgeorepCollector())
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print("Interrupted.")
		sys.exit(0)

if __name__ == "__main__":
	main()
