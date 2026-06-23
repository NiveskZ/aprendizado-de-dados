from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def carregar_documentos():
    loader = TextLoader("data/manual_rh.txt", encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="hr_manual"
    )
    print("Documentos carregados.")

if __name__ == "__main__":
    carregar_documentos()