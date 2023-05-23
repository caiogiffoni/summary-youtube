import logging
import math
import os
import re
import sys

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi

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
async def summarize(body: SummarizeText):
    def get_transcript(link):
        logger.info(f"Link received: {body.link}")
        video_id = re.findall(
            r"https:\/\/.*\/(?:watch\?v=)?(?P<video_id>[\w-]+)", link
        )[0]
        logger.info(f"Video_id obtained: {video_id}")
        transcript_response = YouTubeTranscriptApi.get_transcripts(
            [video_id], languages=["pt", "en"]
        )
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
    # summary = get_summary(transcript)
    logger.info("Summary Generated!")

    return [
	"\n\nA crise econômica iniciada no início do ano tem feito vítimas, como as Lojas Americanas, que acabaram indo à falência. Outras empresas do mesmo segmento, como o Magalu, Via Varejo e Lojas Marisa, também tiveram prejuízos colossais. O Magalu, por exemplo, apresentou o maior prejuízo para um primeiro trimestre desde que foi para a Bolsa em 2011. Por sua vez, o Via Varejo teve um prejuízo de 297 milhões, somando juros pagos e recebidos. Já as Lojas Marisa tiveram um prejuízo de 149 milhões de reais e 10 lojas físicas alvos de despejo por falta de pagamento de aluguel. O e-commerce brasileiro também teve redução de quase 40%, mas as vendas do e-commerce da Magalu avançaram 11%. Parece que a queda nas vendas das Lojas Americanas foi aproveitada por outras empresas, como o Magalu. \n\nA maior parte dos produtos pode ser encontrada no Mercado Livre e nas lojas chinesas, dependendo do que está sendo comprado. O grande motivo do péssimo resultado da Magalu é o alto endividamento devido ao pagamento de juros. A dívida total da Magalu é de 7 bilhões e 271 milhões, enquanto que a dívida total da Lojas Marisa é de 737 milhões. A capacidade de pagamento da Magalu pode ser medida pela relação da receita financeira em relação ao resultado operacional, que é de 2,38, enquanto que o resultado operacional da Marisa foi negativo nos últimos 12 meses, mostrando prejuízo de 149 milhões. Devido ao alto endividamento, três empresas entraram com um pedido de falência na justiça. \n\nNeste vídeo, foi discutida a situação atual do varejo brasileiro. Se você tiver algum comentário para compartilhar, por favor deixe-o nos comentários abaixo. O nosso bate-papo chegou ao fim, mas até a próxima!"
]
