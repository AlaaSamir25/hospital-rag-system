import os
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from database import tables, fetch_all_records
from embeddings import GeminiEmbeddings

embeddings = GeminiEmbeddings(api_key="gemini-api-key")

def build_documents():
    documents = []
    for table, cols in tables.items():
        records = fetch_all_records(table, cols)
        for record in records:
            text = f"{table} record: " + ", ".join([f"{k}: {v}" for k, v in record.items()])
            documents.append(Document(page_content=text, metadata={"table": table}))
    return documents

def get_vector_store():
    index_dir = "faiss_index"
    if os.path.exists(index_dir):
        return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    else:
        documents = build_documents()
        vector_store = FAISS.from_documents(documents, embeddings)
        vector_store.save_local(index_dir)
        return vector_store

if __name__ == "__main__":
    vs = get_vector_store()
    print("Vector store initialized with", vs.index.ntotal, "documents")