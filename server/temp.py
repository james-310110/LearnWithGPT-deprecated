import os
import json
from pathlib import Path
from llama_index import download_loader, GPTSimpleVectorIndex

# loading openai api key from json file
with open('../keys_and_tokens.json', 'r') as f:
    data = json.load(f)
    openai_api_key = data.get("openai-api-key")
    if openai_api_key:
      os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
      print("openai_api_key not found in JSON file")
      
def build_simple_vector_index_from_pdf():
  # initializing pdf reader
  CJKPDFReader = download_loader('CJKPDFReader')
  # loading pdf into documents
  pdf = CJKPDFReader().load_data(file=Path('../data/llama-index.pdf'))
  # building simple vector index
  simple_vector_index = GPTSimpleVectorIndex.from_documents(pdf)
  # querying simple vector index
  # saving simple vector index to disk
  simple_vector_index.save_to_disk('simple_vector_index.json')

def query_simple_vector_index(prompt, response_mode):
  simple_vector_index = GPTSimpleVectorIndex.load_from_disk('simple_vector_index.json')
  simple_vector_response = simple_vector_index.query(
      prompt, mode=response_mode)
  print(simple_vector_response)

# prompt to write code
# query_simple_vector_index("Write a python code that loads document from google docs, builds a simple vector index, and generate a summary response",
#                           "default")
# evaluation: simple, effective, but needs more explaination

# prompt to explain concept
# query_simple_vector_index("Explain the difference betweeen each response mode when querying any index, give reference to the pdf document",
#                           "default")
# evaluation: accurate but not detailed and not wholistic, ignored other response modes somehow

# prompt to explain concept
# query_simple_vector_index("List every non-recursive mode when querying an index and explain when to use each of them.",
#                           "default")
# evaluation: still ignored other response modes, a bit too concise and not detailed enough