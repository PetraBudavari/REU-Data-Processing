from pathlib import Path
import pandas as pd
import numpy as np
import argparse

from IPython.display import display
pd.set_option("display.precision", 10) 

def parse(filepath, sensor_id, max_lines=5, header_startswith='Format for each'):
    '''Parse a kinematics file'''

    with filepath.open('r') as f:

        # read header info
        header = f.readline()
        if header_startswith:
            # check for header where the columns names are for the sensors
            if not header.startswith(header_startswith): 
                return None
            
        # loop over the lines of sensor data
        for line_number, line in enumerate(f.readlines()):
            if max_lines and line_number < max_lines:
                sensor = line.split('Sensor')
                # pick the correct sensor
                s = sensor[sensor_id]
                # split the data and exclude first item with the sensor id
                t = s.split()[1:]
                # this generator yields every item one by one
                yield t

# location of data 
root = Path('D:\\')
dir = root / 'Kinematic_data' 

# find all kinematics files in the folder
file_list = list(dir.glob('*_kinematics.txt'))
file_list

# use just one kinematics file
fn = file_list[0]
print (fn)

colnames = ['status', 'x', 'y', 'z', 'azimuth', 'elevation', 'roll', 'button', 'quality', 'time']

sensor_id = 2
max_lines = 1000 # for testing

df = pd.DataFrame(columns=colnames)

# load dataframe row by row
for row in parse(fn, sensor_id, max_lines):
    df.loc[len(df)] = row

# convert columns one by one
coltypes = dict(
    x=np.float32, y=np.float32, z=np.float32, 
    azimuth=np.float32, elevation=np.float32, roll=np.float32, 
    button=np.int8, quality=np.int8
    )

for c,t in coltypes.items():
    df[c] = df[c].astype(t)

df['t'] = df.time.astype(np.float64)

#df['video_time'] = df.t - df.t[0]

print (df.time[0], df.t[0])
print(df.dtypes)
df

def interpolation(args = None):
    parser = argparse.ArgumentParser(
        description='Interolation of motion data on video frames')

    parser.add_argument('csv_unix', help='File of Start and End UNIX timestamps for processed videos')       
    parser.add_argument('-f', '--fps', default=30, help="Frame rate")

    args = parser.parse_args()
    csv = args.csv_unix

    #csv = 'C:/Users/petra/REU/unix_videos.csv'
    dfv = pd.read_csv(csv)

    # loop over videos - iterate through the unix start and end times for tasks
    for index, row in dfv.iterrows():

        # useful time interval
        start_timestamp = row['unix_start_time']
        end_timestamp = row['unix_end_time']
        
        # total number of frames
        frames = int(end_timestamp - start_timestamp) * args.fps

        # new dataframe for the time of each frame
        f = np.arange(frames) # array of frame numbers 0,1,2...,frames-1
        t = start_timestamp + f / args.fps
        times = pd.DataFrame({'t': t, 'frame': f})

        # test time intervals
        #assert times.t.values[0] > df.t.values[0], 'starting violation'
        #assert times.t.values[-1] < df.t.values[-1], 'ending violation'

        #join the motion data and the frame times data frames 
        merged_df = times.merge(df, how='outer', on='t')
        display(merged_df)

        # sort the unix times column in numerical order 
        merged_df = merged_df.sort_values('t')
        # set as index
        merged_df.set_index('t', inplace=True)

        # sensor columns to interpolate are all but a few
        sensor_cols = list(df.columns) # everything kinematic file
        for c in ['t', 'status', 'time']: # excluding these columns
            sensor_cols.remove(c)
        print (sensor_cols)

        # interpolate selected columns in place 
        for c in sensor_cols:
            merged_df[c].interpolate(inplace=True, method='linear')

        # exclude rows without frame numbers, i.e., NaN 
        merged_df = merged_df[merged_df.frame.apply(lambda f: f >= 0)]

        display(merged_df)

        # Save the DataFrame to a CSV file
        video = int(row['video_id'])
        output = Path(f'''{video}_Sensor{sensor_id}.csv''')
        # delete output csv if already exists
        if output.exists():
            output.unlink() 
        merged_df.to_csv(output, index=False)

        
        

interpolation()
