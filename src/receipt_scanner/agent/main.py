from pydantic_ai import Agent
from receipt_scanner.models import Receipt
from dotenv import load_dotenv

load_dotenv

agent = Agent(
    model="openai:gpt-4o",
    result_type=Receipt,
    system_prompt="""
You are an intelligent document parser. 
Your job is to extract structured information from messy OCR output of shopping receipts.

Return a valid JSON that matches this structure:
- storeName: the name of the store
- total: total amount paid
- products: a list of products with:
    - name: product name
    - price: total price of that product

Do not hallucinate. If something is missing, skip it.
""",
)


async def receipt_agent(receipt_text: str):
    response = await agent.run(receipt_text)
    return response.data
