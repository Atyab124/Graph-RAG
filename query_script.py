import json
import numpy as np
import ollama

# --- Step 1: Load stored embeddings ---
with open("ollama_embeddings.json", "r") as f:
    documents = json.load(f)  # [{"text": "...", "embedding": [...]}, ...]

# --- Step 2: Helper for cosine similarity ---
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# --- Step 3: Encode the query using the same local embed model ---
query = "which student is the top scorer?"
embed_response = ollama.embeddings(model="nomic-embed-text", prompt=query)
query_embedding = embed_response["embedding"]

# --- Step 4: Rank documents by similarity ---
ranked_docs = sorted(
    documents,
    key=lambda x: cosine_similarity(query_embedding, x["embedding"]),
    reverse=True
)

top_docs = ranked_docs[:3]  # pick top-k matches

# --- Step 5: Send top matches to Qwen for answer generation ---
context = "\n".join(d["text"] for d in top_docs)
prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {query}
Answer:"""

response = ollama.chat(model="qwen2.5:latest", messages=[{"role": "user", "content": prompt}])
print(response["message"]["content"])
