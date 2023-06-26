import pandas as pd
import os
import subprocess
from pathlib import Path
import argparse
import datetime

 #hello
def main():
    parser = argparse.ArgumentParser(
        #prog='ProgramName',
        description='Crops and trims videos according to parameters',
        epilog='written by PB under JHU REU')

    parser.add_argument('csv', help='Required CSV file with details of all videos (video_id, etc)')           # positional argument
    parser.add_argument('-r', '--root', type=str, default='D:/', help="Root directory")
    parser.add_argument('-i', '--input', type=str, default='HerniaVid', help='Folder name for input videos under root')
    parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag    

    args = parser.parse_args()
    #print(args.csv, args.verbose)

    #csv = root / 'raw_data_config.csv'
    csv = args.csv
    # root folder for all data and config
    root = Path(args.root)
    dir = root / args.input #'HerniaVid'

    # read config
    df = pd.read_csv(csv)


    # loop through dataframe
    for index, row in df.iterrows():
        vid = int(row["video_id"])
        vid_str = str(row["video_id"])
        fname = f'{vid}.mp4'
        print (fname)

        mesh_video = str(row["mesh_file"])
        mrecords = f'''{mesh_video}.mkv'''
        print (mrecords)

        filename = dir / fname
        print(filename)

        meshfile = dir / mrecords
        print(meshfile)

        if not (dir/fname).exists():
            print(f'''{fname} does not exist''')
            continue
       # if not (dir/mrecords).exists():
            #continue

        # create new directory
        path_file = f'''C:/Users/petra/REU/'''

        # Check if the directory exists
        path_cal = 'C:/Users/petra/REU/Calibration_videos'
        if not os.path.exists(path_cal):
            # If it doesn't exist, create it
            os.makedirs(path_cal)

        path_endo = 'C:/Users/petra/REU/Endoscope_videos'
        if not os.path.exists(path_endo):
            # If it doesn't exist, create it
            os.makedirs(path_endo)

        path_over = 'C:/Users/petra/REU/OverHead_videos'
        if not os.path.exists(path_over):
            # If it doesn't exist, create it
            os.makedirs(path_over)

        path_mesh = 'C:/Users/petra/REU/Mesh_records'
        if not os.path.exists(path_mesh):
            # If it doesn't exist, create it
            os.makedirs(path_mesh)
       
        #calibration 
        cal = "calibration"
        start = str(row["calibration_start_time"])
        end = str(row["calibration_end_time"])
        w1, h1, x1, y1 = 546, 308, 0, 360
        vid_cal = f'''ffmpeg -i {filename} -filter:v "crop={w1}:{h1}:{x1}:{y1}" -ss {start} -to {end} {vid}_{cal}.mp4'''
        print (vid_cal)
        subprocess.run(vid_cal)
        os.rename(f'''{path_file}/{vid}_{cal}.mp4''', f'''{path_cal}/{vid}_{cal}.mp4''')

        #Overhead 
        ovr = "overhead"
        start2 = str(row["task_start_time"])
        end2 = str(row["task_end_time"])
        vid_cal2 = f'''ffmpeg -i {filename} -filter:v "crop={w1}:{h1}:{x1}:{y1}" -ss {start2} -to {end2} {vid}_{ovr}.mp4'''
        #print (vid_cal2)
        #subprocess.run(vid_cal2)
        #os.rename(f'''{path_file}/{vid}_{ovr}.mp4''', f'''{path_over}/{vid}_{ovr}.mp4''')

        #endoscope 
        endo = "endoscope"
        w2, h2, x2, y2 = 640, 360, 640, 360
        vid_cal3 = f'''ffmpeg -i {filename} -filter:v "crop={w2}:{h2}:{x2}:{y2}" -ss {start2} -to {end2} {vid}_{endo}.mp4'''
        #print (vid_cal3)
        #subprocess.run(vid_cal3)
        #os.rename(f'''{path_file}/{vid}_{endo}.mp4''', f'''{path_endo}/{vid}_{endo}.mp4''')

        #mesh records
        mesh = "mesh_records"
        start3 = str(row["mesh_start"])
        end3 = str(row["mesh_end"])
        vid_cal3 = f'''ffmpeg -i {meshfile} -ss {start3} -to {end3} {vid}_{mesh}.mkv'''
        #print (vid_cal3)
        #subprocess.run(vid_cal3)
        #os.rename(f'''{path_file}/{vid}_{mesh}.mkv''', f'''{path_mesh}/{vid}_{mesh}.mkv''')

                  
if __name__=='__main__':
    main()

def merge():

    parser = argparse.ArgumentParser()  
    parser.add_argument('--folder', type=str, default='C:/Users/petra/REU/Processed_Data/')
    args = parser.parse_args()
 
    #read the path
    #file_path = "C:/Users/petra/REU/Processed_Data"
    #list all the files from the directory
    folder = Path(args.folder)
    file_list = os.listdir(folder)
    print(file_list)

    # Read the CSV files into DataFrames
    df1 = pd.read_csv(f'''{folder}/processed_data_config.csv''')
    df2 = pd.read_csv(f'''{folder}/ACS 2022 Post-Survey_sharing.csv''')
    df3 = pd.read_csv(f'''{folder}/ACS 2022 Pre-Survey_Sharing.csv''')
    df4 = pd.read_csv(f'''{folder}/Data Sanity Check - Master.csv''')
    df5 = pd.read_csv(f'''{folder}/Mesh Annotations - Sheet1.csv''')
    
    # Merge the DataFrames on columns with different names
    merged_df = df1.merge(df2, left_on='video_id', right_on='Participant #', how='outer')
    merged_df = merged_df.merge(df3, left_on='video_id', right_on='Participant #', how='outer')
    merged_df = merged_df.merge(df4, left_on='video_id', right_on='Motion PID', how='outer')
    merged_df = merged_df.merge(df5, left_on='video_id', right_on='Participant I.D.', how='outer')

    # Write the merged DataFrame to a new CSV file
    merged_df.to_csv("merged_processed_data.csv", index=False)

#merge()


#Motion data

dt = datetime.datetime.fromtimestamp(1666211163.084 )
print(dt)
