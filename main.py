from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import ollama
from rag import retrieve_context

app = FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/ask")
async def ask_question(question:str):
    retrieval = retrieve_context(question, top_k=4)
    context = retrieval["context"]
    sources = retrieval["sources"]

    # Build the RAG system prompt
    system_prompt = (
        "You are a helpful assistant for international students in Berlin. "
        "Answer the user's question using ONLY the information in the context below. "
        "If the context does not contain the answer, say 'I don't have enough information "
        "in my sources to answer that.' Do not make up facts. "
        "Answer in 2-3 clear sentences.\n\n"
        f"CONTEXT:\n{context}"
    )

    # Call Llama with system prompt + user question
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )

    return {
        "question": question,
        "answer": response["message"]["content"],
        "sources": sources,
        "num_chunks_used": retrieval["num_chunks"]
    }