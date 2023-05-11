import os
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from dotenv import load_dotenv
import math

import ipdb


load_dotenv()


def get_transcript(link):
    video_id = re.findall(
        r"https:\/\/.*\/(?:watch\?v=)?(?P<video_id>[\w-]+)", link
    )[0]
    transcript_response = YouTubeTranscriptApi.get_transcripts(
        [video_id], languages=["pt", "en"]
    )
    # transcript_list = [t['text'] for t in transcript[0][video_id]]
    blocks = math.ceil(
        transcript_response[0][video_id][-1]["start"] / (60 * 5)
    )
    for i in range(blocks):
        print((i + 1) * 300)
        banan.append(
            [
                t["text"]
                for t in response[0][video_id]
                if t["start"] > (i) * 300 and t["start"] <= (i + 1) * 300
            ]
        )
    transcript_list = [t["text"] for t in transcript_response[0][video_id]]
    ipdb.set_trace()
    return " ".join(transcript_list)


def get_summary(transcript):
    openai.api_key = os.getenv("OPENAI_API")
    # response = openai.Completion.create(
    #     engine='text-davinci-003',
    #     prompt=f'Esse texto é uma transcrição de uma video do youtube. Pode resumir, mas mantendo todos pontos principais discutidos? {transcript}',
    #     temperature=0.9,
    #     max_tokens=2048,
    #     n=1,
    #     stop=None
    # )
    # ipdb.set_trace()
    # return response['text']
    return "oi"


link = sys.argv[1]
transcript = get_transcript(link)
summary = get_summary(transcript)
print(summary)
