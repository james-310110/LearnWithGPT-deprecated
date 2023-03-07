import { ChatGPTAPI } from "chatgpt";
import { OPENAI_API_KEY } from "./openai-api-key.js";
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
}
main();