import matplotlib.pyplot as plt
from matplotlib import dates
import csv
from datetime import datetime
from datetime import date
import matplotlib
import numpy as np
from dateutil.parser import parse

### Function to display event descriptions on hover
def onpick3(event):
	global last
	for curve in ax2.get_lines(): # Going through list of single points
		if curve.contains(event)[0]:
			label = curve.get_label()
			#print "printing label & last: ", label, last
			if label != last and (label not in data_legends) and label != 'Estimated Installs' and label != 'Estimated Uninstalls': # Only show label for events (not plots) and once for consecutive mouse overs
				print label
				last = label
	for curve in ax2.get_children(): # Going through list of lines
		if curve.contains(event)[0]:
			label = curve.get_label()
			if isinstance(label, unicode):
				if label != last and len(label) > 0 and (label not in data_legends) and label != 'Estimated Installs' and label != 'Estimated Uninstalls': # Only show label for events (not plots) and once for consecutive mouse overs
					print label
					last = label


### Curve fitting to estimate trends	
def curve_fit(x, y):
	# calculate polynomial
	z = np.polyfit(x, y, 2)
	f = np.poly1d(z)
	
	# calculate new x's and y's
	x_new = np.linspace(x[0], x[-1], 50)
	y_new = f(x_new)
	
	return x_new, y_new

# Ask user whether to overlay event info or not	
overlay_events_flag = 's'
invalid_response = True

while (invalid_response):
	overlay_events_flag = raw_input("Overlay event information? (Y/N)").lower()
	if (overlay_events_flag != 'y' and overlay_events_flag != 'n'):
		invalid_response = True
	else:
		invalid_response = False

# Take file names as command line input
invalid_response = True

while (invalid_response):
	filename = raw_input("Enter the file name (case sensitive) that contains MRR/installs/uninstalls information (include the extension, for example: data.csv): ")
	
	# Opening and reading data files
	try:
		f = open(filename, 'rU')
		stats = csv.reader(f, delimiter=',')
		data_headers = next(stats, None)  # Read the headers
		invalid_response = False
	except:
		print "Could not find file. Please ensure that file exists and file name was correctly input - remember, the name is case sensitive!"

invalid_response = True

if overlay_events_flag == 'y':
	while (invalid_response):
		filename_milestones = raw_input("Enter the file name (case sensitive) that contains milestones/notable events information (include the extension, for example: events.csv): ")
		
		# Opening and reading data files
		try:
			f_milestones = open(filename_milestones, 'rU')
			event_data = csv.reader(f_milestones, delimiter=',')
			event_data_headers = next(event_data, None)  # Read the headers
			invalid_response = False
		except:
			print "Could not find file. Please ensure that file exists and file name was correctly input - remember, the name is case sensitive!"	

invalid_response = True

while (invalid_response):
	plot_date_start = raw_input("Plot data on the graph from date (DD/MM/YY): ")
	
	try: 
		plot_date_start = parse(plot_date_start)
		invalid_response = False
	except:
		print "Input does not appear to be a date :S Please try again!"
		
invalid_response = True

while (invalid_response):
	plot_date_end = raw_input("Plot data on the graph till date (DD/MM/YY): ")
	
	try: 
		plot_date_end = parse(plot_date_end)
		invalid_response = False
	except:
		print "Input does not appear to be a date :S Please try again!"

# Ask user which metric to plot on which axis
print "Found following data headers: "
for i in range(len(data_headers)):
	print "(" + str(i + 1) + ") " + data_headers[i]

date_column_index = input("Choose column that contains X-axis values (dates): ") - 1
first_axis_columns = raw_input("Choose column(s) that contain(s) first Y-axis values (separate numbers by space): ")
first_axis_columns = [int(i) - 1 for i in first_axis_columns.split(' ')]
second_axis_columns = raw_input("Choose column(s) that contain(s) second Y-axis values (separate numbers by space): ")
second_axis_columns = [int(i) - 1 for i in second_axis_columns.split(' ')]
	
columns_to_plot = set().union(first_axis_columns, second_axis_columns)
date_range_start = []
date_range_end = []
measures_to_plot = [[] for i in range(len(data_headers) - 1)] # Initialize array to appropriate size
net_mrr = []
uninstalls = []
installs = []
data_indexes = {}
data_index_second_axis = -1
y_label = 'Number of '

colours = ['purple', 'teal', 'orchid', 'C3', 'C4', 'C5']
markers = ['+', 'o', '*', '+', 'o', '*']
data_legends = data_headers[1:]

# Parse and process data
for line in stats:
	# Parse date fields as dates
	rs = parse(line[date_column_index].split('-')[0].strip())
	re = parse(line[date_column_index].split('-')[1].strip())
	
	if (rs >= plot_date_start):
		date_range_start.append(rs)
	if (re <= plot_date_end):
		date_range_end.append(re)
	
	# Iterate over all columns and read in data fields
	for metric in columns_to_plot:
		value = line[metric + 1]
		measures_to_plot[metric].append(float(value.replace(',', ''))) # Strip out commas from numeric values and convert to float
		
