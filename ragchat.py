import streamlit as st
import os
import requests
import chromadb
from sentence_transformers import SentenceTransformer

# -------------------------
# SIDEBAR API CONFIG
# -------------------------
st.sidebar.title("🔑 API Configuration")

gemini_api_key = st.sidebar.text_input(
    "Enter your Google Gemini API Key:",
    type="password",
    help="Get your API key from https://aistudio.google.com/app/apikey"
)

if not gemini_api_key:
    st.error("Please enter your Google Gemini API key in the sidebar to continue.")
    st.stop()

# -------------------------
# PAGE UI
# -------------------------
st.title("🤖 RAG-Powered Chatbot (Google Gemini Auto Model)")
st.write("Upload documents and ask questions. Uses local embeddings + auto Gemini model selection.")

# -------------------------
# EMBEDDING MODEL (LOCAL)
# -------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(texts):
    """Generate embeddings using SentenceTransformer"""
    return embed_model.encode(texts).tolist()

# -------------------------
# CHROMA VECTOR DATABASE
# -------------------------
try:
    chroma_client = chromadb.Client()

    # Recreate collection cleanly
    try:
        chroma_client.delete_collection("docs")
    except:
        pass

    collection = chroma_client.create_collection("docs")

except Exception as e:
    st.error(f"Error setting up ChromaDB: {str(e)}")
    st.stop()

# -------------------------
# FILE UPLOAD
# -------------------------
uploaded_file = st.file_uploader("📄 Upload a .txt file", type=["txt"])

if uploaded_file:
    try:
        text = uploaded_file.read().decode("utf-8")

        collection.add(
            documents=[text],
            embeddings=embed([text]),
            ids=["doc1"]
        )

        st.success("✅ Document added to the local vector database!")

    except Exception as e:
        st.error(f"Error adding document: {str(e)}")

# -------------------------
# AUTO-DETECT GEMINI MODEL
# -------------------------
@st.cache_data(show_spinner=False)
def get_available_gemini_model(api_key: str):
    """Fetch available Gemini models and return the best one."""
    try:
        url = "https://generativelanguage.googleapis.com/v1/models"
        headers = {"x-goog-api-key": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        models = [m["name"].split("/")[-1] for m in data.get("models", [])]
        # Prefer flash > pro > older
        preferred_order = ["1.5-flash", "1.5-pro", "1.0-pro", "flash", "pro"]

        for pref in preferred_order:
            for model in models:
                if pref in model:
                    return model

        # fallback to first available
        if models:
            return models[0]

        return None
    except Exception as e:
        st.warning(f"⚠ Could not fetch model list automatically: {e}")
        return None

gemini_model = get_available_gemini_model(gemini_api_key)
if gemini_model:
    st.sidebar.success(f"Using Gemini model: `{gemini_model}`")
else:
    gemini_model = "gemini-1.5-flash"  # fallback default
    st.sidebar.warning(f"Using fallback model: {gemini_model}")

# -------------------------
# GEMINI CHAT FUNCTION
# -------------------------
def query_gemini(prompt: str, api_key: str, model: str):
    """Send a prompt to Gemini API and return text response."""
    endpoint = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(endpoint, headers=headers, json=body)

    if response.status_code != 200:
        try:
            err = response.json().get("error", {}).get("message", "Unknown error")
            raise Exception(f"Gemini API Error ({response.status_code}): {err}")
        except Exception:
            response.raise_for_status()

    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

# -------------------------
# QUESTION INPUT
# -------------------------
user_question = st.text_input("💬 Ask a question based on your document:")

# -------------------------
# ASK BUTTON HANDLER
# -------------------------
if st.button("Ask Gemini"):
    if collection.count() == 0:
        st.warning("⚠ Please upload a document first!")
    elif not user_question.strip():
        st.warning("⚠ Please enter a question.")
    else:
        try:
            # Retrieve relevant context
            results = collection.query(
                query_embeddings=embed([user_question]),
                n_results=1
            )
            context = results["documents"][0][0] if results["documents"] else ""

            # Create the full prompt
            prompt = f"""
You are a helpful AI assistant. Use the context below to answer accurately.

Context:
{context}

Question:
{user_question}

Answer:
"""

            # Get Gemini response
            answer = query_gemini(prompt, gemini_api_key, gemini_model)

            st.write("### ✅ Gemini's Answer:")
            st.write(answer)

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
