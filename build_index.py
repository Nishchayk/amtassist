import os
from sentence_transformers import SentenceTransformer
import chromadb


def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks



print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Done.\n")


client = chromadb.PersistentClient(path="./chroma_db")

try:
    client.delete_collection("auslander_helper")
    print("Deleted old collection")
except Exception:
    pass

collection = client.create_collection(name="auslander_helper")
print("Created fresh collection\n")

data_dir = "data"
all_ids = []
all_documents = []
all_metadatas = []
all_embeddings = []

files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
print(f"Found {len(files)} documents to process\n")

for filename in files:
    filepath = os.path.join(data_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)
    print(f"  {filename}: {len(text)} chars -> {len(chunks)} chunks")


    embeddings = model.encode(chunks)

    for i, chunk in enumerate(chunks):
        chunk_id = f"{filename}_chunk_{i}"
        all_ids.append(chunk_id)
        all_documents.append(chunk)
        all_metadatas.append({"source": filename, "chunk_index": i})
        all_embeddings.append(embeddings[i].tolist())


print(f"\nAdding {len(all_ids)} chunks to ChromaDB...")
collection.add(
    ids=all_ids,
    documents=all_documents,
    metadatas=all_metadatas,
    embeddings=all_embeddings
)

print(f"Done. Collection size: {collection.count()}")