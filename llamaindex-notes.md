
## Steps
### Set-up
- run `conda env create -f env.yml` to install python environment and dependencies
- import `llamaindex` into your python script
### Building Index
```python
documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleVectorIndex.from_documents(documents)
```
### Querying Index
```python
response = index.query("<query>", response_mode="<mode>")
```

## [Examples](https://github.com/jerryjliu/llama_index/tree/main/examples)

### [Data connectors](https://gpt-index.readthedocs.io/en/latest/how_to/data_connectors.html)
- local file directory: `SimpleDirectoryReader`
- Google Docs: `GoogleDocsReader`
- else: `NotionPageReader`, `SlackReader`, `DiscordReader`
- [community data connectors](https://llamahub.ai)
- example
```python
from llama_index import GPTSimpleVectorIndex, download_loader
GoogleDocsReader = download_loader('GoogleDocsReader')
gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
loader = GoogleDocsReader()
documents = loader.load_data(document_ids=gdoc_ids)
index = GPTSimpleVectorIndex.from_documents(documents)
index.query('Where did the author go to school?')
```

### [Index Structures](https://gpt-index.readthedocs.io/en/latest/guides/primer/index_guide.html)
- index is a sequence of nodes where each node is a chunk of text from documents
- `.query` loads all or parts of nodes into Response Synthesis module
- types of index
  - list index: loads all nodes
  - vector store index: pairs each node with an embedding
  - tree index: builds a hierachical tree from node set
  - keyword table index: builds a mapping from keywords to nodes
- response synthesis
  - setting [response mode](https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html#setting-response-mode)
  - create and refine: one node at a time
  - tree summarize: bottom-up tree traversal
- modifying index
  - creation
    - `index = GPTSimpleVectorIndex.from_documents(loader.load_data())`
    - `doc_chunks = [Document(text, doc_id=f"doc_id_{i}")...]`
  - insertion
    - `index.insert(doc_chunks[i])`
  - deletion
    - `index.delete("doc_id_0")`
  - update
    - `index.update(doc_chunks[0])`
- [**composing a graph**](https://gpt-index.readthedocs.io/en/latest/how_to/index_structs/composability.html)
  - compose a graph made up of indices and use query the graph instead
    - `doc_i = SimpleDirectoryReader('data_i').load_data()`
    - `index_i = GPTTreeIndex.from_documents(doc_i)`
    - `index_i_summary = str(index_i.query("<summary_prompt>", mode="summarize"))`
    - `graph = ComposableGraph.build_from_indices(GPTListIndex, index_list, index_summaries=index_summaries)`
    - `graph.save_to_disk("save_path.json")`
    - `graph = ComposableGraph.load_from_disk("save_path.json")`
  - [query a graph recursively top down](https://gpt-index.readthedocs.io/en/latest/reference/indices/composability_query.html)

### [Query Interface](https://gpt-index.readthedocs.io/en/latest/guides/primer/usage_pattern.html#load-in-documents)
- to continue...




# TODOs
- [ ] setting response mode
- [ ] query a graph top down