import pinecone
import sys
from langchain.llms import Replicate
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader


def create_vector_db():
    pinecone.init(api_key='', environment='gcp-starter') 

    loader = CSVLoader(file_path="./final_perfume_data.csv", encoding='ISO-8859-1')
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings()

    index_name = "perfume"

    if index_name in pinecone.list_indexes():
        pinecone.delete_index(index_name)

    pinecone.create_index(name=index_name, dimension=768, metric="cosine")

    vectordb = Pinecone.from_documents(texts, embeddings, index_name=index_name)

if __name__ == "__main__":
    create_vector_db()