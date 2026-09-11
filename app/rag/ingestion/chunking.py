import os


#so this is taking in a list of dict={"filename": filename, "text": text}
def chunking(file_names_texts):

    list_of_chunks = []
    for files in file_names_texts:
        
        text = files["text"]
        length = len(text)

        #need to make a chunk overlap every beginnign of a chunk should contain 
        #words from the previous chunk
        #i went to the sea and went to go fishinig 
        # i went to the sea  chunk 1
        #        to the sea to go chunk 2
        #           the sea to go fishing chunk 3
        chunk_overlap = 50
        for paragraph in range(0, length, 500):
            if paragraph == 0:
                chunk_overlap = 0
            else: 
                chunk_overlap = 50
            chunk = text[paragraph - chunk_overlap :paragraph + 500]
            file_chunk = {"file_name": files["file_name"], "text": chunk} 
            list_of_chunks.append(file_chunk)


    return list_of_chunks
        

if __name__ =="__main__":
    
    print(chunking())