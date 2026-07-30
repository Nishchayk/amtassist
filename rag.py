import chromadb
from sentence_transformers import SentenceTransformer


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="auslander_helper")



def retrieve_context(question:str, top_k:int = 4) -> dict:

    question_embedding = embedding_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k
    )


    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context_parts = []
    sources = []

    for i, (chunk,meta,dist) in enumerate(zip(chunks,metadatas,distances),start=1):
        context_parts.append(f"[Source {i}]\n{chunk}")
        sources.append({
            "source" : meta.get("source","unknow"),
            "distance":round(dist,3)
        })

    context = "\n\n".join(context_parts)

    return{
        "context":context,
        "sources":sources,
        "num_chunks":len(chunks)
    }

if __name__ == "__main__":
    test_question = "how do I register my address in berlin"
    print(f"\n test question : {test_question}\n")
    result = retrieve_context(test_question)
    print(f"Retrieved {result['num_chunks']} chunks")
    print(f"Sources: {result['sources']}\n")
    print("--- Context ---")
    print(result["context"][:800] + "...")

