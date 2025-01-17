import os
from Processing.Text import PDF
from Processing.Images import Image
from Processing.Audio import Audio
from Processing.CSV import CSV
# Lexora is compatible with four file extensions .pdf, .jpg , .jpeg, .png , .mp3, .csv

class MainProcessing:
    def __init__(self):
        self.root_folder =  'D:/Hilti_Hackathon/Hilti_Hackathon/Target_Folder/Target_Folder'
        self.PDF = PDF()
        self.Image = Image()
        self.Audio = Audio()
        self.CSV = CSV()

    def read_files(self, target_folder):
        paths = []
        for dirpath, dirnames, filenames in os.walk(target_folder):
            for filename in filenames:
                file_path  = os.path.join(dirpath, filename)
                paths.append(file_path)
        return paths

    def process_files(self, paths):
        arr = []
        for path in paths:
            if path.endswith('.jpg') or path.endswith('.jpeg') or path.endswith('.png'):
                # Process the image
                text = self.Image.process_image(path)
            elif path.endswith('.pdf'):
                # Process the pdf
                text = self.PDF.process_pdf(path)
            elif path.endswith('.mp3'):
                # Process the audio
                text = self.Audio.process_audio(path)
            elif path.endswith('.csv'):
                # Process the csv
                text = self.CSV.process_csv(path)
            else:
                continue
            arr.append([text, path])
        return arr

    # Function when the user installs Lexora and runs it for the first time and the below function will be called after that
    def main_processing(self, root_folder):
        paths = self.read_files(root_folder)
        processed_files = self.process_files(paths)
        return processed_files

    # this function will be called whenver a user creates a new file 
    def main_processing_new(self,root_folder):
        paths = self.read_files(root_folder)
        # check for the paths that are already processed and stored in the database and remove those paths from the paths list
        new_paths = paths # yet to be completed
        processed_files = self.process_files(new_paths)
        return processed_files
