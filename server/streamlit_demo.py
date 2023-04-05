import os
import json
from urllib.parse import urlparse
import streamlit as st
from scrape_utils import scrape
from llama_index import download_loader, GPTSimpleVectorIndex, SimpleDirectoryReader, ServiceContext, LLMPredictor, PromptHelper
from llama_index.llm_predictor.chatgpt import ChatGPTLLMPredictor
from llama_index.node_parser import SimpleNodeParser
from langchain import OpenAI
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory
from llama_index.langchain_helpers.memory_wrapper import GPTIndexChatMemory

index_name = "./index.json"
documents_folder = "./documents"

def get_index_name(input_urls):
    basepoints = input_urls.split('\n')
    index_name = ""
    for basepoint in basepoints:
        index_name += urlparse(basepoint).netloc.split(".")[0] + "&"
    return index_name
    

def load_documents_to_gpt_vectorstore(input_urls):
    index_name = get_index_name(input_urls)
    if os.path.exists("../index/"+index_name+".json"):
        print("index found")
        return GPTSimpleVectorIndex.load_from_disk("../index/"+index_name+".json")
    else:
        print("building new index")
    basepoints = input_urls.split('\n')
    endpoints = scrape(basepoints)
    BeautifulSoupWebReader = download_loader("BeautifulSoupWebReader")
    loader = BeautifulSoupWebReader()
    documents = loader.load_data(endpoints)
    parser = SimpleNodeParser()
    
    nodes = parser.get_nodes_from_documents(documents)
    llm_predictor = LLMPredictor(
        llm=OpenAI(temperature=0, model_name="text-davinci-003")
    )
    
    max_input_size = 4096
    num_output = 2048
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index = GPTSimpleVectorIndex(nodes, service_context=service_context)
    index.save_to_disk("../index/"+index_name+".json")
    return index

def build_conversation(urls):
    index_name = get_index_name(urls)
    if not os.path.exists("../index/"+index_name+".json"):
        return "index not found, click on 'load documents' first"
    else: print("index found")
    index = GPTSimpleVectorIndex.load_from_disk("../index/"+index_name+".json")
    tools = [
        Tool(
            name = "GPT Index",
            func=lambda q: str(index.query(q)),
            description="useful for when you want to answer questions about the author. The input to this tool should be a complete english sentence.",
            return_direct=True
        ),
    ]
    memory = GPTIndexChatMemory(
        index=index, 
        memory_key="chat_history", 
        query_kwargs={"response_mode": "compact"},
        # return_source returns source nodes instead of querying index
        return_source=True,
        # return_messages returns context in message format
        return_messages=True
    )
    llm=OpenAI(temperature=0, model_name="text-davinci-003")
    st.session_state.agent_chain = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory)

def chat(query,urls):
    index_name = get_index_name(urls)
    if not os.path.exists("../index/"+index_name+".json"):
        return "index not found, click on 'load documents' first"
    else: print("index found")
    index = GPTSimpleVectorIndex.load_from_disk("../index/"+index_name+".json")
    tools = [
        Tool(
            name = "GPT Index",
            func=lambda q: str(index.query(q)),
            description="useful for when you want to answer questions about the author. The input to this tool should be a complete english sentence.",
            return_direct=True
        ),
    ]
    memory = GPTIndexChatMemory(
        index=index, 
        memory_key="chat_history", 
        query_kwargs={"response_mode": "compact"},
        # return_source returns source nodes instead of querying index
        return_source=True,
        # return_messages returns context in message format
        return_messages=True
    )
    llm=OpenAI(temperature=0, model_name="text-davinci-003")
    agent_chain = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory)
    response = agent_chain.run(input=query)
    
    # response = st.session_state.agent_chain.run(input=query)
    return response
        

# loading openai api key from json file
with open('../keys_and_tokens.json', 'r') as f:
    data = json.load(f)
    openai_api_key = data.get("openai-api-key")
    if openai_api_key:
      os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
      print("openai_api_key not found in JSON file")


st.header("LearnWithGPT Demo")
st.session_state.agent_chain = None

doc_input = st.text_area("Enter a URL to scrape and index")
if st.button("load documents"):
    st.markdown(load_documents_to_gpt_vectorstore(doc_input))
    build_conversation(doc_input)
    
user_input = st.text_area("ask about the docs")
if st.button("Ask"):
    st.write(chat(user_input, doc_input))
    

# @st.cache_resource
# def initialize_index(index_name, documents_folder):
#     llm_predictor = ChatGPTLLMPredictor()
#     service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
#     if os.path.exists(index_name):
#         index = GPTSimpleVectorIndex.load_from_disk(index_name, service_context=service_context)
#     else:
#         documents = SimpleDirectoryReader(documents_folder).load_data()
#         index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
#         index.save_to_disk(index_name)

#     return index


# @st.cache_data(max_entries=200, persist=True)
# def query_index(_index, query_text):
#     response = _index.query(query_text)
#     return str(response)


# st.title("🦙 Llama Index Demo 🦙")
# st.header("Welcome to the Llama Index Streamlit Demo")
# st.write("Enter a query about Paul Graham's essays. You can check out the original essay [here](https://raw.githubusercontent.com/jerryjliu/llama_index/main/examples/paul_graham_essay/data/paul_graham_essay.txt). Your query will be answered using the essay as context, using embeddings from text-ada-002 and LLM completions from ChatGPT. You can read more about Llama Index and how this works in [our docs!](https://gpt-index.readthedocs.io/en/latest/index.html)")

# index = None
# api_key = st.text_input("Enter your OpenAI API key here:", type="password")

# if api_key:
#     os.environ['OPENAI_API_KEY'] = api_key
#     index = initialize_index(index_name, documents_folder)    


# if index is None:
#     st.warning("Please enter your api key first.")

# text = st.text_input("Query text:", value="What did the author do growing up?")

# if st.button("Run Query") and text is not None:
#     response = query_index(index, text)
#     st.markdown(response)
    
#     llm_col, embed_col = st.columns(2)
#     with llm_col:
#         st.markdown(f"LLM Tokens Used: {index.service_context.llm_predictor._last_token_usage}")
    
#     with embed_col:
#         st.markdown(f"Embedding Tokens Used: {index.service_context.embed_model._last_token_usage}")
