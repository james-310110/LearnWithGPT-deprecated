# youtube-summarizer
A helpful webapp that takes in a youtube video url and outputs a detailed summary with highlights and timestamps included.

# To run:
1. go to root directory
2. run `yarn install`
3. run `node chatgpt.js`

# Development Logs

## Workflow

1. Fetch transcript from youtube url in scraper.js
2. Prep chatgpt so that we can send multiple messages containing parts of the transcript
3. Send transcript blocks to chatgpt
4. Instruct chatgpt to generate a summary based on the instructed goals and formats
5. Log the summary in console

## TODOs:
1. Figure out the maximum length of a message that chatgpt can handle
2. Figure out how to tell chatgpt to shut up while we send the transcript blocks
3. Figure out how to tell chatgpt to summarize based on our instructions

The current instructions do not work very well but serve as a good starting ground.
Experiment with it however you like.

Sample [Youtube Video](https://www.youtube.com/watch?v=RYDiDpW2VkM)

Sample [Transcript](https://www.youtube.com/api/timedtext?v=RYDiDpW2VkM&caps=asr&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1678192888&sparams=ip,ipbits,expire,v,caps,xoaf&signature=087B3C118245D74861054827746B033A7A7CF8E7.4BA604B798CEF2CF647D56579D05B7FA38B8AFE2&key=yt8&lang=en)

Sample response from the current instructions:

One-sentence summary: The video discusses the different types of machine learning algorithms, their applications, and how they work, covering supervised, unsupervised, semi-supervised, and reinforcement learning.

Detailed summary:

Introduction (0:00 - 0:40): The video provides an overview of the different types of machine learning algorithms and their applications.
Supervised Learning (0:40 - 4:32): The video explains how supervised learning works, including classification and regression problems, feature engineering, and evaluation metrics.
Unsupervised Learning (4:32 - 7:39): The video discusses unsupervised learning, including clustering, dimensionality reduction, and anomaly detection.
Semi-Supervised Learning (7:39 - 9:43): The video describes semi-supervised learning, which is a combination of supervised and unsupervised learning, and its use cases.
Reinforcement Learning (9:43 - 12:10): The video covers reinforcement learning, which is used for decision making in dynamic environments and its applications.
Conclusion (12:10 - 12:40): The video summarizes the different types of machine learning algorithms and their use cases.
