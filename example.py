import librosa
import pyworld as pw
import soundfile as sf
import numpy as np
from PhantomSilhouette import phantom_silhouette


def convert(wav_side: np.ndarray, sr: int) -> np.ndarray:
    """
    phantom silhouette法で音声の変換

    Parameters
    ----------
    wav_side: np.ndarray
        片方の音声
    sr: int
        サンプルレート

    Returns
    ----------
    wav_out: np.ndarray
        変換した音声
    """
    wav = wav_side.astype(np.float64)
    f0, sp, ap = pw.wav2world(wav, sr)
    f0_out, sp_out = phantom_silhouette(f0, sp, sr)
    wev_out = pw.synthesize(f0_out, sp_out, ap, sr)
    return wev_out.astype(np.float32)[: wav.shape[0]]


if __name__ == "__main__":
    wav, sr = librosa.load("sample.wav")
    wav = convert(wav, sr)
    audio_out = wav.transpose()
    sf.write("out.wav", audio_out, sr, format="WAV", subtype="PCM_16")
