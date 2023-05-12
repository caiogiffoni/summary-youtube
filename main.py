import math
import os
import re
import sys

import ipdb
import openai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()


def get_transcript(link):
    video_id = re.findall(
        r"https:\/\/.*\/(?:watch\?v=)?(?P<video_id>[\w-]+)", link
    )[0]
    transcript_response = YouTubeTranscriptApi.get_transcripts(
        [video_id], languages=["pt", "en"]
    )
    # transcript_list = [t['text'] for t in transcript[0][video_id]]
    seconds = 60 * 5
    blocks = math.ceil(transcript_response[0][video_id][-1]["start"] / seconds)
    transcript_list = []
    for i in range(blocks):
        transcript_list.append(
            [
                t["text"]
                for t in transcript_response[0][video_id]
                if t["start"] > (i) * seconds
                and t["start"] <= (i + 1) * seconds
            ]
        )
    return [" ".join(t) for t in transcript_list]


def get_summary(transcript: list):
    openai.api_key = os.getenv("OPENAI_API")
    # transcript_list = [t["text"] for t in transcript_response[0][video_id]]
    response = []
    # ipdb.set_trace()
    for part in transcript:
        # ipdb.set_trace()
        prompt = f"Resuma essa transcição de vídeo do Youtube: '{part}'"
        response.append(
            openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=2048,
                n=1,
                stop=None,
                temperature=0.8,
            )
        )
    treated_transcript = [t["choices"][0]["text"] for t in response]
    return " ".join(treated_transcript)


link = sys.argv[1]
transcript = get_transcript(link)
summary = get_summary(transcript)
print(summary)

# prompt = f"Quero que resuma essa transcição de vídeo do Youtube: {part}"
# promptx = "quanto é 5x5"
# banana = openai.Completion.create(
#     model="text-davinci-003",
#     prompt=promptx,
#     temperature=0.9,
#     max_tokens=2048,
# )
