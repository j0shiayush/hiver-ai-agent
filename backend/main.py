import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="Hiver AI Support Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CHROMA_DB_DIR = '../data/chroma_db'
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

try:
    collection = chroma_client.get_collection(name="amex_support_history")
except Exception:
    print("Warning: ChromaDB collection not found. Make sure you ran build_vector_db.py")
    collection = None

class SupportTicket(BaseModel):
    customer_tweet: str

@app.post("/api/process-ticket")
async def process_ticket(ticket: SupportTicket):
    if not collection:
        raise HTTPException(status_code=500, detail="Vector DB not initialized.")
        
    try:
        results = collection.query(
            query_texts=[ticket.customer_tweet],
            n_results=3
        )
        
        historical_context = ""
        for idx, metadata in enumerate(results['metadatas'][0]):
            historical_context += f"Past Resolution {idx+1}: {metadata['brand_response']}\n"

        prompt = f"""
        You are an expert AI support agent for @AskAmex. Analyze this incoming tweet:
        "{ticket.customer_tweet}"
        
        Here is how the brand historically handled similar issues:
        {historical_context}
        
        Respond with ONLY a raw JSON object containing these three keys:
        1. "intent": A short category (e.g., "account_locked", "fee_dispute", "general_inquiry").
        2. "drafted_reply": A professional, empathetic reply under 280 characters grounded in the historical resolutions.
        3. "escalate": Boolean (true/false). Set to true if it requires secure info or a human supervisor.
        """
        
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        
        return json.loads(clean_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)