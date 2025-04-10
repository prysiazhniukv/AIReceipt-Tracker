from pydantic_ai import Agent
from receipt_scanner.eyes.main import result
from receipt_scanner.models import Receipt

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
    - quantity:
        - value: amount (can be weight in grams or number of items)
        - unit: one of "g", "ml", or "pcs"
    - price: total price of that product

Do not hallucinate. If something is missing, skip it.
"""
)
receipt_text = "\n".join(result)


response = agent.run_sync(receipt_text)
print(response.data)
