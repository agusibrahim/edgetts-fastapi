from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import edge_tts
import uvicorn
import base64
import os,time

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "id-ID-ArdiNeural"
    subtitle: bool = False
    words_per_subtitle: int = 8

@app.post("/text-to-speech/")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        communicate = edge_tts.Communicate(text=request.text, voice=request.voice)
        audio_data = bytearray()
        subtitle_data = ""

        if request.subtitle:
            submaker = edge_tts.SubMaker()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.extend(chunk["data"])
            elif chunk["type"] == "WordBoundary" and request.subtitle:
                submaker.merge_cues(request.words_per_subtitle)
                submaker.feed(chunk)

        response = {
            "audio": base64.b64encode(audio_data).decode("utf-8")
        }

        if request.subtitle:
            response["subtitle"] = submaker.get_srt()

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list-languages/")
async def list_languages():
    try:
        voices = await edge_tts.list_voices()
        languages = {voice["ShortName"]: voice["Locale"] for voice in voices}
        return languages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
