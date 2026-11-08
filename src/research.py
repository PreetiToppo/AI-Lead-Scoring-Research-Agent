from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY, MODEL

llm = ChatGoogleGenerativeAI(
    model=MODEL,
    google_api_key=GEMINI_API_KEY,
    temperature=0.2,
)

def research_company(name: str) -> str:
    prompt = f"""Research the company "{name}" briefly:
- What they do
- Industry and approximate size
- Recent news or growth signals
- Likely pain points

Max 150 words. Plain text."""
    
    response = llm.invoke(prompt)
    content = response.content

    # Handle newer LangChain returning a list of content blocks
    if isinstance(content, list):
        text = "".join([block.get("text", "") if isinstance(block, dict) else str(block) for block in content])
    else:
        text = str(content)

    return text.strip()

if __name__ == "__main__":
    print(research_company("Stripe"))