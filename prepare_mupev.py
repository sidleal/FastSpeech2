import csv
import shutil
import os
destination_path = "/home/sidleal/sources/FastSpeech2/raw_data/mupev"
source_path = "/home/sidleal/sources/data/mupev"
def process_file():
    filepath = source_path + "/metadata.csv" 
    try:
        with open(filepath, 'r', newline='') as csvfile: 
            reader = csv.reader(csvfile)
            next(reader, None) 
            for row in reader:
                fpath = row[2]
                ftext = row[10]
                fspeaker = row[4]

                ftext = ftext.split('"')[1]
                if ftext.strip() == '':
                    continue
                print(fspeaker, fpath, ftext)
                wav_name = fpath.split('/')[-1]
                lab_name = wav_name[:-4] + ".lab"
                #print(wav_name, lab_name)
                #print('--------------', source_path + fpath[10:])
                os.makedirs(destination_path + "/" + fspeaker, exist_ok=True )
                shutil.copy2(source_path + fpath[10:], destination_path + "/" + fspeaker + "/"+ wav_name)
                with open(destination_path + "/" + fspeaker + "/"+ lab_name, "w", encoding="utf-8") as f:
                    f.write(ftext)
    
    #except FileNotFoundError:
    #    print(f"Error: File not found at '{filepath}'")
    except Exception as e:  
        print(f"An error occurred: {e}")

process_file()