import os
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="support_assistant/chroma_db")

collection = client.get_or_create_collection(
    name="zepto_policies"
)

documents = []
document_ids = []

for filename in sorted(os.listdir("support_assistant/docs")):

    if filename.endswith(".txt"):

        filepath = os.path.join("support_assistant/docs", filename)

        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()

        documents.append(text)
        document_ids.append(filename.replace(".txt", ""))

embeddings = model.encode(documents).tolist()

collection.add(
    ids=document_ids,
    documents=documents,
    embeddings=embeddings
)

print("Documents added to ChromaDB successfully.")
print("Number of documents:", collection.count())