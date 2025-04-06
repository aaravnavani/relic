import json
import chromadb
import openai
from chromadb.config import Settings

# 📍 Use persistent Chroma storage
client = chromadb.PersistentClient(path="./ChromaStore")
collection = client.get_or_create_collection("user_messages")

def sanitize(value):
    return value if isinstance(value, (str, int, float, bool)) else "unknown"

def load_messages(path="messages.json"):

    if len(collection.get()["ids"]) > 0:
        print("✅ Already loaded. Skipping re-insert.")
        return

    with open(path) as f:
        data = json.load(f)

    docs, metadatas, ids = [], [], []

    for i, m in enumerate(data):
        text = m.get("text")
        if not text:
            continue

        sender = sanitize(m.get("sender"))
        timestamp = sanitize(m.get("timestamp"))

        docs.append(f"{sender}: {text}")
        metadatas.append({
            "sender": sender,
            "timestamp": timestamp
        })
        ids.append(f"msg_{i}")

    print(f"Loading {len(docs)} clean messages into Chroma...")
    collection.add(documents=docs, metadatas=metadatas, ids=ids)
    print("✅ Data inserted into Chroma!")

# 🚀 Load and persist if needed
load_messages()

# 🔍 View stored collection content
print("\n📂 Previewing Chroma collection data...")
results = collection.get()
for doc, meta in list(zip(results["documents"], results["metadatas"]))[:10]:
    print(f"• {doc}  — {meta}")

# 🧠 Set your OpenAI key

def ask_question(query, n_results=1000):
    results = collection.query(query_texts=[query], n_results=n_results)
    docs = results.get("documents", [[]])[0]

    print(f"\n🔍 Retrieved {len(docs)} docs from Chroma:")
    for d in docs:
        print("•", d)

    if not docs:
        return "No relevant messages found in your data."

    # Format into RAG prompt
    context = "\n".join([f"- {doc}" for doc in docs])
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.

Context:
{context}

Question:
{query}

Answer:"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

# 🧪 Example usage
query = "Where was the new office for my job last summer?"
answer = ask_question(query)

print("\n🧠 GPT says:")
print(answer)
