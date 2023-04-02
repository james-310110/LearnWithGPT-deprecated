import os
import sys
import json
from llama_index import GPTSimpleVectorIndex

def load_simple_vector_index_from_pdf(name):
  return GPTSimpleVectorIndex.load_from_disk(name+'-index.json')
  
def query_simple_vector_index(index, prompt):
  return index.query(prompt, mode="default")
  
# loading openai api key from json file
with open('../keys_and_tokens.json', 'r') as f:
    data = json.load(f)
    openai_api_key = data.get("openai-api-key")
    if openai_api_key:
      os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
      print("openai_api_key not found in JSON file")

if len(sys.argv) != 3:
  print("[Error] Incorrect Argument: expect argument 1 to be the name of the pdf and argument 2 to be the question to ask wrapped in double quotes.")
else:
  index = load_simple_vector_index_from_pdf(sys.argv[1])
  print("[Progress] "+sys.argv[1]+" loaded")
  question = sys.argv[2]
  answer = query_simple_vector_index(index, question)
  print("[Success] Answer generated below: ")
  print(answer)