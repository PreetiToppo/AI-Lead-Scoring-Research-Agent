# AI Lead Scoring & Research Agent

An automated GTM pipeline that ingests a list of companies, researches them using the Gemini API, scores them against a custom Ideal Customer Profile (ICP), and syncs qualified leads to HubSpot.

## Architecture

1. **Ingestion & Deduplication:** Reads a CSV of companies and removes duplicates using Pandas.
2. **Research:** Uses LangChain and `gemini-3.5-flash` to generate a brief profile of the company.
3. **Scoring:** Prompts the LLM to score the company 0-100 based on a defined ICP, returning structured JSON.
4. **CRM Sync:** Pushes leads scoring above a defined threshold to the HubSpot CRM via REST API.

## Setup

1. Clone the repo and install dependencies:
   `pip install -r requirements.txt`
2. Create a `.env` file with your keys:
   `GEMINI_API_KEY=your_key`
   `HUBSPOT_API_KEY=your_key`
3. Run the pipeline:
   `python src/main.py`

## Design Decisions & Technical Challenges

*   **Structured Output:** LLMs naturally return conversational text. I enforced a strict JSON output schema in the prompt, and added a fallback parser to strip markdown formatting just in case the model hallucinated it.
*   **LangChain Response Formatting:** Handled cases where LangChain's `response.content` returned a list of dictionaries instead of a string, ensuring the pipeline didn't crash on parsing.
*   **Rate Limiting:** The Gemini free tier limits requests to 5 per minute. I implemented `time.sleep()` pacing in the pipeline loop to prevent `429 RESOURCE_EXHAUSTED` errors, ensuring reliable delivery at scale.
*   **HubSpot Integration:** Handled API integrations via Bearer tokens, filtering only leads with a score >= 70 to keep the CRM clean.

## Limitations
*   *Research:* The current research is based on the LLM's training data. A production version would integrate a live web search API (like Tavily or Serper) for real-time company news.
*   *Idempotency:* The HubSpot sync uses a standard POST request. A production pipeline would query the CRM first to avoid creating duplicate contacts on re-runs.
*   *Model Pinning:* The model is hardcoded to `gemini-3.5-flash`. In production, this should be a moving alias or a fallback list to handle API deprecations.