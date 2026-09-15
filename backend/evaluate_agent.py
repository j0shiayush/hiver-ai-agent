import pandas as pd
import json
import os
import time
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = 'gemini-2.5-flash'

CHROMA_DB_DIR = '../data/chroma_db'
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = chroma_client.get_collection(name="amex_support_history")

DATA_PATH = '../data/golden_dataset_labelled.csv'

def call_model_with_retry(prompt, retries=5):
    for attempt in range(retries):
        try:
            res = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            if res and res.text:
                return res.text
            else:
                raise ValueError("Empty response from API")
                
        except Exception as e:
            if attempt == retries - 1:
                print(f"   [Failed completely after {retries} attempts: {e}]")
                return '{"intent": "error", "drafted_reply": "error", "escalate": false}'
                
            print(f"   [API limit hit. Pausing 30s... (Attempt {attempt+1}/{retries})]")
            time.sleep(30)

def evaluate_system():
    print("Loading Golden Dataset...")
    df = pd.read_csv(DATA_PATH)
    sample_df = df.head(15)
    
    total_tested = 0
    correct_escalations = 0
    total_empathy = 0.0
    total_grounding = 0.0
    
    print(f"Starting evaluation on {len(sample_df)} tickets...\n" + "-" * 50)

    for index, row in sample_df.iterrows():
        tweet = str(row['customer_text'])
        true_esc = str(row['requires_escalation']).strip().lower() == 'true'
        
        results = collection.query(query_texts=[tweet], n_results=3)
        context = "\n".join([f"- {m['brand_response']}" for m in results['metadatas'][0]])
        
        agent_prompt = f"""
        You are a support agent for @AskAmex. Analyze this tweet:
        "{tweet}"

        Historical brand context:
        {context}

        Return raw JSON with:
        - "intent": short category string
        - "drafted_reply": under 280 chars grounded in context
        - "escalate": boolean (true/false)
        """
        
        try:
            agent_raw = call_model_with_retry(agent_prompt)
            clean_agent = agent_raw.replace('```json', '').replace('```', '').strip()
            agent_data = json.loads(clean_agent)
            
            gen_reply = agent_data.get('drafted_reply', '')
            gen_esc = bool(agent_data.get('escalate', False))
            
            if gen_esc == true_esc:
                correct_escalations += 1
            
            time.sleep(13)

            judge_prompt = f"""
            You are a QA auditor for customer support. Evaluate this drafted reply.
            
            Customer: "{tweet}"
            AI Reply: "{gen_reply}"
            Context: {context}

            Score from 1 to 5:
            - "empathy_score": tone, professionalism, politeness
            - "grounding_score": strict adherence to Amex context without hallucinated details

            Return raw JSON with keys: "empathy_score" (int) and "grounding_score" (int).
            """
            
            judge_raw = call_model_with_retry(judge_prompt)
            clean_judge = judge_raw.replace('```json', '').replace('```', '').strip()
            judge_data = json.loads(clean_judge)
            
            emp = float(judge_data.get('empathy_score', 3))
            grd = float(judge_data.get('grounding_score', 3))
            
            total_empathy += emp
            total_grounding += grd
            total_tested += 1
            
            print(f"Row {index + 1:02d} | Escalation Match: {gen_esc == true_esc} | Empathy: {emp}/5 | Grounding: {grd}/5")
            time.sleep(13)

        except Exception as e:
            print(f"Row {index + 1:02d} Error: {e}")

    if total_tested > 0:
        esc_acc = round((correct_escalations / total_tested) * 100, 1)
        avg_emp = round(total_empathy / total_tested, 2)
        avg_grd = round(total_grounding / total_tested, 2)
        
        print("-" * 50)
        print("EVALUATION SUMMARY")
        print(f"Samples Evaluated:       {total_tested}")
        print(f"Escalation Accuracy:     {esc_acc}%")
        print(f"Average Empathy & Tone:  {avg_emp} / 5.0")
        print(f"Average Grounding:       {avg_grd} / 5.0")
        print("-" * 50)

if __name__ == "__main__":
    evaluate_system()