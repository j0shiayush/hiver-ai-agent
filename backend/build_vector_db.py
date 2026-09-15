import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import os

DATA_PATH = '../data/processed_conversations.csv'
CHROMA_DB_DIR = '../data/chroma_db'

def build_db():
    print("Loading processed conversations...")
    df = pd.read_csv(DATA_PATH)
    
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    
    sentence_transformer_ef = embedding_functions.DefaultEmbeddingFunction()
    
    collection = client.get_or_create_collection(
        name="amex_support_history",
        embedding_function=sentence_transformer_ef
    )
    
    sample_df = df.head(1000).copy()
    
    documents = sample_df['customer_text'].tolist()
    metadatas = [{"brand_response": response, "intent": "historical"} for response in sample_df['brand_response'].tolist()]
    ids = [str(tweet_id) for tweet_id in sample_df['customer_tweet_id'].tolist()]
    
    print(f"Embedding and storing {len(documents)} conversations into ChromaDB. This may take a minute...")
    
    batch_size = 200
    for i in range(0, len(documents), batch_size):
        collection.add(
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            ids=ids[i:i+batch_size]
        )
        print(f"Processed batch {i//batch_size + 1}")

    print(f"Successfully built ChromaDB vector index at {CHROMA_DB_DIR}")

if __name__ == "__main__":
    build_db()