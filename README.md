Visualizing Business Trends
=========

Python scripts to visualize and analyze how a business' key metrics are affected by user-curated notable events or milestones.
Includes sample data which can be used as a template for the input files.
To use your own data, annotate notable events with date when it occurred, date till when its effect lasted, and severity of the effect on a scale of -3 to 3, where -3 is an event with a strong negative effect, and 3 is an event with a strong positive effect. They are presented colour-coded on the graph for easy and immediate visualization.

Getting started:
----------------
- Download the script and sample files
- Open your preferred command line interface
 - Navigate to the folder with the script and data files
 - Run script: `python milestones.py`
 - When prompted, enter `y` to overlay important events on the timeline, or enter `n` to skip
 - When prompted, enter the names of the data files

Data file specifications
------------------------
- Ensure that all columns have a header
- File containing business' performance metrics must have at least one column of numeric data that is to be plotted
- Plots are along a timeline, on a per week basis, so ensure that each record has a 'Date range' column with a start date and an end date for the week
- Events are classified as strongly negative (-3) and strongly positive (3) and colour-coded on a red to green spectrum
