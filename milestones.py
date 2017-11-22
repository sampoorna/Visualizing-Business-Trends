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
	overlay_events_flag = raw_input("Overlay event information? (Y/N) ").lower()
	if (overlay_events_flag != 'y' and overlay_events_flag != 'n'):
		invalid_response = True
	else:
		invalid_response = False

# Take file name as command line input
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

# Take second file name as command line input
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
plot_from_start = True

while (invalid_response):
	plot_date_start = raw_input("Plot data on the graph from date (DD/MM/YY). Type '/' to use the start of the data file: ")
	
	if plot_date_start == '/':
		plot_from_start = True
		invalid_response = False
		print "Plotting from the beginning of the data file..."
	else:
		try: 
			plot_date_start = parse(plot_date_start)
			invalid_response = False
		except:
			print "Input does not appear to be a date :S Please try again!"
		
invalid_response = True
plot_till_end = True

while (invalid_response):
	plot_date_end = raw_input("Plot data on the graph till date (DD/MM/YY). Type '/' to plot till the end of the data file: ")
	
	if plot_date_end == '/':
		plot_till_end = True
		invalid_response = False
		print "Plotting till the end of the data file..."
	else:
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
second_axis_columns = raw_input("Choose column(s) that contain(s) second Y-axis values (separate numbers by space). Type 0 if all columns are to be plotted on the first axis only: ")
second_axis_columns = [int(i) - 1 for i in second_axis_columns.split(' ')]

if second_axis_columns[0] == -1:
	first_axis_only = True
	columns_to_plot = first_axis_columns
else:
	first_axis_only = False
	columns_to_plot = list(set().union(first_axis_columns, second_axis_columns))

date_range_start = []
date_range_end = []
measures_to_plot = [[] for i in range(len(data_headers))] # Initialize array to appropriate size
data_index_second_axis = -1
y_label = 'Number of '

colours = ['purple', 'teal', 'orchid', 'C3', 'C4', 'C5']
markers = ['+', 'o', '*', '+', 'o', '*']
data_legends = data_headers

# Parse and process data
for line in stats:
	# Parse date fields as dates
	rs = parse(line[date_column_index].split('-')[0].strip())
	re = parse(line[date_column_index].split('-')[1].strip())
	
	if plot_from_start or rs >= plot_date_start:
		date_range_start.append(rs)
	
	if plot_till_end or (re <= plot_date_end):
		date_range_end.append(re)
	
	# Iterate over all columns and read in data fields
	for metric in columns_to_plot:
		value = line[metric]
		measures_to_plot[metric].append(float(value.replace(',', '').replace('$', ''))) # Strip out commas from numeric values and convert to float
		
x_axis_dates = dates.date2num(date_range_end) # Convert dates to numbers
formatted_dates = dates.DateFormatter('%b %d') # Format dates
fig = plt.figure()
ax = fig.add_subplot(111)

if not first_axis_only:
	ax2 = ax.twinx()

for metric in columns_to_plot:

	result = curve_fit(x_axis_dates, measures_to_plot[metric]) # Fit curve to data points to estimate trend
	if not first_axis_only and metric in second_axis_columns:
		ax2.plot(x_axis_dates, measures_to_plot[metric], label = data_legends[metric], marker = markers[metric], color = colours[metric], linewidth = 1) # Plot raw data points
		ax2.plot(result[0], result[1], label = 'Estimated ' + data_legends[metric], linestyle = '--', color = colours[metric], linewidth = 3) # Plot trend curve
	else:
		ax.plot(x_axis_dates, measures_to_plot[metric], label = data_legends[metric], marker = markers[metric], color = colours[metric], linewidth = 1) # Plot raw data points
		ax.plot(result[0], result[1], label = 'Estimated ' + data_legends[metric], linestyle = '--', color = colours[metric], linewidth = 3) # Plot trend curve
		y_label += data_legends[metric].lower() + ', ' # Construct label for Y axis

