import librosa
import soundfile as sf
import pyworld as pw
import numpy as np
from PhantomSilhouette import phantom_silhouette

def convert(wav, sr):
    wav = wav.astype(np.float64)
    f0, sp, ap = pw.wav2world(wav, sr)
    f0_out, sp_out = phantom_silhouette(f0, sp, sr)
    wev_out = pw.synthesize(f0_out, sp_out, ap, sr)
    wav_out = wev_out.astype(np.float32)[:wav.shape[0]]
    return wav_out

if __name__ == '__main__':
    wav, sr = librosa.load('suzuki.wav', mono=False)
    wav[0] = convert(wav[0], sr) * 1.8
    wav[1] = convert(wav[1], sr) * 0.2
    sf.write('./wav_out.wav', wav.T, sr)