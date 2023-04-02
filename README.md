# LearnWithGPT

A helpful webapp that inputs web links or local files, paired with user query, and outputs a detailed summary with structures and references.

# On this repository

### To run:

1. go to [open-ai](https://platform.openai.com/account/api-keys) to find your own key and copy it
2. create an 'keys_and_tokens.json' file in the root directory and paste your key in the following format

```json
{ "openai-api-key": "<your_key_here>" }
```

3. go to root directory
4. run `yarn install`
5. run `node chatgpt.js`
6. run `conda env create -f env.yml` to install python environment and dependencies
7. run `conda activate feed-gpt` to activate python environment

### To develop:

1. after pulling from main branch, run `git checkout -b new-branch-name`
2. to push your changes, run `git push origin <your-branch-name>`, note that if it's your first time pushing to your branch, you may need to run `git push --set-upstream origin <your-branch-name>` instead.

### JavaScript Code Base

1. Currently using an open-source [chatgpt](https://github.com/transitive-bullshit/chatgpt-api) library to interact with openai
2. Also check out open-ai's official [documentation](https://platform.openai.com/docs/api-reference/introduction) for help.
3. See how to change completionParameters at open-ai's [playground](https://platform.openai.com/playground?mode=chat)
4. ChatGPT is able to reference up to 3000words/4000tokens from the current conversation, according to [Raf](https://help.openai.com/en/articles/6787051-does-chatgpt-remember-what-happened-earlier-in-the-conversation). However [u/kmdr](https://www.reddit.com/r/ChatGPT/comments/zz36n5/an_experiment_on_chatgpts_memory/) also pointed out that this cap is not strict. By reseeding basic information, ChatGPT is able to recall data 10,000 words before.
5. Any single message sent to ChatGPT is capped at 6144characters, according to testing.

### JavaScript Code Workflow

1. Fetch transcript from youtube url in scraper.js
2. Prep chatgpt so that we can send multiple messages containing parts of the transcript
3. Send transcript blocks to chatgpt
4. Instruct chatgpt to generate a summary based on the instructed goals and formats
5. Log the summary in console

### Python Code Base

1. Currently using [LlamaIndex](https://github.com/jerryjliu/llama_index) for data augmentation
2. Data augmentation currently in exploration, see relevant code in `server` directory

### Python Code Workflow

1. loading documents
   - comparing different connectors:
     - pdfs
     - htmls
     - github repo
     - webpage endpoints
   - dividing documents into chunks/nodes
2. building indices
   - comparing different indices:
     - simple vector index
     - list index
     - vector store index
     - tree index
     - keyword table index
     - graph index
   - comparing service contexts(llm_predictor and prompt_helper)
3. making queries
   - comparing parameters
     - mode
     - response_mode
     - required_keywords and exclude_keywords
   - comparing queries to different indices
   - comparing query transformations
   - comparing [prompts](https://gpt-index.readthedocs.io/en/latest/reference/prompts.html)
4. pipeline -> interface [streamlit](https://streamlit.io/)
   - input parsing
   - output parsing

# Notes on the go

1. What is the relationship between prompt and query in LlamaIndex?

```quote
In LlamaIndex, prompts are typically passed in during query-time, not during index construction. Prompts are used to provide additional context to the query and can be used to customize the query. For instance, the QuestionAnswerPrompt and RefinePrompt are used during query-time to synthesize an answer. Some indices do use prompts during index construction to build the index; for instance, GPTTreeIndex uses a SummaryPrompt to hierarchically summarize the nodes, and GPTKeywordTableIndex uses a KeywordExtractPrompt to extract keywords. The user may provide their own prompt or use the default prompts provided by LlamaIndex. Additionally, LlamaIndex also provides an Optimizers module which consists of ways for users to optimize for token usage. This module can be used to compare the outputs without optimization and with.
```

# TODOs

- more important and urgent
  - [x] build POC to learn documentation
  - [x] learn **Customization**
  - [ ] finalize workflow/pipeline
  - [ ] understand [vector stores](https://gpt-index.readthedocs.io/en/latest/how_to/integrations/vector_stores.html)
- less important and urgent
  - [x] learn **Examples for POC/MVP**
  - [x] checkout existing [webapps](https://gpt-index.readthedocs.io/en/latest/gallery/app_showcase.html) for reference
- less important and urgent
  - [ ] collect more prompts to compare and evaluate results
  - [ ] build and compare more indices
  - [ ] figure out how to load documents from web url (get all endpoints from a basepoint)
  - [ ] build and compare indices built from graphs and non-graphs
  - [ ] find resources on prompt engineering for structured output
  - [ ] learn prompt engineering for structured output
  - [ ] figure out a way to benchmark/compare structured output
  - [ ] study pdf reader and find out if figures and tables can be accurately read
- less important and not urgent
  - [ ] learn **Analysis and Optimization**
  - [ ] learn **Integrations\*\***

_see references from notes below_
_notes below is copied from `LlamaIndex Notes`_
_use obsidian or other markdown viewers for better readability_

# Starter Tutorials

### Set-up

- run `conda env create -f env.yml` to install python environment and dependencies
- import `llamaindex` into your python script

### Building Index

```python
from llama_index import SimpleDirectoryReader,GPTSimpleVectorIndex
documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleVectorIndex.from_documents(documents)
```

### Querying Index

```python
response = index.query("<query>", response_mode="<mode>")
```

# Key Components

## Data connectors

- ### types of connectors
  - local file directory: `SimpleDirectoryReader`
  - Google Docs: `GoogleDocsReader`
  - else: `NotionPageReader`, `SlackReader`, `DiscordReader`
  - [community data connectors](https://llamahub.ai)
- ### example of built-in connectors
  ```python
  from llama_index import GPTSimpleVectorIndex, download_loader
  GoogleDocsReader = download_loader('GoogleDocsReader')
  gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
  loader = GoogleDocsReader()
  documents = loader.load_data(document_ids=gdoc_ids)
  index = GPTSimpleVectorIndex.from_documents(documents)
  index.query('Where did the author go to school?')
  ```

## Index Structures

- conceptual
  - index is a sequence of nodes where each node is a chunk of text from documents
  - `.query` loads all or parts of nodes into Response Synthesis module
- types of index
  - list index: loads all nodes
  - vector store index: pairs each node with an embedding
  - tree index: builds a hierachical tree from node set
  - keyword table index: builds a mapping from keywords to nodes
- response synthesis
  - [setting response mode](https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html#setting-response-mode)
  - create and refine: one node at a time
  - tree summarize: bottom-up tree traversal
- modifying index
  - creation
  ```python
  index = GPTSimpleVectorIndex.from_documents(loader.load_data())
  documents = [Document(text, doc_id=f"doc_id_{i}")...]
  ```
  - insertion
  ```python
  index.insert(documents[i])
  ```
  - deletion
  ```python
  index.delete("doc_id_0")
  ```
  - update
  ```python
  index.update(documents[0])
  ```
- [**composing a graph**](https://gpt-index.readthedocs.io/en/latest/how_to/index_structs/composability.html)
  - compose a graph made up of indices and use query the graph instead
  ```python
  doc_i = SimpleDirectoryReader('data_i').load_data()
  index_i = GPTTreeIndex.from_documents(doc_i)
  index_i_summary = str(index_i.query("<summary_prompt>", mode="summarize"))
  graph = ComposableGraph.build_from_indices(
  	GPTListIndex, index_list, index_summaries=index_summaries)
  graph.save_to_disk("save_path.json")
  graph = ComposableGraph.load_from_disk("save_path.json")
  ```
  - [query a graph recursively top down](https://gpt-index.readthedocs.io/en/latest/reference/indices/composability_query.html)

## Query Interface

- ### [Usage Pattern](https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html)

  - loading documents through data loader or document struct

    ```python
    from llama_index import SimpleDirectoryReader
    documents = SimpleDirectoryReader('data').load_data()

    from llama_index import Document
    text_list = [text1, text2, ...]
    documents = [Document(t) for t in text_list]
    ```

  - parsing documents into nodes

    ```python
    from llama_index.node_parser import SimpleNodeParser
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)

    from llama_index.data_structs.node_v2 import Node, DocumentRelationship
    node1 = Node(text="<text_chunk>", doc_id="<node_id>")
    node2 = Node(text="<text_chunk>", doc_id="<node_id>")
    node1.relationships[DocumentRelationship.NEXT] = node2.get_doc_id()
    node2.relationships[DocumentRelationship.PREVIOUS] = node1.get_doc_id()
    ```

  - constructing index from nodes or documnets

    ```python
    from llama_index import GPTSimpleVectorIndex
    index = GPTSimpleVectorIndex.from_documents(documents)

    from llama_index import GPTSimpleVectorIndex
    index = GPTSimpleVectorIndex(nodes)
    ```

    - [customizing LLMs](https://gpt-index.readthedocs.io/en/latest/how_to/customization/custom_llms.html)

      ```python
      from llama_index import LLMPredictor # defining llm
      llm_predictor = LLMPredictor(llm=OpenAI(temperature=0,
      model_name="text-davinci-003")) # define prompt helper
      # set maximum input size
      max_input_size = 4096
      # set number of output tokens
      num_output = 256
      # set maximum chunk overlap
      max_chunk_overlap = 20
      prompt_helper = PromptHelper(
      max_input_size, num_output, max_chunk_overlap)
      # set index configuration
      service_context = ServiceContext.from_defaults(
      llm_predictor=llm_predictor, prompt_helper=prompt_helper)
      # construct index
      index = GPTSimpleVectorIndex.from_documents(
      documents, service_context=service_context
      )
      ```

      ```

      ```

    - [customizing prompts](https://gpt-index.readthedocs.io/en/latest/how_to/customization/custom_prompts.html)
    - [customizing embeddings](https://gpt-index.readthedocs.io/en/latest/how_to/customization/embeddings.html#custom-embeddings)

  - [building indices on top of other indices](https://gpt-index.readthedocs.io/en/latest/how_to/index_structs/composability.html)
    ```python
    from llama_index import GPTSimpleVectorIndex, GPTListIndex
    index1 = GPTSimpleVectorIndex.from_documents(documents1)
    index2 = GPTSimpleVectorIndex.from_documents(documents2)
    index1.set_text("summary1")
    index2.set_text("summary2")
    index3 = GPTListIndex([index1, index2])
    ```
  - [querying the index](https://gpt-index.readthedocs.io/en/latest/reference/query.html)
    - response_mode
      - default: querying mode
      - retrieve
      - embedding
      - summarize: hierachical summarization in tree index
      - simple: keyword extraction
      - rake: keyword extraction
      - recursive: recursively query over composed indices
    ```python
    index = GPTListIndex.from_documents(documents)
    # mode="default"
    response = index.query("<question>", mode="default")
    # mode="embedding"
    response = index.query("<question>", mode="embedding")
    index.query(
        "<question>",
        required_keywords=["Combinator"],
        exclude_keywords=["Italy"]
    )
    ```
  - parsing/formating the [response](https://gpt-index.readthedocs.io/en/latest/reference/response.html)
    ```python
    response = index.query("<question>", verbose=True)
    display(Markdown(f"<b>{response}</b>"))
    ```

- ### [Query Transformation](https://gpt-index.readthedocs.io/en/latest/how_to/query/query_transformations.html)

  - HypotheticalDocumentEmbedding
    - [conceptual explaination](http://boston.lti.cs.cmu.edu/luyug/HyDE/HyDE.pdf)
    - [notebook example](https://github.com/jerryjliu/llama_index/blob/main/examples/query_transformations/HyDEQueryTransformDemo.ipynb)
  - single-step query decomposition

    ```python
    # Setting: a list index composed over multiple vector indices
    # llm_predictor_chatgpt corresponds to the ChatGPT LLM interface
    from llama_index.indices.query.query_transform.base import DecomposeQueryTransform
    decompose_transform = DecomposeQueryTransform(
        llm_predictor_chatgpt, verbose=True
    )

    # initialize indexes and graph
    ...

    # set query config
    query_configs = [
        {
            "index_struct_type": "simple_dict",
            "query_mode": "default",
            "query_kwargs": {
                "similarity_top_k": 1
            },
            # NOTE: set query transform for subindices
            "query_transform": decompose_transform
        },
        {
            "index_struct_type": "keyword_table",
            "query_mode": "simple",
            "query_kwargs": {
                "response_mode": "tree_summarize",
                "verbose": True
            },
        },
    ]

    query_str = (
        "Compare and contrast the airports in Seattle, Houston, and Toronto. "
    )
    response_chatgpt = graph.query(
        query_str,
        query_configs=query_configs,
        llm_predictor=llm_predictor_chatgpt
    )
    ```

  - multi-step query transformation **_coming soon_**

    ```python
    from llama_index.indices.query.query_transform.base import StepDecomposeQueryTransform
    # gpt-4
    step_decompose_transform = StepDecomposeQueryTransform(
        llm_predictor, verbose=True
    )

    response = index.query(
        "Who was in the first batch of the accelerator program the author started?",
        query_transform=step_decompose_transform,
    )
    ```

## Customization

- ### [Defining LLMs](https://gpt-index.readthedocs.io/en/latest/how_to/customization/custom_llms.html)

  - `index` takes `service_context`
  - `service_context` takes `llm_predictor` and `prompt_helper`
  - `llm_predictor` defines LLM, i.e.
    - model_name
    - temperature
    - max_token
  - `prompt_helper` defines chat configurations, i.e.
    - max_input_size
    - max_output_size
    - max_chunk_overlap
  - example code

    ```python
    from llama_index import (
    	GPTKeywordTableIndex, SimpleDirectoryReader,
    	LLMPredictor, PromptHelper, ServiceContext
    )
    from langchain import OpenAI

    documents = SimpleDirectoryReader('data').load_data()

    # define prompt helper
    max_input_size = 4096
    num_output = 256
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    # define LLM
    llm_predictor = LLMPredictor(
    	llm=OpenAI(
    		temperature=0,
    		model_name="text-davinci-002",
    		max_tokens=num_output)
    )

    service_context = ServiceContext.from_defaults(
    	llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    # build index
    index = GPTKeywordTableIndex.from_documents(
    	documents, service_context=service_context)
    ```

  - define [CustomLLM](https://python.langchain.com/en/latest/modules/models/llms/examples/custom_llm.html) using langchain

- ### [Defining Prompts](https://gpt-index.readthedocs.io/en/latest/reference/prompts.html)
  - KeywordExtractPrompt
  - KnowledgeGraphPrompt
  - PandasPrompt
  - QueryKeywordExtractPrompt
  - QuestionAnswerPrompt
  - RefinePrompt
  - RefineTableContextPrompt
  - SchemaExtractPrompt
  - SimpleInputPrompt
  - SummaryPrompt
  - TableContextPrompt
  - TextToSQLPrompt
  - TreeInsertPrompt
  - TreeSelectMultiplePrompt
  - TreeSelectPrompt
- ### [Embedding Support](https://gpt-index.readthedocs.io/en/latest/how_to/customization/embeddings.html)
  - TODO
- ### [Output Parsing](https://gpt-index.readthedocs.io/en/latest/how_to/output_parsing.html#langchain)
  - formatting instructions for any prompt/query (through `output_parser.format`)
  - “parsing” for LLM outputs (through `output_parser.parse`)
  - [example code](https://gpt-index.readthedocs.io/en/latest/how_to/output_parsing.html)

## Analysis and Optimization

- ### [Cost Predictor](https://gpt-index.readthedocs.io/en/latest/how_to/analysis/cost_analysis.html)
  - TODO
- ### [Cost Optimizers](https://gpt-index.readthedocs.io/en/latest/how_to/analysis/optimizers.html)
  - TODO
- ### [Combinations Comparison](https://gpt-index.readthedocs.io/en/latest/how_to/analysis/playground.html)
  - TODO

## Integrations

- ### [Using Vector Stores](https://gpt-index.readthedocs.io/en/latest/how_to/integrations/vector_stores.html)
  - TODO
- ### [Using Langchain](https://gpt-index.readthedocs.io/en/latest/how_to/integrations/using_with_langchain.html)
  - TODO
- ### [Using ChatGPT Plugins](https://gpt-index.readthedocs.io/en/latest/how_to/integrations/chatgpt_plugins.html)
  - ignore for now

# References

## Main information

- [LlamaIndex Documentation](https://gpt-index.readthedocs.io/en/latest/index.html)
- [LlamaIndex Github](https://github.com/jerryjliu/llama_index)
- [langchain Documentation](https://docs.langchain.com/docs/)
- [langchain Github](https://github.com/hwchase17/langchain)

## Data Loaders

- [Llama Hub for Data Loaders](https://llamahub.ai)
- [How to add Data Loaders](https://github.com/emptycrown/llama-hub/tree/main)

## Examples for POC/MVP

- [How to build a POC](https://github.com/logan-markewich/llama_index_starter_pack)
- [How to build PDF reader](https://github.com/0xmerkle/llama-index-pdf-loader-simple/blob/main/main.py)
- [How to build Twitter finder](https://github.com/0xmerkle/llama-index-twitter/blob/main/twitter_main.py)
- [How to build a Chatbot](https://gpt-index.readthedocs.io/en/latest/guides/tutorials/building_a_chatbot.html)
- [How to build a Web App](https://gpt-index.readthedocs.io/en/latest/guides/tutorials/fullstack_app_guide.html)
- [How to augment with Structured Data](https://gpt-index.readthedocs.io/en/latest/guides/tutorials/sql_guide.html)
- [How to augment with SEC Filings](https://medium.com/@jerryjliu98/how-unstructured-and-llamaindex-can-help-bring-the-power-of-llms-to-your-own-data-3657d063e30d)https://medium.com/@jerryjliu98/how-unstructured-and-llamaindex-can-help-bring-the-power-of-llms-to-your-own-data-3657d063e30d
- [**Example Notebooks**](https://github.com/jerryjliu/llama_index/tree/main/examples)
- [**Example WebApps**](https://gpt-index.readthedocs.io/en/latest/gallery/app_showcase.html)
