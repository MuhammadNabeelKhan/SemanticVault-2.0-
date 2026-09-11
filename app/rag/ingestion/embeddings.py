import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

#takes in a list of dictionaries that hold chunks of texts with their respective files
def embeddings(list_dic_chunks):

    list_of_embedded_chunksInfo = []
    for dics_chunks in list_dic_chunks:

        embedded_text = client.embeddings.create(
            model="text-embedding-3-small",
            input = dics_chunks["text"]
        ).data[0].embedding
        embedded_chunksInfo = {"file_name": dics_chunks["file_name"], "text":embedded_text}  
        list_of_embedded_chunksInfo.append(embedded_chunksInfo)

    return list_of_embedded_chunksInfo


if __name__ == "__main__":
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="I went to the see hehehe"
    )

    print(f"this is the {response}")