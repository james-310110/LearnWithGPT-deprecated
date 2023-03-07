import { ChatGPTAPI } from "chatgpt";
import { OPENAI_API_KEY } from "./config.js";
import { getTranscriptFromYoutube } from "./scraper.js";

async function initializeAPI() {
  const api = new ChatGPTAPI({
    apiKey: OPENAI_API_KEY,
    completionParams: {
      temperature: 0.25,
      max_tokens: 2048,
      top_p: 0.95,
      frequency_penalty: 0,
      presence_penalty: 0,
    },
    // debug: true,
  });
  const configuration = {
    // print the partial response as the AI is "typing"
    // onProgress: (partialResponse) => console.log(partialResponse.text),
    // timeout after 1 minute
    timeoutMs: 1 * 60 * 1000,
  };
  return api;
  // const res = await api.sendMessage("Who is Obama?");
  // console.log(res);
}

async function main() {
  // const api = await initializeAPI();
  // const transcript = await getTranscriptFromYoutube();
  // const resp = await api.sendMessage(
  //   "Generate bulelted summaries with timestamps for the transcript below." +
  //     JSON.stringify(transcript)
  // );
  // console.log(resp.text);
  const api = await initializeAPI();
  const videoUrl = "https://www.youtube.com/watch?v=RYDiDpW2VkM";
  const transcript = await getTranscriptFromYoutube(videoUrl);
  let instruction = await api.sendMessage(
    "Generate a bulelted list of summaries with timestamps for the transcript I'm going to send you."
  );
  // send a message and wait for the response
  let res = await api.sendMessage(JSON.stringify(transcript).slice(0, 4086), {
    parentMessageId: instruction.id,
  });
  console.log(res.text);

  // // send a follow-up
  // res = await api.sendMessage("Can you expand on that?", {
  //   parentMessageId: res.id,
  // });
  // console.log(res.text);

  // // send another follow-up
  // res = await api.sendMessage("What were we talking about?", {
  //   parentMessageId: res.id,
  // });
  // console.log(res.text);
}
main();

/**
 * Workflow
 *
 * 1. prep chatgpt so that we can send multiple messages containing parts of the transcript
 * 2. send transcript blocks to chatgpt
 * 3. instruct chatgpt to generate a summary based on the instructed goals and formats
 * 4. log the summary in console
 *
 * TODO:
 * 1. figure out the maximum length of a message that chatgpt can handle
 * 2. figure out how to tell chatgpt to shut up while we send the transcript blocks
 * 3. figure out how to tell chatgpt to summarize based on our instructions
 *
 * The current instructions do not work very well but serve as a good starting ground.
 * Experiment with it however you like.
 *
 * Sample Youtube Video: https://www.youtube.com/watch?v=RYDiDpW2VkM
 * Sample Transcript: https://www.youtube.com/api/timedtext?v=RYDiDpW2VkM&caps=asr&xoaf=5&hl=en&ip=0.0.0.0&ipbits=0&expire=1678192888&sparams=ip,ipbits,expire,v,caps,xoaf&signature=087B3C118245D74861054827746B033A7A7CF8E7.4BA604B798CEF2CF647D56579D05B7FA38B8AFE2&key=yt8&lang=en
 * Sample response from the current instructions:
 *
 * One-sentence summary: The video discusses the different types of machine learning algorithms, their applications, and how they work, covering supervised, unsupervised, semi-supervised, and reinforcement learning.
 *
 * Detailed summary:
 *
 * Introduction (0:00 - 0:40): The video provides an overview of the different types of machine learning algorithms and their applications.
 * Supervised Learning (0:40 - 4:32): The video explains how supervised learning works, including classification and regression problems, feature engineering, and evaluation metrics.
 * Unsupervised Learning (4:32 - 7:39): The video discusses unsupervised learning, including clustering, dimensionality reduction, and anomaly detection.
 * Semi-Supervised Learning (7:39 - 9:43): The video describes semi-supervised learning, which is a combination of supervised and unsupervised learning, and its use cases.
 * Reinforcement Learning (9:43 - 12:10): The video covers reinforcement learning, which is used for decision making in dynamic environments and its applications.
 * Conclusion (12:10 - 12:40): The video summarizes the different types of machine learning algorithms and their use cases.
 *
 *
 *
 */
