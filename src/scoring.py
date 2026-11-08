import json
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY, MODEL, ICP

llm = ChatGoogleGenerativeAI(
    model=MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0,
)

def score_lead(company: str, research: str) -> dict:
    prompt = f"""You are a B2B lead scorer. Score this company against our ICP.

ICP: {json.dumps(ICP)}

Company: {company}
Research: {research}

Return ONLY valid JSON in this exact shape:
{{"score": 0, "rationale": "one sentence", "signals": ["signal1", "signal2"]}}

Score 0-100. No markdown, no explanation outside the JSON."""
    
    response = llm.invoke(prompt)
    content = response.content

    # Handle newer LangChain returning a list of content blocks
    if isinstance(content, list):
        text = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in content])
    else:
        text = str(content)

    text = text.strip()

    # Strip markdown fences if the model added them
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
            
    return json.loads(text.strip())

if __name__ == "__main__":
    result = score_lead("Stripe", "B2B payments company, ~8000 employees, global.")
    print(result)