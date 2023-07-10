import pandas as pd
from pathlib import Path
import os
import numpy as np
import argparse

parser = argparse.ArgumentParser(
        #prog='ProgramName',
        description='Interpolate motion data')

parser.add_argument('csv', help='Required CSV file with details of all videos (video_id, etc)')           # positional argument
parser.add_argument('-r', '--root', type=str, default='D:/', help="Root directory")
parser.add_argument('-i', '--input', type=str, default='Kinematic_data', help='Folder name for input videos under root')

args = parser.parse_args()

# location of data 
root = Path(args.root)
dir = root / args.input

csv = args.csv
#csv = 'C:/Users/petra/REU/unix_videos.csv'
dfv = pd.read_csv(csv)

# Loop over videos
for index, row in dfv.iterrows():
    file = int(row["video_id"])
    fname = f'''{file}.txt'''
    print (fname)

    filename = f'''{dir}/{fname}'''
    print(filename)
    filepath = Path(filename)

    # Get all 88 column names (will look like "sensor_6_azimuth")
    col_names = ["name", "status", "x", "y", "z", "azimuth", "elevation", "roll", "button", "quality", "time"]
    cols = []
    for sensor_num in range(8):
        for col_name in col_names:
            cols.append(f"sensor_{sensor_num}_{col_name}")

    # Read all sensor data into one dataframe
    df = pd.read_csv(filename, sep='\s+', header=0, names=cols)

    # Separate out each sensor into its own dataframe
    sensor_dfs = []
    for sensor_num in range(8):
        sensor_cols = [f"sensor_{sensor_num}_{col_name}" for col_name in col_names]
        # Rename ("sensor_6_azimuth" -> "azimuth") since sensor name isn't needed anymore
        sensor_df = df[sensor_cols].rename({sc: c for sc,c in zip(sensor_cols, col_names)}, axis=1)
        sensor_dfs.append(sensor_df)
        #print(sensor_df)
        
    # Frames per second
    fps = 30
    
    # Iterate through the unix start and end times for tasks
    start_timestamp = row['unix_start']
    end_timestamp = row['unix_end']

    # Total number of frames
    frames = int(np.floor((end_timestamp - start_timestamp) * fps))
  

    # New dataframe for the time of each frame
    f = np.arange(frames) # array of frame numbers 0,1,2...,frames-1
    t = start_timestamp + f / fps #time at each frame
    times = pd.DataFrame({'time': t, 'frame': f})
    #print(times)

    # Create empty list for sensor dataframes
    merged_dfs = []
    for sensor_index, sensor_df in enumerate(sensor_dfs):
        sensor_num = sensor_index + 1
        #print(sensor_df)

        # Test time intervals
        assert times.time.values[0] > sensor_df.time.values[0], 'starting violation'
        assert times.time.values[-1] < sensor_df.time.values[-1], 'ending violation'

        # Merge motion data times and frame times
        merged_df = times.merge(sensor_df, how='outer', on='time')
       
        # Sort the unix times column in numerical order 
        merged_df = merged_df.sort_values(by=['time'])
        # Set column as index
        merged_df.set_index('time', inplace=True)
        

        # Sensor columns to interpolate (not all columns are interpolated)
        sensor_cols = list(sensor_df.columns) # everything kinematic file
        for c in ['status', 'time']: # excluding these columns
            sensor_cols.remove(c)
        #print (sensor_cols)
        
        # Interpolates the selected columns based on index (time)
        for c in sensor_cols:
            merged_df[c].interpolate(inplace=True, method='index')
   
        # Delete rows that do not have a frame number - get sensor values only for frames
        merged_df = merged_df[merged_df['frame'].notna()]

        # Insert column for sensor number
        merged_df.insert(0, 'sensor_num', sensor_num * np.ones(len(merged_df), dtype=np.uint8))
        
        # Add to empty list created eariler
        merged_dfs.append(merged_df)

        
    # Merge sensor data back together from list of 8 dataframes
    all_df = pd.concat(merged_dfs)

    #Clean-up
    all_df.reset_index(inplace=True)
    all_df = all_df.sort_values(by=['time', 'sensor_num' ])
    all_df = all_df.drop(['name', 'status'], axis=1)

    # Save the DataFrame to a CSV file
    output = Path(f'''{file}_kinematics.csv''')
    # delete output csv if already exists
    if output.exists():
        output.unlink() 
    all_df.to_csv(output, index=False)

    # end of loop over sensors

# end of loop over videos

