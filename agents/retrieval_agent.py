import os
import json
import numpy as np
from dotenv import load_dotenv
from chromadb import Client as ChromaClient
from chromadb.api.types import Documents, Embeddings, EmbeddingFunction
from google import genai
from google.genai import types

load_dotenv()

# --- Initialize Gemini client ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in environment variables")

client = genai.Client(api_key=GOOGLE_API_KEY)

# --- Custom embedding function using Gemini ---
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model_id = "gemini-embedding-001"
        response = client.models.embed_content(
            model=model_id,
            contents=input,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=768
            )
        )
        return [np.array(e.values).tolist() for e in response.embeddings]

# --- Persistent ChromaDB setup ---
CHROMA_PATH = "chroma_faq_db"
chroma_client = ChromaClient()
embedding_fn = GeminiEmbeddingFunction()
collection = chroma_client.get_or_create_collection(
    name="faq_collection",
    embedding_function=embedding_fn
)

# --- Load FAQ JSON and populate Chroma if empty ---
FAQ_PATH = r"data\Ecommerce_FAQ_Chatbot_dataset.json"  # raw string for Windows path
if os.path.exists(FAQ_PATH):
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    faqs = faq_data.get("questions", [])
    if collection.count() == 0:  # only embed once
        print("🔹 Creating embeddings for FAQ dataset...")
        for i, faq in enumerate(faqs):
            question = faq.get("question")
            answer = faq.get("answer")
            collection.add(
                ids=[str(i)],
                documents=[f"{question}\nAnswer: {answer}"],
                metadatas=[{"question": question, "answer": answer}]
            )
        print("✅ Embeddings stored in Chroma successfully!")
else:
    raise FileNotFoundError(f"FAQ dataset not found at {FAQ_PATH}")

# --- Retrieval Agent ---
class RetrievalAgent:
    def __init__(self):
        self.client = client
        self.collection = collection

    def retrieve(self, user_query):
    # --- Create query embedding ---
        embed_response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=[user_query],
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=768
            )
        )
        query_embedding = np.array(embed_response.embeddings[0].values)

        # --- Retrieve top matches from Chroma ---
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=1
        )

        if not results["documents"]:
            return "Sorry, I couldn't find any relevant FAQ."

        retrieved_docs = [doc for sublist in results["documents"] for doc in sublist]
        print(retrieved_docs)

        # --- Construct prompt as a single string ---
        context = "\n\n".join(retrieved_docs)
        # --- Generate answer using contents argument ---
        answer = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=f"Using the following FAQ context, answer the question:\n\nContext:\n{context}\n\nQuestion: {user_query}\n\nAnswer:"),
            contents=user_query
        )
        return answer.text.strip()