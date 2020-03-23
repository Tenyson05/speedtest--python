import os
import matplotlib.pyplot as plt
from matplotlib import dates, rcParams
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def read_data():
	'''read the data from the logs'''
	df = pd.io.parsers.read_csv(
		'speedtest.log',
		names='date time ping download upload'.split(),
		header=None,
		sep=r'\s+',
		parse_dates={'timestamp':[0,1]},
		na_values=['TEST','FAILED'],
		
	)

	print(df)
	# return the data from the last one in the log file
	return df[-48:]

def make_plot_file(last_24, file_plot_name):
	'''
		Creates the graph and apply all the relevant information, that is
		Title of the axis and graph as well as the scaling of each axis
	'''
	rcParams['xtick.labelsize'] = 'xx-small'
	rcParams['ytick.labelsize'] = '5'

	# Getting the last 24 hour of timestamp and download speed
	plt.plot(last_24['timestamp'],last_24['download'], 'b-')
	# title of the graph
	plt.title('Bandwith Report (last 24 hours)')
	# Bandwidth in 
	plt.ylabel('Bandwith in Mbps')
	plt.yticks(xrange(0,52))
	plt.ylim(1,50)


	plt.xlabel('Date/Time')
	plt.xticks(rotation='45')
	# plt.yticks(rotation='30')
	# plt.yticks(width='5')

	plt.grid

	current_axes = plt.gca()
	current_figure = plt.gcf()

	hfmt = dates.DateFormatter('%m/%d %H:%M')
	current_axes.xaxis.set_major_formatter(hfmt)
	current_figure.subplots_adjust(bottom=.25)

	loc = current_axes.xaxis.get_major_locator()
	loc.maxticks[dates.HOURLY] = 24
	loc.maxticks[dates.MINUTELY]

	current_figure.savefig(file_plot_name)

def create_plot(plot_file_name):
	df = read_data()
	make_plot_file(df, plot_file_name)


def main():
	plot_file_name = 'bandwidth.png'
	create_plot(plot_file_name)
	os.system('open' + plot_file_name)

if __name__=='__main__':
	main()