fdts = dates.date2num(date_range_end) # Convert dates to numbers
hfmt = dates.DateFormatter('%b %d') # Format dates
fig = plt.figure()
ax = fig.add_subplot(111)
ax2 = ax.twinx()


for metric in range(len(data_headers) - 1):
	result = curve_fit(fdts, measures_to_plot[metric]) # Fit curve to data points to estimate trend
	if metric == data_index_second_axis:
		ax.plot(fdts, measures_to_plot[metric], label = data_legends[metric], marker = markers[metric], color = colours[metric], linewidth = 1) # Plot raw data points
		ax.plot(result[0], result[1], label = 'Estimated ' + data_legends[metric], linestyle = '--', color = colours[metric], linewidth = 3) # Plot trend curve
		#print result[1]
	else:
		ax2.plot(fdts, measures_to_plot[metric], label = data_legends[metric], marker = markers[metric], color = colours[metric], linewidth = 1) # Plot raw data points
		ax2.plot(result[0], result[1], label = 'Estimated ' + data_legends[metric], linestyle = '--', color = colours[metric], linewidth = 3) # Plot trend curve
		y_label += data_legends[metric].lower() + ', ' # Construct label for Y axis

### Graph legends etc
ax.set_xlabel('Week ending in') # Setting X axis label
plt.xticks(fdts) # Place X axis ticks for every week
ax.xaxis.set_major_formatter(hfmt) # Format X tick labels
ax.set_ylabel('Dollar amounts') # Setting Y axis label: remove the last comma
ax2.set_ylabel(y_label[:-2] + " (weekly)") # Setting the second Y axis label
# Place legends on the graph
ax.legend(loc = 6)
ax2.legend(loc = 2)
ax.set_ylim(ymin=0)
ax2.set_ylim(ymin=0)

if overlay_events_flag == 'y': # If overlaying events

	# Opening and reading file
	f = open(filename_milestones, 'rU')
	stats = csv.reader(f, delimiter=',')
	headers = next(stats, None)  # Skip the headers

	range_start_ms = []
	range_end_ms = []
	milestones = []
	classes = []
	y = []
	init_y = 300
	add = 0
	single_event_bad = 750
	colormap = []
	indexes = {}
	
	# To use header names to index
	for h in range(len(headers)):
		indexes[headers[h]] = h
	
	# Sort events by degree of severity
	stats = list(stats)
	stats.sort(key=lambda x: int(x[indexes['Severity']]))

	# Parse and process data
	for line in stats:
		# Parse date fields as dates
		rs = parse(line[indexes['Start Date']].strip())
		print rs
		if line[indexes['End Date']].strip().lower() == "ongoing":
			re = rs
		else:
			re = parse(line[indexes['End Date']].strip()) 
		range_start_ms.append(rs)
		range_end_ms.append(re)	
		
		# Assign marker colours according to degree of severity
		classes.append(line[indexes['Severity']])
		if line[indexes['Severity']] == '1':
			colormap.append('yellowgreen')
		elif line[indexes['Severity']] == '2':
			colormap.append('lightgreen')
		elif line[indexes['Severity']] == '3':
			colormap.append('lime')
		elif line[indexes['Severity']] == '0':
			colormap.append('black')
		elif line[indexes['Severity']] == '-1':
			colormap.append('gold')
		elif line[indexes['Severity']] == '-2':
			colormap.append('orange')
		elif line[indexes['Severity']] == '-3':
			colormap.append('red')
		
		# Y axis position of markers
		add += 10
		y_coord = init_y + add
		y.append(y_coord)
		milestones.append(line[indexes['Milestones']])
		
		if rs == re: # If same start and end date, set marker to a single point
			ax2.plot(rs, y_coord, marker = 'd', color = colormap[-1], label = line[indexes['Milestones']])
		elif (re - rs).days > 3: # If long duration events, place text on the graph itself
			ax2.text(dates.date2num(re) + 1, y_coord, line[indexes['Milestones']], fontsize=7)

	fdts_start = dates.date2num(range_start_ms) # Convert start dates to numbers
	fdts_end = dates.date2num(range_end_ms) # Convert end dates to numbers
	hfmt = dates.DateFormatter('%b %d') # Format dates
	for hl in range(len(y)): # Draw lines matching duration of events
		ax2.hlines(y[hl], fdts_start[hl], fdts_end[hl], colors = colormap[hl], linewidth = 3, label = milestones[hl])
	last = ''
	ax2.set_ylim(ymax=y[-1]+30)
	fig.canvas.mpl_connect('motion_notify_event', onpick3) # Function to show labels on mouse over

plt.show()
plt.close()
