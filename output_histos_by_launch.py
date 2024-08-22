# OUTPUT_HISTOS_BY_LAUNCH.PY
# script that outputs histograms of average channel values by launch group

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = pd.read_csv('output.csv')
satdf = pd.read_pickle('v2_sats_FILT.pkl')

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


# output histograms of distributions for each actuator current value by launch group
def avg_histo(df,launch):
    plt.figure(figsize=(10, 4))
    a = plt.hist(df['Average'], bins=20,range=(0, 0.3), edgecolor='black')
    plt.axvline(df['Average'].mean(),color='k',linestyle='dashed',linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    plt.text((df['Average'].mean())*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(df['Average'].mean()))
    plt.xlabel('Average Channel Value')
    plt.ylabel('Frequency')
    plt.title(f'Histogram of Average Channel Value of Deploy: {df['Channel'].iloc[0]}: {launch}')
    plt.savefig(f'histos_by_launch/{launch}_{channel}')
    plt.close()


# output statistics of the average channel value
def output_stats(df,launch):
    print(df['Channel'].iloc[0], launch)
    print(f'avg: {df['Average'].mean()}')
    print()
    return df['Average'].mean()


# list of channels to look at current values of actuators
channels = [
        'satfc1x_loads_i_avi_deploy_forward',
        'satfc1x_loads_i_kae1_deploy_forward',
        'satfc1x_loads_i_kae3_deploy_forward',
        'satfc1x_loads_i_kae4_deploy_forward',
        'satfc1x_loads_i_lsw_deploy_forward',
        'satfc1x_loads_i_propavi1_deploy_forward',
        ]


# output histograms and average values for each launch group
for channel in channels:
    for launch in set(satdf['launch_name']):
        launchdf = satdf[satdf['launch_name'] == launch]
        launch_sats_list = [f'satellite{sat}' for sat in set(launchdf['identifier'])]
        filt = df[(df['Channel'] == channel) & (df['Sat'].isin(launch_sats_list))]

        if filt.shape[0] == 0:
            continue

        mean = output_stats(filt,launch)
        result_df = pd.DataFrame({'launch': [launch], 'channel': [channel], 'average': [mean]})
        result_df.to_csv('avgs_by_launch_FULL.csv',mode='a',index=False,header=False)
