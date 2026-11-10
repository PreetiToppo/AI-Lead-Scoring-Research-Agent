# AI Lead Scoring & Research Agent

An automated GTM pipeline that ingests a list of companies, researches them using the Gemini API, scores them against a custom Ideal Customer Profile (ICP), and safely syncs qualified leads to HubSpot.

## Architecture

1. **Ingestion & Deduplication:** Reads a CSV of companies and removes duplicates using Pandas.
2. **Research:** Uses LangChain and `gemini-3.5-flash` to generate a brief profile of the company.
3. **Scoring:** Prompts the LLM to score the company 0-100 based on a defined ICP, returning structured JSON.
4. **CRM Sync:** Checks if the lead exists in HubSpot, and pushes new leads scoring above a defined threshold via REST API.

## Setup & Execution

### Option 1: Run Locally
1. Clone the repo and install dependencies:
   `pip install -r requirements.txt`
2. Create a `.env` file with your keys:
   `GEMINI_API_KEY=your_key`
   `HUBSPOT_API_KEY=your_key`
3. Run the pipeline:
   `python src/main.py`

### Option 2: Run via Docker
1. Build the image:
   `docker build -t lead-scoring-agent .`
2. Run the container:
   `docker run --env-file .env lead-scoring-agent`

### Run Tests
To run the unit tests (which mock the LLM to test JSON parsing):
`pytest tests/`

## Design Decisions & Technical Challenges

*   **Structured Output:** LLMs naturally return conversational text. I enforced a strict JSON output schema in the prompt, and added a fallback parser to strip markdown formatting just in case the model hallucinated it.
*   **LangChain Response Formatting:** Handled edge cases where LangChain's `response.content` returned a list of dictionaries instead of a string, ensuring the pipeline doesn't crash during parsing.
*   **Rate Limiting:** The Gemini free tier limits requests to 5 per minute. I implemented `time.sleep()` pacing in the pipeline loop to prevent `429 RESOURCE_EXHAUSTED` errors, ensuring reliable delivery at scale.
*   **Idempotency:** To prevent duplicate data, the HubSpot integration queries the CRM API to check if the company already exists before creating a new record. 
*   **Testing & Mocking:** Wrote Pytest unit tests to validate JSON extraction logic. Because LangChain uses Pydantic, mocking individual methods fails; I had to mock the entire LLM object at the module level.
*   **Containerization:** Handled Docker `FileNotFoundError` issues by programmatically creating the logging directory (`os.makedirs`) on startup to ensure resilience in isolated environments.

## Limitations & Future Work
*   *Live Web Search:* The current research relies on the LLM's built-in knowledge. A production version would integrate a live web search API (like Tavily or Serper) to pull real-time company news and trigger the scoring logic based on current events.
*   *Model Pinning:* The model is hardcoded to `gemini-3.5-flash`. In production, this should be a moving alias or a fallback list to handle API deprecations.