import logging
import math
import os
import re
import sys

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import TranscriptsDisabled, YouTubeTranscriptApi

from app.models import SummarizeText

from .logging_config import LOG_LEVELS

load_dotenv()

app = FastAPI()

logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/summarize")
async def summarize(body: SummarizeText, request: Request):
    if request.headers["authorization"].split(" ")[1] != os.getenv("TOKEN"):
        logger.warn(f"Invalid Token sent")
        raise HTTPException(status_code=401, detail="Invalid token")

    def get_transcript(link):
        if not link:
            logger.warn(f"Invalid link sent")
            raise HTTPException(status_code=400, detail="Invalid link")

        logger.info(f"Link received: {body.link}")
        video_id = re.findall(
            r"https:\/\/.*\/(?:watch\?v=)?(?P<video_id>[\w-]+)", link
        )[0]
        logger.info(f"Video_id obtained: {video_id}")
        try:
            transcript_response = YouTubeTranscriptApi.get_transcripts(
                [video_id], languages=["pt", "en"]
            )
        except TranscriptsDisabled:
            raise HTTPException(status_code=400, detail="AI Token expired")
        seconds = 60 * 5
        blocks = math.ceil(
            transcript_response[0][video_id][-1]["start"] / seconds
        )
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
        logger.info("Generating summary")
        request_length = len(transcript)
        openai.api_key = os.getenv("OPENAI_API")
        if not openai.api_key:
            logger.warn("No token loaded")
            raise HTTPException(status_code=401, detail="AI Token expired")
        response = []
        for idx, part in enumerate(transcript):
            prompt = f"Resuma essa transcição de vídeo do Youtube: '{part}'"
            try:
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
            except:
                logger.warn("Token expired")
                raise HTTPException(status_code=401, detail="AI Token expired")
            logger.info(f"Generated {idx+1} of {request_length}")
        treated_transcript = [t["choices"][0]["text"] for t in response]
        return " ".join(treated_transcript)

    logger.info("Link Received")
    transcript = get_transcript(body.link)
    logger.info(f"Transcript obtained for requested video")
    summary = get_summary(transcript)
    logger.info("Summary Generated!")

    return {summary}
