import os
import json

with open('../openai-api-key.json', 'r') as f:
    data = json.load(f)
    openai_api_key = data.get("openai-api-key")
    if openai_api_key:
      os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
      print("openai_api_key not found in JSON file")

from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader

# loading data
# documents = SimpleDirectoryReader('data').load_data()
# index = GPTSimpleVectorIndex.from_documents(documents)

# # making queries
# response = index.query("<summarization_query>", response_mode="tree_summarize")
# print(response)

# # save to disk
# index.save_to_disk('index.json')

# load from disk
index = GPTSimpleVectorIndex.load_from_disk('index.json')
response = index.query("What did the author work on?", response_mode="tree_summarize")
print(response)