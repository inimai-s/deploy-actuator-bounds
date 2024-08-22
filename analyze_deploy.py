# ANALYZE_DEPLOY.PY
# script to find time duration, average current value, and peak-to-peak values for each satellite actuator


from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import telemetron as tron
import matplotlib.pyplot as plt
import os
from pathlib import Path


# list of channels to look at current values of actuators
channels = [
        'satfc1x_loads_i_avi_deploy_forward',
        'satfc1x_loads_i_kae1_deploy_forward',
        'satfc1x_loads_i_kae3_deploy_forward',
        'satfc1x_loads_i_kae4_deploy_forward',
        'satfc1x_loads_i_lsw_deploy_forward',
        'satfc1x_loads_i_propavi1_deploy_forward',
        ]


# find the central spike in the current data, calculate the metrics, and plot the data
def peak_find(sat, df, channel):

   df = df[df[channel] != 0]
   df = df[np.isnan(df[channel]) == False]
   if df.shape[0] == 0:
      return
   
   # find the central peak of the data
   pts = np.array(df[channel])
   threshold = 0.05
   derivs = np.diff(pts) # derivative of current
   peaks1 = np.where(derivs[:-1] > threshold)[0] + 1 # find the areas with big derivative changes
   peaks2 = []
   for item in peaks1:
      peaks2.append(item-1)

   if len(peaks2) == 0:
      return
   
   peaks = [peaks2[0]+1,peaks2[-1]]
   for i in range(1,len(peaks2)-1):
      peaks.append(peaks2[i])
      peaks.append(peaks2[i] + 11)


   big_changes = df.iloc[list(peaks)]
   big_changes.sort_values(by='timestamp',inplace=True)

   big_changes['time_diff'] = (big_changes['timestamp'] - big_changes['timestamp'].iloc[0])
   big_changes = big_changes[big_changes['time_diff'] <= timedelta(minutes=10)] # limit the datapoints to 10 sec maximum as the actuation time is roughly 8 sec


   # plot the data with the peak identification marks
   plt.figure(figsize=(10, 6))
   plt.plot(df['timestamp'], df[channel], label=channel)
   plt.scatter(big_changes['timestamp'], big_changes[channel], color='red', label='Peaks')
   plt.xlabel('Date')
   plt.xlim(big_changes['timestamp'].iloc[0] - timedelta(seconds=5), big_changes['timestamp'].iloc[-1] + timedelta(seconds=5))
   plt.ylabel(channel)
   plt.title(f'Channel values with peaks: {sat}, {channel}')
   plt.legend()
   plt.grid(True)
   plt.savefig(f'channel_pics_FILT/{sat}_{channel}')
   plt.close()

   if big_changes.shape[0] <= 1:
      return

   total_time = big_changes['timestamp'].iloc[-1] - big_changes['timestamp'].iloc[0]

   # limit actuation period
   for i in range(1,len(big_changes['timestamp'])-1,2):
      df = df[(df['timestamp'] < big_changes['timestamp'].iloc[i]) | ((df['timestamp'] > big_changes['timestamp'].iloc[i+1]))]
   df = df[(df['timestamp'] >= big_changes['timestamp'].iloc[0]) & (df['timestamp'] <= big_changes['timestamp'].iloc[-1])]
   
   # calculate metrics
   avg_val = df[channel].mean()
   max_val = df[channel].max()
   min_val = df[channel].min()
   pk_to_pk = max_val - min_val
   
   result_df = pd.DataFrame({'Sat': [sat], 'Channel': [channel], 'Time': [total_time], 'Average': [avg_val], 'Peak to peak': [pk_to_pk]})
   result_df.to_csv('output.csv',mode='a',index=False,header=False)


# find list of V2 satellites
v2_df = pd.read_pickle('v2_sats_FILT.pkl')
v2_list = list(f'satellite{sat}' for sat in v2_df['identifier'])
directory = r"C:\Users\isubramanian\Desktop\prop_launch\df_pkls"

for name in os.listdir(directory):

   if Path(name).stem not in v2_list:
      continue
   
   filt_df = pd.read_pickle(f'df_pkls/{name}')
   filt_df['timestamp'] = pd.to_datetime(filt_df['timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
   for channel in channels:
      peak_find(Path(name).stem, filt_df, channel)
