from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import pinecone
import json
from langchain.llms import Replicate
from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain

app = FastAPI()

pinecone.init(api_key='', environment='gcp-starter')
index_name = "perfume"
index = pinecone.Index(index_name)

llm = Replicate(
    model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
    model_kwargs={"temperature": 0.75, "max_length": 3000, "image_dimensions": "768x768"}
)

prompt_template = """Retrieve information from the database to help the user choose a perfume based on their preferences related to perfume notes. If you are uncertain about the answer, simply indicate that there is no product matching the criteria; avoid generating inaccurate responses.

User's Question: {question}

Helpful Answer: 
(Ensure that the Helpful Answer is a direct response and does not include a request for additional information or any user-facing question.)
"""

embeddings = HuggingFaceEmbeddings()
db = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    db.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True
)

chat_history = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        if data == "q":
            break
        input_data = json.loads(data)
        question = input_data.get("question", "")
        prompt = prompt_template.format(question=question)
        result = qa_chain({'question': prompt, 'chat_history': chat_history})
        response = {"answer": result['answer']}
        await websocket.send_text(json.dumps(response))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
