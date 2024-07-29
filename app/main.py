from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import edge_tts
import uvicorn
import base64
import os,time

app = FastAPI()

class TextToSpeechRequest(BaseModel):
    text: str
    voice: str = "en-US-JennyNeural"

@app.post("/text-to-speech/")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        communicate = edge_tts.Communicate(text=request.text, voice=request.voice)
        filename = "output_"+str(time.time)+".mp3"
        await communicate.save(filename)

        with open(filename, "rb") as file:
            audio_data = base64.b64encode(file.read()).decode("utf-8")

        # Clean up the generated file
        os.remove(filename)

        return {"audio": audio_data}
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
