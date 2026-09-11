import os
from pypdf import PdfReader

def loading():
    current_file = __file__

    #trying to get to the folderfile directory
    deposited_files_dir = os.path.abspath(os.path.join( current_file, "..", "..", "..", "..", "depositedFiles"))
    
    list_of_dfiles = os.listdir(deposited_files_dir)


    all_documents = []

    for file in list_of_dfiles:
        filename, extension = os.path.splitext(file)
        file_path = os.path.join(deposited_files_dir, file)

        if extension == ".pdf":
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()
            file_info = {"file_name": filename, "text": full_text}
            all_documents.append(file_info)
        elif extension == ".txt":
            with open(file_path, "r") as f:
                text = f.read()
            file_info = {"file_name": filename, "text": text}    
            all_documents.append(file_info)        
        else:
            print(f"Unsupported file type: {file}")
    return all_documents

#need to return block of text for the chunker 
if __name__ == "__main__":
    print (loading())