import os
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from generation import send_to_gpt, retreive_doc
from loading_embedding import *
import psycopg

app = FastAPI()

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
    conn = psycopg.connect("postgresql://postgres:password@localhost:5432/rag_db")
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
async def upload_file(file: UploadFile = File(...)):

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