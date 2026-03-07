from loading_embedding import *
from retrieval import *
from generation import *

def main():

    #Loading, Embedding, and Storing in postgres
    docs = load_documents("docs_path")
    chunks = chunking_documents(docs)
    embedding_logic = embedding_model()
    store_vectors(embedding_logic, chunks)

    query = "is she straight or gay?"

    #Gathering relevant chunks and sending to gpt
    relevant_docs = retreive_doc(query)
    awnser = send_to_gpt(query, relevant_docs)


if __name__ == "__main__":
    main()
