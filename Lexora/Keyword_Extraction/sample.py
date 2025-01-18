import torch  # Import torch at the beginning
from Keyword_Extraction.main_keyword_extraction import MainKeywordExtraction
from Keyword_Extraction.embeddings import Embeddings
from Keyword_Extraction.keyword_ranking import Keyword
from Keyword_Extraction.vectordb import VectorDB

def embeddings():
    print("=== Generating Text Embeddings ===")
    text = "Natural Language Processing (NLP) involves the application of computational techniques to the analysis and synthesis of natural language."
    embeddings_class = Embeddings()
    embeddings = embeddings_class.get_embeddings(text)
    print("Embeddings generated (shape):", embeddings.shape)

def keyword_ranking():
    print("\n=== Extracting and Ranking Keywords ===")
    text = "Machine learning is a subset of artificial intelligence that involves training algorithms to learn from and make predictions on data."
    keyword_class = Keyword()
    ranked_set = keyword_class.keyword_main(text)
    print("Ranked Keywords and Scores:")
    for embedding, rank, keyword in ranked_set:
        print(f"Keyword: {keyword}, Score: {rank}")

def vectordb():
    print("\n=== Storing Keywords in VectorDB ===")
    ranked_set = [
        [torch.tensor([1.0, 2.0, 3.0]), 0.9, "machine learning"],
        [torch.tensor([4.0, 5.0, 6.0]), 0.8, "artificial intelligence"],
    ]
    path = "D:/Hilti_Hackathon/Example/path/to/file.txt"
    vector_db = VectorDB()
    vector_db.keywords_db(ranked_set, path)
    print("Keywords stored in VectorDB.")

def main_keyword_extraction():
    print("\n=== Full Pipeline for Keyword Extraction ===")
    processed_files = [
        (
            "Data science is an interdisciplinary field that uses scientific methods to extract insights from data.",
            "D:/Hilti_Hackathon/Example/path1/to/file1.txt",
        ),
        (
            "Big data refers to datasets that are too large or complex to be processed using traditional methods.",
            "D:/Hilti_Hackathon/Example/path2/to/file2.txt",
        ),
    ]
    main_extraction = MainKeywordExtraction()
    result = main_extraction.main_keyword_extraction(processed_files)  # Use the correct method name
    print(result)

if __name__ == "__main__":
    embeddings()
    keyword_ranking()
    vectordb()
    main_keyword_extraction()
