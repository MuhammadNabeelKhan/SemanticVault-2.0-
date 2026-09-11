import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from rag.generation.generation import send_to_gpt, retreive_doc
from rag.ingestion.loading_embedding import *
import psycopg

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware


#this will let us send request to fasiapi, our server thats uploaded on railway, then returns
#info to our local host.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query:str


@app.get("/rag/listDB")
def list_db_files():
    try:
        docs = load_documents("docs_path")
        return {"files": [doc.metadata['source'] for doc in docs]}
    except FileNotFoundError:
         return {"files": "Data base is empty"}


@app.get("/rag/clear")
def clear_db():
    #this will clear everything in the postgres data base
    conn = psycopg.connect("postgresql://postgres:nymRaUMnoFSkSbjgVhKhXxRuyXyyTNxS@postgres.railway.internal:5432/railway")
    conn.execute("DELETE FROM langchain_pg_embedding;")
    conn.commit()
    conn.close()

    #this will clear everything in the local folder
    for file in os.listdir("docs_path"):
        os.remove(f"docs_path/{file}")

    #this will clear pycache
    for pyc in os.listdir("__pycache__"):
        os.remove(f"__pycache__/{pyc}")

    return {"message": "Database cleared successfully"}


@app.post("/rag/upload")
#so file: is telling fastAPi that it must be named file we do this when we package it in the 
# javascript form data. 
# then uploadfile is a type that helps us get multiple methods on the file later like 
# file.filename/file.read etc, 
# the file jsut arries as raw http data, uploadfiel tells fast api to wrap it into an upladofile
# Object so we can intereact with ti and use methods instead of it just being raw dat  
#it must havae a filed section named file for it to work and that is required 
#basically tells it to check that the http request
# has a file field in the body and that it is existing. 
#when we wrap it in a formdata object in the front end, we specify the name of the field 
# as file, so that is why we have to have file: here
async def upload_file(file: UploadFile = File(...)):
    os.makedirs("docs_path", exist_ok=True)

    file_path = f"docs_path/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    #important to note that our load_documents uses a function that goes inside a directory
    #and looks for files, if we were to put jsut docs_path, then we would be giving it a
    #file instead of a directory which would cause errors
    docs = load_documents("docs_path")
    chunks = chunking_documents(docs)
    embedding_logic = embedding_model()
    store_vectors(embedding_logic, chunks)

    return {"message": "File uploaded and processed successfully"}
        

@app.post("/rag/query")
def query_rag(request: QueryRequest):
    relevant_docs = retreive_doc(request.query)
    answer = send_to_gpt(query = request.query, relevant_docs= relevant_docs)

    return {"answer": answer}
