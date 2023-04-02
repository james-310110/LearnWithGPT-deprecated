import os
import sys
import json
from pathlib import Path
from llama_index import download_loader, GPTSimpleVectorIndex

def build_simple_vector_index_from_pdf(file_name):
  # initializing pdf reader
  CJKPDFReader = download_loader('CJKPDFReader')
  file_name_prefix = os.path.splitext(file_name)[0]
  # loading pdf into documents
  try:
    # loading pdf into documents
    pdf = CJKPDFReader().load_data(file=Path('../data/'+file_name))
    print("[Progress] "+file_name+" loaded")
    # building simple vector index from documents
    simple_vector_index = GPTSimpleVectorIndex.from_documents(pdf)
    print("[Progress] "+file_name_prefix+" indexed")
    # saving simple vector index to disk
    simple_vector_index.save_to_disk(file_name_prefix+'-index.json')
    print("[Success] Index stored in "+file_name_prefix+'-index.json')
  except Exception as e:
    print("[Error] File not found in data folder, please check the file name and extension.")
  
# loading openai api key from json file
with open('../keys_and_tokens.json', 'r') as f:
    data = json.load(f)
    openai_api_key = data.get("openai-api-key")
    if openai_api_key:
      os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
      print("openai_api_key not found in JSON file")
      
if len(sys.argv) != 2:
  print("[Error] Incorrect Argument: input the name of pdf put in data folder, with extension included.")
else:
  print("[Progress] building index... do not exit the terminal")
  build_simple_vector_index_from_pdf(sys.argv[1])