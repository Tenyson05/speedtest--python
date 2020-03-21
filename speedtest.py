import os
import logging

LOG_FILE = "speedtest.log"


def setup_logging():
	'''Logs the information retrieved from speedtest'''
	logging.basicConfig(
		filename=LOG_FILE,
		level=logging.INFO,
		format="%(asctime)s %(message)s",
		datefmt="%Y-%m-%d %H:%M",
	)

def get_speedtest_results():

	''' -
		Run test and parse results.
		Returns tuple of ping speed, download speed and upload speed or
		raises valueError if unable to parse data		
	'''
	ping = None
	download = None
	upload = None

	with os.popen("speedtest-cli  --simple") as spedtest_output:
		for line in spedtest_output:
			label, value, unit = line.split()
			if 'Ping' in label:
				ping = float(value)
			elif 'Download' in label:
				download = float(value)
			elif 'Upload' in label:
				upload = float(value)

	if all((ping, download, upload)):
		return ping, download, upload
	else:
		raise ValueError('TEST FAILED')


def main():
	setup_logging()
	try:
		ping, download, upload = get_speedtest_results()
	except ValueError as err:
		logging.info(err)
	else:
		logging.info("%5.1f %5.1f %5.1f", ping, download, upload)