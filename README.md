# PhantomSilhouette

普通に喋る音声を入れると囁き声に変換されます．

## こんな感じになります(音あり)

https://user-images.githubusercontent.com/34536327/191547222-989b1b77-82d4-4b3e-8bd5-c66bf22e262d.mp4

## 導入の仕方

このライブラリをインストールします．
```sh
pip install git+https://github.com/Uraroji/PhantomSilhouette.git
```

関連のライブラリをインストールします．
```sh
pip install librosa
pip install SoundFile
pip install pyworld
```

Pythonからの簡単な呼び出し方法
```py
import librosa
import pyworld as pw
import soundfile as sf
import numpy as np
from phantomsilhouette import phantom_silhouette


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
    return wev_out.astype(np.float32)[:wav.shape[0]]


if __name__ == "__main__":
    wav, sr = librosa.load("sample.wav")
    wav = convert(wav, sr)
    audio_out = wav.transpose()
    sf.write("out.wav", audio_out, sr, format="WAV", subtype="PCM_16")
```

## 進捗
- [x] PhantomSilhouetteの実装
  - [x] 雑音駆動音声の実装
    - F0を0~1の白色雑音に入れ替え([2] 2.1参照)
  - [x] F1,F2の上方シフトの実装
    - スペクトル包絡を画像的にワープ処理することにより上方シフトを実現([2] 2.2参照)
  - [x] 気息音成分の補填
    - スペクトル包絡の高域部分に正の重みづけ([2] 2.4参照)
  - [x] スペクトル低域抑圧
    - スペクトル包絡の低域部分に負の重みづけ([2] 2.3参照)
- [ ] PhantomSilhouette2の実装
  - [ ] F1,F2帯域の上方シフト量の改良
  - [ ] 高域気息成分の補填量の適応的補正
  - [ ] 低域スペクトルの抑圧対象の拡大

## 参考文献
- [1] Uchida, T. & Morise, M. (2021).  
  A practical method of generating whisper voice: Development of phantom silhouette method and its improvement.  
  Acoustical Science & Technology, 42 (4) 214-217.  
  [https://doi.org/10.1250/ast.42.214](https://doi.org/10.1250/ast.42.214)
- [2] [実用的なささやき声の生成法:Phantom Silhouette方式とその評価](https://jglobal.jst.go.jp/detail?JGLOBAL_ID=201902255241782790)
- [3] [実用的なささやき声の生成法:Phantom Silhouette方式の改良](https://jglobal.jst.go.jp/detail?JGLOBAL_ID=202002252470550660)
- [4] Teruhisa Uchida.  
  A practical method for generating whispers from singing voices: Application of improved phantom silhouette method.  
  2023 年 44 巻 3 号 p. 239-246.  
  [https://www.jstage.jst.go.jp/article/ast/44/3/44_E2249/_article/-char/ja/](https://www.jstage.jst.go.jp/article/ast/44/3/44_E2249/_article/-char/ja/)