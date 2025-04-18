import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
import google.generativeai as genai

load_dotenv()

# Custom Google Embeddings wrapper
class GoogleGenAIEmbeddings(Embeddings):
    def __init__(self, model="models/embedding-001", api_key=None):
        self.model = model
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)

    def embed_documents(self, texts):
        return [genai.embed_content(content=text, model=self.model, task_type="retrieval_document")["embedding"] for text in texts]

    def embed_query(self, text):
        return genai.embed_content(content=text, model=self.model, task_type="retrieval_query")["embedding"]

def load_documents():
    docs = []
    knowledge_folder = "knowledge/"
    for file in os.listdir(knowledge_folder):
        path = os.path.join(knowledge_folder, file)
        if file.endswith(".pdf"):
            with open(path, "rb") as f:
                reader = PdfReader(f)
                text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
                docs.append(Document(page_content=text, metadata={"source": file}))
        elif file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                docs.append(Document(page_content=text, metadata={"source": file}))
    return docs

def load_and_index_knowledge():
    print("Loading documents...")
    raw_docs = load_documents()
    print(f"Loaded {len(raw_docs)} files.")

    print("Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(raw_docs)
    print(f"Created {len(chunks)} chunks.")

    print("Generating embeddings (this might take a few minutes)...")
    embeddings = GoogleGenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    print("Saving vector store to disk...")
    vectorstore.save_local("gabby_vectorstore")
    print("Vector store saved successfully!")


def load_vectorstore():
    embeddings = GoogleGenAIEmbeddings()
    return FAISS.load_local(
        "gabby_vectorstore",
        embeddings,
        allow_dangerous_deserialization=True  # ✅ this is what you're missing
    )

