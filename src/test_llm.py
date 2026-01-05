import os
from llm_client import LLMClient

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load sample document
doc_path = os.path.join(BASE_DIR, "../data/sample_doc.txt")
with open(doc_path, "r", encoding="utf-8") as f:
    document = f.read()

# Load prompt template
prompt_path = os.path.join(BASE_DIR, "../prompts/extract_v1.txt")
with open(prompt_path, "r", encoding="utf-8") as f:
    prompt_template = f.read()

# Replace placeholder
prompt = prompt_template.replace("{{DOCUMENT}}", document)

# Initialize LLM client
llm = LLMClient(model="mistral")

# Generate output
output = llm.generate(prompt)

# Print raw output
print("LLM Output:\n", output)