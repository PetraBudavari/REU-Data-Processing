import pandas as pd
import os
import subprocess
from pathlib import Path


def main():
    # root folder for videos
    root = Path('D:/')
    dir = root / 'HerniaVid' #'HerniaVid'
    csv = 'C:\Users\petra\REU\raw_data_config.csv'


    # read config
    df = pd.read_csv(csv)

    # loop through dataframe
    for index, row in df.iterrows():
        vid = int(row["video_id"])
        vid_str = str(row["video_id"])
        fname = f'{vid}.mp4'
        print (fname)
        filename = dir / fname
        print(filename) 

        # create new directory
        path = 'C:/Users/petra/REU/' + vid_str
        os.mkdir(path)
        
        #calibration 
        cal = "calibration"
        start = str(row["calibration_start_time"])
        end = str(row["calibration_end_time"])
        w1, h1, x1, y1 = 546, 308, 0, 360
        vid_cal = f'''ffmpeg -i {filename} -filter:v "crop={w1}:{h1}:{x1}:{y1}" -ss {start} -to {end} {vid}"_"{cal}.mp4'''
        print (vid_cal)
        subprocess.run(vid_cal)

        os.rename('C:/Users/petra/REU/' + vid_str + "_" + cal + ".mp4", 'C:/Users/petra/REU/' + vid_str + "/" + vid_str + "_"+ cal + ".mp4")

        #Overhead 
        ovr = "overhead"
        start2 = str(row["task_start_time"])
        end2 = str(row["task_end_time"])
        vid_cal2 = f'''ffmpeg -i {filename} -filter:v "crop={w1}:{h1}:{x1}:{y1}" -ss {start2} -to {end2} {vid}"_"{ovr}.mp4'''
        print (vid_cal2)
        subprocess.run(vid_cal2)
        os.rename('C:/Users/petra/REU/' + vid_str + "_" + ovr + ".mp4", 'C:/Users/petra/REU/' + vid_str + "/" + vid_str + "_"+ ovr + ".mp4")

        #endoscope 
        endo = "endoscope"
        w2, h2, x2, y2 = 640, 360, 640, 360
        vid_cal3 = f'''ffmpeg -i {filename} -filter:v "crop={w2}:{h2}:{x2}:{y2}" -ss {start2} -to {end2} {vid}"_"{endo}.mp4'''
        print (vid_cal3)
        subprocess.run(vid_cal3)
        os.rename('C:/Users/petra/REU/' + vid_str + "_" + endo + ".mp4", 'C:/Users/petra/REU/' + vid_str + "/" + vid_str + "_"+ endo + ".mp4")

if __name__=='__main__':
    main()