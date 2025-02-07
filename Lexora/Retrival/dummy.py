import pickle
import os
import faiss

database_dir = 'D:\\Hilti_Hackathon\\Hilti_Hackathon\\Lexora\\Database\\Embeddings'
faiss_temp = os.listdir(database_dir)
faiss_files = [faiss_temp[i] for i in range(len(faiss_temp)) if faiss_temp[i][-6:] == ".faiss"]
metadata = [faiss_temp[i] for i in range(len(faiss_temp)) if faiss_temp[i][-4:] == ".pkl"]
keyword_database_dir = 'D:\\Hilti_Hackathon\\Hilti_Hackathon\\Lexora\\Database\\Keywords'
keyword_temp = os.listdir(keyword_database_dir)
keyword_faiss = [keyword_temp[i] for i in range(len(keyword_temp)) if keyword_temp[i][-6:] == ".faiss"]
keyword_metadata = [keyword_temp[i] for i in range(len(keyword_temp)) if keyword_temp[i][-4:] == ".pkl"]

if len(faiss_files) != len(metadata):
    raise ValueError("The number of .faiss files does not match the number of .pkl files")

for i in range(len(faiss_files)):
    index_path = os.path.join(database_dir, faiss_files[i])
    metadata_path = os.path.join(database_dir, metadata[i])
    index = faiss.read_index(index_path)
    with open(metadata_path, "rb") as f:
        metadata_content = pickle.load(f)
    print(index.ntotal)
    if len(metadata_content) != index.ntotal:
        print(f"Metadata content for {faiss_files[i]} is incorrect")
    if index.ntotal > 9000:
        os.rmdir(index_path)
        os.rmdir(metadata_path)
        os.rmdir(os.path.join(keyword_database_dir, keyword_faiss[i]))
        os.rmdir(os.path.join(keyword_database_dir, keyword_metadata[i]))
        print(f"Deleted {faiss_files[i]} and {metadata[i]}")

# with open('D:\Hilti_Hackathon\Hilti_Hackathon\Lexora\Database\Keywords\metadata_Others_Diamond tools - Wear.pkl', "rb") as f:
#     metadata_content = pickle.load(f)
# print(metadata_content)