# youtube-summarizer
A helpful webapp that takes in a youtube video url and outputs a detailed summary with highlights and timestamps included.

# To run:
1. go to [open-ai](https://platform.openai.com/account/api-keys) to find your own key and copy it
2. create an 'openai-api-key.json' file in the root directory and paste your key in the following format
```json
{"openai-api-key": "<your_key_here>"}
```
3. go to root directory
4. run `yarn install`
5. run `node chatgpt.js`

# To develop:
1. after pulling from main branch, run `git checkout -b new-branch-name`
2. to push your changes, run `git push origin <your-branch-name>`, note that  if it's your first time pushing to your branch, you may need to run `git push --set-upstream origin <your-branch-name>` instead.

# Development Logs

## References and documentation
1. Currently using an open-source [chatgpt](https://github.com/transitive-bullshit/chatgpt-api) library to interact with openai
2. Also check out open-ai's official [documentation](https://platform.openai.com/docs/api-reference/introduction) for help.
3. See how to change completionParameters at open-ai's [playground](https://platform.openai.com/playground?mode=chat)
4. ChatGPT is able to reference up to 3000words/4000tokens from the current conversation, according to [Raf](https://help.openai.com/en/articles/6787051-does-chatgpt-remember-what-happened-earlier-in-the-conversation). However [u/kmdr](https://www.reddit.com/r/ChatGPT/comments/zz36n5/an_experiment_on_chatgpts_memory/) also pointed out that this cap is not strict. By reseeding basic information, ChatGPT is able to recall data 10,000 words before.
5. Any single message sent to ChatGPT is capped at 6144characters, according to testing.

## Feeding data to ChatGPT
1. currently exploring [LlamaIndex](https://github.com/jerryjliu/gpt_index), check out documentation [here](https://gpt-index.readthedocs.io/en/latest/guides/use_cases.html).
2. Friend's advice: 试试官方提供的方法，先转成embedding存到向量数据库，prompt用的时候也走一下OpenAI接口转embedding，在本地向量数据库做一次相似度查询，重组出新的prompt，丢给OpenAI的completion或chat接口。
3. On example of this can be found on [Twitter](https://twitter.com/thejessezhang/status/1615390646763945991), check out PapersGPT demo [here](https://jessezhang.org/llmdemo).


## Workflow

1. Fetch transcript from youtube url in scraper.js
2. Prep chatgpt so that we can send multiple messages containing parts of the transcript
3. Send transcript blocks to chatgpt
4. Instruct chatgpt to generate a summary based on the instructed goals and formats
5. Log the summary in console

## TODOs:
2. Figure out how to tell chatgpt to shut up while we send the transcript blocks
3. Figure out how to tell chatgpt to summarize based on our instructions

The current instructions do not work very well but serve as a good starting ground.
Experiment with it however you like.

Sample [Youtube Video](https://www.youtube.com/watch?v=RYDiDpW2VkM)

Sample [Transcript](https://www.youtube.com/api/timedtext?v=RYDiDpW2VkM&caps=asr&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1678245164&sparams=ip,ipbits,expire,v,caps,xoaf&signature=2EE15D86288738C1A50776B23851AE43FB2BC037.4769EECD27896C49CE27BC54BEDA4804BC13FC3D&key=yt8&lang=en)

Sample response from the current instructions:

One-sentence summary: The video discusses the different types of machine learning algorithms, their applications, and how they work, covering supervised, unsupervised, semi-supervised, and reinforcement learning.

Detailed summary:

Introduction (0:00 - 0:40): The video provides an overview of the different types of machine learning algorithms and their applications.

Supervised Learning (0:40 - 4:32): The video explains how supervised learning works, including classification and regression problems, feature engineering, and evaluation metrics.

Unsupervised Learning (4:32 - 7:39): The video discusses unsupervised learning, including clustering, dimensionality reduction, and anomaly detection.

Semi-Supervised Learning (7:39 - 9:43): The video describes semi-supervised learning, which is a combination of supervised and unsupervised learning, and its use cases.

Reinforcement Learning (9:43 - 12:10): The video covers reinforcement learning, which is used for decision making in dynamic environments and its applications.

Conclusion (12:10 - 12:40): The video summarizes the different types of machine learning algorithms and their use cases.
