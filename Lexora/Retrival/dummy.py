import pickle

chunk_file = 'D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Keywords\metadata_Hilti_storage_pexels-juan-felipe-ramirez-312591454-18190023.pkl'
with open(chunk_file, 'rb') as f:
    chunks = pickle.load(f)
print(chunks)