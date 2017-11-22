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
- When prompted, enter the names of the data files, and the columns corresponding to the different data types
- Note that if you choose to overlay the event info on the timeline graph, events with a duration of 2 days or longer show up on the graph along with their name or a short description, and shorter-duration events only show up as markers, that display the name when hovering over the marker

Data file specifications:
------------------------
- Ensure that all columns have a header

- For the file containing business' performance metrics
  - There must be at least one column of numeric data that is to be plotted
  - Plots are along a timeline, on a per week basis, so ensure that each record has a 'Date range' column with a start date and an end date for the week

- For the file containing event data
  - Events should be classified as strongly negative (-3) and strongly positive (3), which is then represented on a red to green spectrum on the graph
  - Plots are along a timeline, on a per week basis, so ensure that each record has a 'Date range' column with a start date and an end date for the week
  - There should be a column containing the name or a short description of the event that can be displayed on the graph
