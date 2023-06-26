from pathlib import Path
import pandas as pd
import numpy as np
import argparse


pd.set_option("display.precision", 13)


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
max_lines = 100 # fir testig

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

df['video_time'] = df.t - df.t[0]

print (df.time[0], df.t[0])
print(df.dtypes)
df

def interpolation():
    #parser = argparse.ArgumentParser(
        #description='Interolation of motion data on video frames')

    #parser.add_argument('csv_unix', help='File of Start and End UNIX timestamps for processed videos')       
    #parser.add_argument('-f', '--fps', default=30, help="Frame rate")

    #args = parser.parse_args()
    #csv = args.csv_unix
    csv = 'C:/Users/petra/REU/unix_videos.csv'
    df2 = pd.read_csv(csv)


    # iterate through the unix start and end times for tasks
    for index, row in df2.iterrows():
        start_timestamp = int(row['unix_start _time'])
        end_timestamp = int(row['unix_end_time'])


        start_value = 0 #first frame
        
        #total number of frames
        #frames = (end_timestamp - start_timestamp) * 30
        frames = 100

        #create new data frame from frame time and frame number
        times = pd.DataFrame(columns=['time', 'frame'])

        for i in range(frames):

            start_value += 1
            
            #find unix time at each frame
            #frame_time = start_timestamp + (i * (1/args.fps))
            frame_time = start_timestamp + (i * (1/30))
            

            #add the frame times to the previously created dataframe
            new_row = pd.DataFrame({'time': [frame_time], 'frame': [i]})
            times['time'] = times['time'].astype('float64')
            times = pd.concat([times, new_row], ignore_index=True)


            #join the motion data and the frame times data frames 
            merged_df = pd.merge(times, df, left_on='time', right_on='t', how='outer')

            #merge the two time column in the new joined dataframe
            merged_df['time_x'] = merged_df['time_x'].fillna(0)
            merged_df['t'] = merged_df['t'].fillna(0)
            #now we have one column with both the motion data timestamps and the frame timestamps
            merged_df['combined_times'] = merged_df['time_x'].astype('float64') + merged_df['t'].astype('float64')

            #sort the unix times column in numerical order 
            merged_df = merged_df.sort_values('combined_times')
            #make it the index
            merged_df.set_index('combined_times', inplace=True)

            #clean up
            columns_to_delete = ['time_x', 'time_y', 't', 'video_time']
            merged_df = merged_df.drop(columns_to_delete, axis=1)

            #interpolate along the index
            df_interpolated = merged_df.interpolate(method='linear')


            #Save the DataFrame to a CSV file
            video = int(row['video_id'])
            output = f'''{video}_{sensor_id}.csv'''
            df_interpolated.to_csv(output, index=False)

            # Print the interpolated dataframe
            print(df_interpolated)

        

interpolation()