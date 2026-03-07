import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from dotenv import load_dotenv

from langchain_text_splitters import CharacterTextSplitter

from langchain_openai import OpenAIEmbeddings

from langchain_postgres import PGVector


#i need to make it so this takes in pdf files aswell or both files?
def load_documents(docs_path = "docs"):
   
   if not os.path.exists(docs_path):
        raise FileNotFoundError("The path does not exist")   
   
   pdf_loader = DirectoryLoader(docs_path, glob = "*.pdf", loader_cls = PyPDFLoader)

   loader = DirectoryLoader(docs_path, glob = "*.txt", loader_cls = TextLoader)

   txt_docs = loader.load()
   pdf_docs = pdf_loader.load()

   docs = txt_docs + pdf_docs
   
   if len(docs) == 0:
       raise FileNotFoundError("There arent any .txt or .pdf files to be read in this folder")

   return docs

def chunking_documents(docs):
    
    #splitter is essentially the logic of splitting.
    splitter = CharacterTextSplitter(chunk_size = 500, chunk_overlap = 5)
    #here, we would apply that logic of splitting to our docs.
    chunks = splitter.split_documents(docs)

    return chunks

def embedding_model():

    load_dotenv()
    os.getenv("OPENAI_API_KEY")
    embedding_logic = OpenAIEmbeddings(model = "text-embedding-3-small")
    return embedding_logic


#The real difference postgres + pgvector is that we can store the vectors in a database
#and in that database we can see their unembedded chunks next to their embedded chunks
#and the meta data. Unlike ChromaDB, which is just a blackbox, this gives us a neat way
#to see the data and how it is being stored.
def store_vectors(embedding_logic, chunks):
    connection_string = "postgresql+psycopg://postgres:password@localhost:5432/rag_db"
    #vector_store is a tool that interacts with the database of postgres. We can 
    #run similarity searches on it and that will connect us with the vectorized info
    vector_store = PGVector.from_documents(documents = chunks , connection= connection_string, embedding = embedding_logic)
    return vector_store

#To see the documents stored we run the following code in terminal
#docker exec -it pgvector-db psql -U postgres -d rag_db -c "SELECT * FROM langchain_pg_embedding LIMIT 5;"
#We can change the * to documents, if we just want the documents, otherwise the vector
#as well as the metadata will be given as well.
#Similarly, we can entirely remove the LIMIT if we want to see everything 

#This is run on a Docker postgres, so the data isnt persisted on our local machine,
#rather on the Docker container thats running and saving the pgvector database

#     This was the code we ran to create the container, the password, the rag_db database
#   and the port and where exactonly on docker this would be called:

#docker run -d --name pgvector-db -e POSTGRES_PASSWORD=password 
#-e POSTGRES_DB=rag_db -p 5432:5432 pgvector/pgvector:pg16
