import pandas as pd
import os
import subprocess
from pathlib import Path
import argparse

def main():
    parser = argparse.ArgumentParser(
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

    # Read config
    df = pd.read_csv(csv)


    # Loop through videos
    for index, row in df.iterrows():
        vid = int(row["video_id"])
        fname = f'{vid}.mp4'
        print (fname)

        # Loop through mesh records videos
        mesh_video = str(row["mesh_file"])
        mrecords = f'''{mesh_video}.mkv'''
        print (mrecords)

        filename = dir / fname
        print(filename)

        meshfile = dir / mrecords
        print(meshfile)

        # Can't find the video
        if not (dir/fname).exists():
            print(f'''{fname} does not exist''')
            continue
      

        # Create new directory for processed videos
        path_file = f'''C:/Users/petra/REU/'''

        # Check if the directory exists
        path_cal = 'C:/Users/petra/REU/Calibration_videos'
        if not os.path.exists(path_cal):
            # If it doesn't exist, create it
            os.makedirs(path_cal)

        path_endo = 'C:/Users/petra/REU/Endoscope_videos'
        if not os.path.exists(path_endo):
            os.makedirs(path_endo)

        path_over = 'C:/Users/petra/REU/OverHead_videos'
        if not os.path.exists(path_over):
            os.makedirs(path_over)

        path_mesh = 'C:/Users/petra/REU/Mesh_records'
        if not os.path.exists(path_mesh):
            os.makedirs(path_mesh)
       
        # Calibration video
        cal = "calibration"
        # Start and end times of calibration
        start = str(row["calibration_start_time"])
        end = str(row["calibration_end_time"])

        # Some videos do not have calibration - skip this part for those videos
        if start is None:
            continue

        # Bounding box for cropped video
        w1, h1, x1, y1 = 546, 308, 0, 360

        # Trim and crop in ffmpeg
        vid_cal = f'''ffmpeg -i {filename} -filter:v "crop={w1}:{h1}:{x1}:{y1}" -ss {start} -to {end} {vid}_{cal}.mp4'''
        print (vid_cal)
        subprocess.run(vid_cal)
        
        # Move to designated directory
        os.rename(f'''{path_file}/{vid}_{cal}.mp4''', f'''{path_cal}/{vid}_{cal}.mp4''')

        # Overhead video 
        ovr = "overhead"
        start2 = str(row["task_start_time"])
        end2 = str(row["task_end_time"])
        vid_cal2 = f'''ffmpeg -i {filename} -filter:v "crop={w1}:{h1}:{x1}:{y1}" -ss {start2} -to {end2} {vid}_{ovr}.mp4'''
        print (vid_cal2)
        subprocess.run(vid_cal2)
        os.rename(f'''{path_file}/{vid}_{ovr}.mp4''', f'''{path_over}/{vid}_{ovr}.mp4''')

        # Endoscope video
        endo = "endoscope"
        w2, h2, x2, y2 = 640, 360, 640, 360
        vid_cal3 = f'''ffmpeg -i {filename} -filter:v "crop={w2}:{h2}:{x2}:{y2}" -ss {start2} -to {end2} {vid}_{endo}.mp4'''
        print (vid_cal3)
        subprocess.run(vid_cal3)
        os.rename(f'''{path_file}/{vid}_{endo}.mp4''', f'''{path_endo}/{vid}_{endo}.mp4''')

        # Mesh records video
        mesh = "mesh_records"
        start3 = str(row["mesh_start"])
        end3 = str(row["mesh_end"])
        vid_cal3 = f'''ffmpeg -i {meshfile} -ss {start3} -to {end3} {vid}_{mesh}.mkv'''
        print (vid_cal3)
        subprocess.run(vid_cal3)
        os.rename(f'''{path_file}/{vid}_{mesh}.mkv''', f'''{path_mesh}/{vid}_{mesh}.mkv''')

                  
if __name__=='__main__':
    main()

