# Deploy Actuator Parameter Bounds
Script that determines the correct alert bounds for current values of deploy actuators

# Script: analyze_deploy.py
Run to find time duration, average current value, and peak-to-peak values for each satellite actuator

# Script: output_histos.py / output_histos_by_launch.py
Run to output histograms of average current, time duration, and peak-to-peak values for each channel and categorize by launch

# Installation python packages:
- pandas
- numpy
- matplotlib.pyplot
- math
- datetime
- sx-telemetron
- os
- pathlib

Initialize empty output.csv with a header
