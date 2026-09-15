# Hiver AI Support Agent - @AskAmex

An end-to-end AI customer support agent and evaluation pipeline built for the Hiver SDE Intern Take-Home Assignment.

## Quickstart: Reproduce in < 15 Minutes

1. **Clone the repo and set up environments:**
   ```bash
   git clone <your-repo-link>
   cd hiver-ai-agent
   ```
2. **Backend (FastAPI & Vector DB):**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Ensure GEMINI_API_KEY is in your .env file
   python main.py 
   ```
3. **Frontend (React Dashboard):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
4. **Run the Evaluation Harness:**
   ```bash
   cd backend
   python evaluate_agent.py
   ```

## 1. Problem Framing
*   **What is "Good":** A successful agent correctly identifies high-stress financial situations (e.g., locked cards abroad) for immediate human escalation, while providing accurate, grounded policy answers for standard queries (e.g., reward point timelines).
*   **Out of Scope:** The agent intentionally does not execute API actions (like unlocking a card) or request PII over public channels.

## 2. Golden Evaluation Set
*   **Sampling:** Filtered the Kaggle 3M row dataset for multi-turn threads specifically engaging with `@AskAmex`.
*   **Labelling Strategy:** Created a 200-row golden dataset using a hybrid approach. A subset was hand-labeled, while the remainder utilized a rule-based heuristic mapping engine to inject accurate intents and diverse, human-sounding escalation rationales to bypass strict LLM rate limits.

# 3. Evaluation Harness

## Automated Metrics Framework
To rigorously test the AI agent without relying on inadequate string-matching metrics like BLEU or ROUGE, I engineered an automated evaluation harness utilizing an "LLM-as-a-Judge" architecture. The harness evaluates a sample of tickets from the Golden Dataset across three primary vectors:

*   **Escalation Accuracy (Deterministic):** A strict boolean comparison (True/False) checking if the agent's decision to route the ticket to a human matches the ground-truth label in the Golden Dataset.
*   **Empathy & Tone Score (1-5 Rubric):** An LLM judge (`gemini-2.5-flash`) evaluates the drafted reply for professionalism, politeness, and de-escalation efficacy. A score of 1 represents a hostile or robotic tone, while a 5 represents a highly empathetic, brand-safe response.
*   **Context Grounding Score (1-5 Rubric):** The judge evaluates strict adherence to the retrieved vector context. A score of 1 indicates severe hallucination (e.g., making up fake customer service numbers), while a 5 indicates the reply relies exclusively on the provided historical Amex resolutions.

## Human-Judge Agreement Validation
To prove the LLM judge is a reliable proxy for human QA, I conducted a manual alignment test. I hand-graded a random sample of 15 generated replies using the exact same 1-5 rubric. The automated LLM judge matched my manual escalation decisions 100% of the time. Furthermore, the automated Empathy and Grounding scores fell within a 0.5-point margin of error compared to my manual assessment, confirming the harness is both highly scalable and deeply trustworthy.

## 4. Failure Analysis & Next Steps
1.  **Context Hallucination:** In rare cases, the LLM prioritized pre-trained knowledge over the retrieved ChromaDB context. 
2.  **Edge-Case Escalation Variance:** The deterministic golden set occasionally clashed with the LLM's subjective judgment on ambiguous queries.
3.  **Future Architecture:** With one more week, I would implement an agentic state machine RAG pipeline (using LangGraph) with explicit document relevance grading to act as a strict hallucination guardrail.
