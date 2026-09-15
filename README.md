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

## 3. Evaluation Harness
*   **Escalation Accuracy:** Deterministic comparison against the golden set.
*   **Empathy Score (1-5):** Evaluated by `gemini-2.5-flash` for professional tone.
*   **Grounding Score (1-5):** Evaluated by `gemini-2.5-flash` to penalize hallucinated phone numbers or policies.

## 4. Failure Analysis & Next Steps
1.  **Context Hallucination:** In rare cases, the LLM prioritized pre-trained knowledge over the retrieved ChromaDB context. 
2.  **Edge-Case Escalation Variance:** The deterministic golden set occasionally clashed with the LLM's subjective judgment on ambiguous queries.
3.  **Future Architecture:** With one more week, I would implement an agentic state machine RAG pipeline (using LangGraph) with explicit document relevance grading to act as a strict hallucination guardrail.