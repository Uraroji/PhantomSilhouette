from tempfile import NamedTemporaryFile
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PhantomSilhouette import phantom_silhouette
import librosa
import pyworld as pw
import soundfile as sf
import numpy as np


def convert(wav_side: np.ndarray, sr: int) -> np.ndarray:
    wav = wav_side.astype(np.float64)
    f0, sp, ap = pw.wav2world(wav, sr)
    f0_out, sp_out = phantom_silhouette(f0, sp, sr)
    wev_out = pw.synthesize(f0_out, sp_out, ap, sr)
    return wev_out.astype(np.float32)[: wav.shape[0]]


app = FastAPI(
    title="PhantomSilhouette",
    description="Make whisper voice from normal voice",
    version="0.1.0",
)


@app.get("/health_check")
async def health_check():
    """生存確認用エンドポイント"""
    return {"message": "Server is working"}


@app.post("/predict")
async def predict_whisper(file: UploadFile):
    """Make whisper voice from normal voice"""
    if not file.filename.endswith(".wav") or not file.content_type == "audio/wav":
        return {"message": "Invalid file format. This server supports wave file only."}
    with NamedTemporaryFile("wb", delete=False) as f:
        content = await file.read()
        f.write(content)
        f.seek(0)
        wav, sr = librosa.load(f.name)
        wav = convert(wav, sr)
        audio_out = wav.transpose()
        sf.write(f.name, audio_out, sr, format="WAV", subtype="PCM_16")
        return FileResponse(f.name, media_type="audio/wav")


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