### Graph legends etc
ax.set_xlabel('Week ending in') # Setting X axis label
plt.xticks(x_axis_dates) # Place X axis ticks for every week
ax.xaxis.set_major_formatter(formatted_dates) # Format X tick labels
ax.set_ylabel('Dollar amounts') # Setting Y axis label: remove the last comma

if not first_axis_only:
	ax2.set_ylabel(y_label[:-2] + " (weekly)") # Setting the second Y axis label

# Place legends on the graph
ax.legend(loc=6)
ax.set_ylim(ymin=0)

if not first_axis_only:
	ax2.legend(loc=2)
	ax2.set_ylim(ymin=0)

if overlay_events_flag == 'y': # If overlaying events

	date_range_start_events = []
	date_range_end_events = []
	milestones = []
	classes = []
	y = []
	init_y = 300
	add = 0
	single_event_bad = 750
	colormap = []
	indexes = {}
	
	# Ask user which metric to plot on which axis
	print "Found following data headers: "
	for i in range(len(event_data_headers)):
		print "(" + str(i + 1) + ") " + event_data_headers[i]

	severity_column_index = input("Choose column that contains severity values (on a scale of -3 to 3): ") - 1
	milestones_column_index = input("Choose column that contains event descriptions/names: ") - 1
	start_date_column_index = input("Choose column that has start date for event: ") - 1
	end_date_column_index = input("Choose column that has end date for event: ") - 1
	
	# To use header names to index
	for h in range(len(event_data_headers)):
		indexes[event_data_headers[h]] = h
	
	# Sort events by degree of severity
	event_data = list(event_data)
	event_data.sort(key=lambda x: int(x[severity_column_index]))

	# Parse and process data
	for line in event_data:
		# Parse date fields as dates
		rs = parse(line[start_date_column_index].strip())
		print rs
		if line[end_date_column_index].strip().lower() == "ongoing":
			re = rs
		else:
			re = parse(line[end_date_column_index].strip()) 
		
		if (plot_from_start or rs >= plot_date_start):
			date_range_start_events.append(rs)
		if (plot_till_end or re <= plot_date_end):
			date_range_end_events.append(re)
		
		# Assign marker colours according to degree of severity
		classes.append(line[severity_column_index])
		if line[severity_column_index] == '1':
			colormap.append('yellowgreen')
		elif line[severity_column_index] == '2':
			colormap.append('lightgreen')
		elif line[severity_column_index] == '3':
			colormap.append('lime')
		elif line[severity_column_index] == '0':
			colormap.append('black')
		elif line[severity_column_index] == '-1':
			colormap.append('gold')
		elif line[severity_column_index] == '-2':
			colormap.append('orange')
		elif line[severity_column_index] == '-3':
			colormap.append('red')
		
		# Y axis position of markers
		add += 10
		y_coord = init_y + add
		y.append(y_coord)
		milestones.append(line[milestones_column_index])
		
		if rs == re: # If same start and end date, set marker to a single point
			ax2.plot(rs, y_coord, marker = 'd', color = colormap[-1], label = line[milestones_column_index])
		elif (re - rs).days > 3: # If long duration events, place text on the graph itself
			ax2.text(dates.date2num(re) + 1, y_coord, line[milestones_column_index], fontsize=7)

	fdts_start = dates.date2num(date_range_start_events) # Convert start dates to numbers
	fdts_end = dates.date2num(date_range_end_events) # Convert end dates to numbers
	formatted_dates = dates.DateFormatter('%b %d') # Format dates
	for hl in range(len(y)): # Draw lines matching duration of events
		ax2.hlines(y[hl], fdts_start[hl], fdts_end[hl], colors = colormap[hl], linewidth = 3, label = milestones[hl])
	print len(y)
	last = ''
	ax2.set_ylim(ymax=y[-1]+30)
	fig.canvas.mpl_connect('motion_notify_event', onpick3) # Function to show labels on mouse over

plt.show()
plt.close()
