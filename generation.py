from langchain_openai import ChatOpenAI

from retrieval import retreive_doc


def send_to_gpt(query, relevant_docs):

    context = '\n'.join([doc.page_content for doc, score in relevant_docs if score > 0.5])

    if not context:
      return "I couldn't find anything relevant in the documents."
    
    prompt = f"Answer the question based on this context: \n{context}\n\n Question: {query}, if theres no context simply say i dont know"
   
    model = ChatOpenAI(model = "gpt-3.5-turbo")

    response = model.invoke(prompt)

    print(response.content)

    return response.content



    