# OUTPUT_HISTOS.PY
# script that outputs histograms of average current, time duration, and peak-to-peak values for each channel

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = pd.read_csv('output.csv')

# list of bad satellites that do not deploy correctly on telemetron - disregard
bad_sats = [f'satellite{num}' for num in range(30752,30978)]
bad_sats.extend(['satellite31076','satellite31145','satellite31150','satellite31156','satellite31176','satellite31180'])
good_sats = ['satellite30828','satellite30856','satellite30857','satellite30862','satellite30863',
             'satellite30893','satellite30932','satellite30936','satellite30941','satellite30945',
             'satellite30947','satellite30948','satellite30953','satellite30956','satellite30965',
             'satellite30968','satellite30970','satellite30972','satellite30973','satellite30974']
final_bad_sats = [badsat for badsat in bad_sats if badsat not in good_sats]
df = df[~df['Sat'].isin(final_bad_sats)]


df['Sec'] = pd.to_timedelta(df['Time'])
df['Sec'] = df['Sec'].dt.total_seconds()


# output histogram of distribution of actuation time
def time_histo(df):
    plt.figure(figsize=(10, 4))
    plt.hist(df['Sec'], bins=20,range=(int(min(df['Sec'])), math.ceil(max(df['Sec'])) + 1), edgecolor='black')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Time (s) of Deploy: {df['Channel'].iloc[0]}')
    plt.show()
    plt.close()


# output histogram of distribution of average current value
def avg_histo(df):
    plt.figure(figsize=(10, 4))
    a = plt.hist(df['Average'], bins=20,range=(0, 0.3), edgecolor='black')
    plt.xlabel('Average Channel Value')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Average Channel Value of Deploy: {df['Channel'].iloc[0]}')
    plt.show()
    plt.close()


# output histogram of distribution of peak-to-peak current value
def pk_histo(df):
    plt.figure(figsize=(10, 4))
    plt.hist(df['Peak to peak'], bins=20,range=(0, 0.15), edgecolor='black')
    plt.xlabel('Peak-to-peak Channel Value')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Peak-to-peak Channel Value of Deploy: {df['Channel'].iloc[0]}')
    plt.show()
    plt.close()


# output duration, average, and peak-to-peak values
def output_stats(df):
    print(df['Channel'].iloc[0])
    print(f'time: {df['Sec'].mean()}')
    print(f'avg: {df['Average'].mean()}')
    print(f'pk: {df['Peak to peak'].mean()}')
    print()


# list of channels to look at current values of actuators
channels = [
        'satfc1x_loads_i_avi_deploy_forward',
        'satfc1x_loads_i_kae1_deploy_forward',
        'satfc1x_loads_i_kae3_deploy_forward',
        'satfc1x_loads_i_kae4_deploy_forward',
        'satfc1x_loads_i_lsw_deploy_forward',
        'satfc1x_loads_i_propavi1_deploy_forward',
        ]


for channel in channels:
    filt = df[df['Channel'] == channel]
    time_histo(filt)
    avg_histo(filt)
    pk_histo(filt)
    output_stats(filt)
