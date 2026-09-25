import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="support_assistant/chroma_db"
)

collection = client.get_collection(
    name="zepto_policies"
)

query = "What is the delivery charge for orders below INR 149?"

query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)


print("Question:")
print(query)

print("Retrieved documents:")

for i in range(len(results["documents"][0])):
    print("Document:", results["ids"][0][i])
    print("Content:")
    print(results["documents"][0][i])