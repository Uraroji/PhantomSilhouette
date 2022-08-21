from typing import List
import librosa
import pyworld as pw
import soundfile as sf
import numpy as np
from PhantomSilhouette import phantom_silhouette


def pan(wav: List[np.ndarray], right_ratio: float = 0) -> List[np.ndarray]:
    """
    パン

    Parameters
    ----------
    wav: np.ndarray
        音声波形
    right_ratio: float
        右の音量の割合(-1~1, default 0)

    Returns
    ----------
    wav_out: np.ndarray
        パンした音声
    """
    wav[0] = wav[0] * (1 - right_ratio)
    wav[1] = wav[1] * (1 + right_ratio)
    return wav


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
    wav, sample_rate = librosa.load("suzuki.wav", mono=False)
    wav[0] = convert(wav[0], sample_rate)
    wav[1] = convert(wav[1], sample_rate)
    wav = pan(wav, right_ratio=0)
    audio_out = wav.transpose()
    sf.write("out.wav", audio_out, sample_rate, format="WAV", subtype="PCM_16")
