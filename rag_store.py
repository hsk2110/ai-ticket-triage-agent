import os
import chromadb
from chromadb.utils import embedding_functions

# Initialize persistent ChromaDB client locally
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Use default light embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = chroma_client.get_or_create_collection(
    name="company_knowledge",
    embedding_function=default_ef
)

def initialize_vector_db(faq_filepath="company_faq.md"):
    # Reads FAQ file, chunks sections, and populates ChromaDB

    if not os.path.exists(faq_filepath):
        print(f"Warning: {faq_filepath} no found")
        return

    with open(faq_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # split sections by header (##)
    sections = [s.strip() for s in content.split("## ") if s.strip()]

    ids = []
    documents = []

    for idx, section in enumerate(sections, 1):
        lines = section.split("\n", 1)
        header = lines[0]
        body = lines[1] if len(lines) > 1 else ""

        full_chunk = f"Topic: {header}\n{body}"
        ids.append(f"faq_chunk_{idx}")
        documents.append(full_chunk)

    # Upsert into ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents
    )

    print(f"Indexed {len(documents)} knowledge chunks into ChromaDB")

def query_knowledge_base(query_text: str, n_results: int = 2) -> str:
    # Retrieves top matching context chunks from ChromaDB
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )

    retrieved_docs = results.get("documents", [[]])[0]
    return "\n---\n".join(retrieved_docs) if retrieved_docs else "No matching company policy found."

# Run setup if executed directly
if __name__ == "__main__":
    initialize_vector_db()
    test_query = "How do I get an invoice?"
    print(f"\nTest Query: '{test_query}'")
    print("Retrieved Context:\n", query_knowledge_base(test_query))