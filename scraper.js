import jsdom from "jsdom";

async function fetchTranscriptUrl(videoUrl) {
  try {
    const response = await fetch(videoUrl);
    if (!response.ok) {
      throw new Error("Failed to fetch the video page");
    }
    const html = await response.text();
    const dom = new jsdom.JSDOM(html);
    const doc =
      dom.window.document.getElementById("watch7-content").nextElementSibling;
    if (!doc) {
      throw new Error("Failed to find the video element");
    }
    const haystack = doc.innerHTML;
    const needle =
      /"captions":{"playerCaptionsTracklistRenderer":{"captionTracks":\[{"baseUrl":"([^"]+)"/;
    const match = haystack.match(needle);
    if (!match) {
      throw new Error("Failed to find the transcript URL");
    }
    const transcriptUrl = match[1].replace(/\\u0026/g, "&");
    return transcriptUrl;
  } catch (error) {
    console.log(
      "An error occurred while fetching the transcriptUrl: " + error.message
    );
    return null;
  }
}

async function fetchTranscriptContent(transcriptUrl) {
  try {
    // fetching transcript content
    const response = await fetch(transcriptUrl);
    if (!response.ok) {
      throw new Error("Failed to fetch the transcript page");
    }
    const xml = await response.text();
    const dom = new jsdom.JSDOM("");
    const domParser = dom.window.DOMParser;
    const parser = new domParser();
    const xmlDoc = parser.parseFromString(xml, "text/xml");
    const transcriptContent = extractTimestampsAndTexts(xmlDoc);
    return joinDialogues(transcriptContent);
  } catch (error) {
    console.log(
      "An error occurred while fetching the transcriptContent: " + error.message
    );
    return null;
  }
}

function extractTimestampsAndTexts(xmlDoc) {
  try {
    const transcripts = [];
    const textElements = Array.from(xmlDoc.getElementsByTagName("text"));
    if (!textElements) {
      throw new Error("Failed to find the transcript transcript elements");
    }
    textElements.forEach((line) => {
      const start = line.getAttribute("start");
      const duration = line.getAttribute("dur");
      const end = parseInt(start) + parseInt(duration);
      const text = line.textContent.replace(/&#(\d+);/g, (_match, capture) =>
        String.fromCharCode(capture)
      );
      transcripts.push({ start: parseInt(start), end: end, text: text });
    });
    return transcripts;
  } catch (error) {
    return [];
  }
}

function joinDialogues(transcript) {
  for (let i = 0; i < transcript.length - 1; i++) {
    const current = transcript[i];
    const next = transcript[i + 1];
    if (next && current.end >= next.start) {
      current.text += ` ${next.text}`;
      transcript.splice(i + 1, 1);
      i--;
    }
  }
  return transcript;
}

async function getTranscriptFromYoutube(videoUrl) {
  try {
    const transcriptUrl = await fetchTranscriptUrl(videoUrl);
    const transcriptContent = await fetchTranscriptContent(transcriptUrl);
    return transcriptContent;
  } catch (error) {
    console.log(
      "An error occurred while fetching the transcript: " + error.message
    );
    return null;
  }
}

export { getTranscriptFromYoutube };
