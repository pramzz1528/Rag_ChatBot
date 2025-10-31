🤖 RAG-Powered Chatbot (Google Gemini + ChromaDB + Streamlit)

This project is an AI-powered chatbot that uses Retrieval-Augmented Generation (RAG) and Google Gemini models to answer user queries based on uploaded documents.
It integrates local embeddings, ChromaDB for vector storage, and Streamlit for an interactive web interface.

🚀 Features

📄 Upload your own .txt documents

🧠 Local embedding generation using SentenceTransformer

💾 Vector database management with ChromaDB

🔍 Auto model detection (Gemini Flash / Pro)

💬 Ask natural questions — get Gemini-powered answers

⚙️ Built with Streamlit for quick deployment and UI simplicity

🧩 Tech Stack
Component	Description
Python	Main programming language
Streamlit	Web framework for UI
SentenceTransformer	Generates text embeddings
ChromaDB	Local vector database for document retrieval
Google Gemini API	Large Language Model used for response generation
📦 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/yourusername/ragchat.git
cd ragchat

2️⃣ Create a Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate     # For Windows
# OR
source venv/bin/activate  # For Mac/Linux

3️⃣ Install Dependencies
pip install streamlit requests chromadb sentence-transformers

4️⃣ Get Google Gemini API Key

Go to Google AI Studio

Generate a new API key

Copy it for later use inside the app.

🧠 How It Works

Upload a .txt document.

The app creates embeddings using SentenceTransformer.

Embeddings are stored locally in ChromaDB.

When you ask a question, the app:

Retrieves the most relevant content from your uploaded text.

Sends it along with your question to the Google Gemini model.

Displays a context-aware answer instantly.

▶️ Run the App

After installation, run:

streamlit run ragchat.py


Then open the link (usually http://localhost:8501) in your browser.

🧾 Example Usage

Upload a .txt document (e.g., your notes or research paper).

Type a question like:

Summarize the main points from the uploaded document.


Click “Ask Gemini”

Get accurate, context-rich answers ✨

⚠️ Troubleshooting

Error: “git not recognized” → Install Git and add it to PATH.

Streamlit not found → Run pip install streamlit

Gemini API error → Ensure your API key is valid and correctly entered in the sidebar.

🧑‍💻 Author

Pramod K
📍 Built as part of AI and Python learning at HACA, Kozhikode.
💡 Focused on RAG, AI, and chatbot systems.

📜 License

This project is open-source and available under the MIT License.
