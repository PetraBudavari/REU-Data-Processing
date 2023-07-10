import pandas as pd
import os
from pathlib import Path
import argparse

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

merge()

