import os
# Lexora is compatible with four file extensions .pdf, .jpg , .jpeg, .png , .mp3, .csv

def read_files(target_folder):
    paths = []
    extenstion = []
    for dirpath, dirnames, filenames in os.walk(target_folder):
        for filename in filenames:
            file_path  = os.path.join(dirpath, filename)
            file_root, file_extension = os.path.splitext(filename)
            extenstion.append(file_extension)
            paths.append(file_path)
    return paths

paths = read_files('D:\Hilti_Hackathon\Hilti_Hackathon\Target_Folder\Target_Folder')

def process_files(paths):
    for path in paths:
        if path.endswith('.jpg') or path.endswith('.jpeg') or path.endswith('.png'):
            #Process the image
        elif path.endswith('.pdf'):
            #Process the pdf
        elif path.endswith('.mp3'):
            #Process the audio
        elif path.endswith('.csv'):
            #Process the csv
            
