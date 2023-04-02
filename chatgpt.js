import { ChatGPTAPI } from "chatgpt";
import OPENAI_API_KEY from "./keys_and_tokens.json" assert { type: "json" };
import { getTranscriptFromYoutube } from "./scraper.js";

async function initializeAPI() {
  const api = new ChatGPTAPI({
    apiKey: OPENAI_API_KEY["openai-api-key"],
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
  // parsing command line argument
  if (process.argv.length !== 3) {
    console.log(
      "[Error] Incorrect Argument: input youtube url as the only argument"
    );
    return;
  }
  console.time("execution time");
  const api = await initializeAPI();
  const videoUrl = process.argv[2];
  const transcript = await getTranscriptFromYoutube(videoUrl);
  let instruction = await api.sendMessage(
    "Generate a bulelted list of summaries with timestamps for the transcript I'm going to send you."
  );
  // send a message and wait for the response
  let res = await api.sendMessage(
    JSON.stringify(transcript).slice(0, 2048 * 3),
    {
      parentMessageId: instruction.id,
    }
  );
  console.log(res.text);
  console.timeEnd("execution time");
}

main();
