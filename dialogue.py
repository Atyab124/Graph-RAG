import json
import numpy as np
import ollama

# --- Step 1: Load stored embeddings once ---
with open("ollama_embeddings.json", "r") as f:
    documents = json.load(f)  # [{"text": "...", "embedding": [...]}, ...]

# --- Step 2: Helper for cosine similarity ---
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("💬 Ask me anything about the class database! (type 'exit' to quit)\n")

while True:
    # --- Step 3: Take user query ---
    query = input("> ").strip()
    if query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # --- Step 4: Encode the query ---
    embed_response = ollama.embeddings(model="nomic-embed-text", prompt=query)
    query_embedding = embed_response["embedding"]

    # --- Step 5: Rank documents by similarity ---
    ranked_docs = sorted(
        documents,
        key=lambda x: cosine_similarity(query_embedding, x["embedding"]),
        reverse=True
    )
    top_docs = ranked_docs[:7]  # fetch top 7 facts

    # --- Step 6: Build prompt for Qwen ---
    context = "\n".join(d["text"] for d in top_docs)
    prompt = f"""You are answering questions based on a class database.
Use the provided context facts to answer clearly.

Context:
{context}

Question: {query}
Answer:"""

    # --- Step 7: Query Qwen ---
    response = ollama.chat(model="qwen2.5:latest", messages=[{"role": "user", "content": prompt}])
    print("🤖", response["message"]["content"])
