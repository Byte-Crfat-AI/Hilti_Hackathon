import os
from Text import process_pdf
from Images import process_image
from Audio import process_audio
from CSV import process_csv
# Lexora is compatible with four file extensions .pdf, .jpg , .jpeg, .png , .mp3, .csv

root_folder = 'D:/Hilti_Hackathon/Hilti_Hackathon/Target_Folder/Target_Folder'

def read_files(target_folder):
    paths = []
    for dirpath, dirnames, filenames in os.walk(target_folder):
        for filename in filenames:
            file_path  = os.path.join(dirpath, filename)
            paths.append(file_path)
    return paths


def process_files(paths):
    arr = []
    for path in paths:
        if path.endswith('.jpg') or path.endswith('.jpeg') or path.endswith('.png'):
            #Process the image
            text = process_image(path)
        elif path.endswith('.pdf'):
            #Process the pdf
            text = process_pdf(path)
        elif path.endswith('.mp3'):
            #Process the audio
            text = process_audio(path)
        elif path.endswith('.csv'):
            #Process the csv
            text = process_csv(path)
        else:
            continue
        arr.append([text , path])
    return arr

def main():
    paths = read_files(root_folder)
    processed_files = process_files(paths)
    return processed_files
    
            
