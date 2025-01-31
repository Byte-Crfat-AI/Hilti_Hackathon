import os
from Text import PDF
from Images import Image
from Audio import Audio
from CSV import CSVProcessor
import tqdm
# Lexora is compatible with four file extensions .pdf, .jpg , .jpeg, .png , .mp3, .csv

class MainProcessing:
    def __init__(self):
        self.PDF = PDF()
        self.Image = Image()
        self.Audio = Audio()
        self.CSV = CSVProcessor(api_key='AIzaSyBkXXtG5XeopoPisjR0LGqFdNcy3F_a8eo')

    def read_files(self, target_folder):
        paths = []
        for dirpath, dirnames, filenames in os.walk(target_folder):
            for filename in filenames:
                file_path  = os.path.join(dirpath, filename)
                paths.append(file_path)
        return paths

    def process_files(self, paths):
        arr = []
        for path in tqdm.tqdm(paths):
            print(path)
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
            elif path.endswith('.xlsx'):
                # Process the excel
                text = self.CSV.process_csv(path)
            elif path.endswith('.xls'):
                # Process the excel
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
