#Here I will connect to my Postgres vector store
#Get user query 
#Find the most similar chunks using cosine similarity
#Return those chunks

from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from loading_embedding import *

def retreive_doc(query):
    #the connection string is telling python where the database is and how to login
    connection_string = os.getenv("DATABASE_URL")
    #//username:passoword@location/specific-database

    embedding_logic = embedding_model()
    
    #postgres is the database
    #pgvector is where we can search and see vector storage
    #so PGVector is a langchain python class that lets us speak to pgvector 
    #pgvector speaks to postgres
    #when i create the PGVector object, its default is set to consine similarity
    #changable by adding a comma followed by: distance_strategy=DistanceStrategy.EUCLIDEAN
    vector_store = PGVector(connection = connection_string, embeddings = embedding_logic)

    results = vector_store.similarity_search_with_score(query, k=3)    

#    for result in results:
#       print(result)


    return results
