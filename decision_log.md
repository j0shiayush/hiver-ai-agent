# Decision Log

1. **FastAPI Backend over Flask/Express:** Selected for native asynchronous support and Pydantic validation to handle robust LLM JSON parsing.
2. **React + Tailwind Dashboard:** Chosen over a basic Streamlit app to create a highly customizable, side-by-side UI that visualizes the agent's reasoning step-by-step.
3. **ChromaDB over Pinecone:** Kept the architecture entirely local to ensure reviewers could run the pipeline instantly without configuring cloud vector database API keys.
4. **Persistent Vector Client:** Configured ChromaDB as a `PersistentClient` rather than in-memory so the database does not need to be rebuilt upon every server restart.
5. **Heuristic Golden Dataset Generation:** Shifted from 100% LLM generation to a heuristic rule-engine for the 200-row dataset to bypass strict free-tier rate limits while maintaining data quality.
6. **LLM-as-a-Judge Evaluation:** Used semantic grading (empathy and grounding) instead of BLEU/ROUGE, as generative support text requires contextual assessment, not exact string matching.
7. **Custom Exponential Backoff:** Engineered a robust retry loop capturing specific HTTP 429 and WinError socket exceptions to ensure the evaluation script completes despite aggressive API throttling.
8. **IPv4 Loopback Bypass:** Hardcoded `127.0.0.1` in the Axios requests instead of `localhost` to bypass Windows-specific IPv6 routing conflicts during local development.
9. **Explainable Escalations:** Designed the dataset and prompt engineering to include an `escalation_reason` string alongside the boolean flag, preventing a "black-box" decision model.
10. **Targeted @AskAmex Filtering:** Sliced the original 3M row Kaggle dataset down to a single brand to constrain the domain and significantly improve RAG retrieval relevance.
11. **Twitter Constraint Prompting:** Hardcoded the agent prompt to draft replies under 280 characters to strictly respect the original platform's limitations.
12. **Read-Only Advisory Boundary:** Chose to restrict the agent from executing live account modifications to prioritize safety and privacy in a public-facing support context.