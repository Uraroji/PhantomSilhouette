import numpy as np
from skimage.transform import PiecewiseAffineTransform, warp
from scipy import interpolate

def hz_to_spec(hz: int, sr: int, spec_sample: int) -> float:
    """
    実際の周波数をスペクトログラム(スペクトル包絡)中の座標に変換する

    Parameters
    ----------
    hz: int
        実際の周波数
    sr: int
        音源のサンプルレート
    spec_sample: int
        スペクトル包絡の周波数方向の配列長
    
    Returns
    -------
    spec_coordinate: float
        スペクトル包絡中の座標
    """
    return (hz/(sr//2))*spec_sample

def formant_shift(sp: np.ndarray, sr: int, time_skip: int = 10) -> np.ndarray:
    """
    F1・F2フォルマントの上方シフト
    区分的アフィン変換を用いて、スペクトル包絡のF1,F2の区間を上方へシフト

    Parameters
    ----------
    sp: np.ndarray
        スペクトル包絡
    sr: int
        サンプルレート
    time_skip: int
        区間的アフィン変換に用いる時間方向のメッシュの幅(default: 10)
    
    Returns
    -------
    sp_out: np.ndarray
        F1・F2フォルマントを上方シフトしたスペクトル包絡
    """
    from_list = []
    to_list = []
    for i in range(0, sp.shape[0], time_skip):
        from_list += [[0, i], [hz_to_spec(1000, sr, sp.shape[1]), i], [hz_to_spec(1600, sr, sp.shape[1]), i], [sp.shape[1], i]]
        to_list += [[0, i], [hz_to_spec(1100, sr, sp.shape[1]), i], [hz_to_spec(1600, sr, sp.shape[1]), i], [sp.shape[1], i]]
    from_list = np.array(from_list)
    to_list = np.array(to_list)
    tform = PiecewiseAffineTransform()
    tform.estimate(from_list, to_list)
    return warp(sp, tform, output_shape=sp.shape)

def low_frequency_suppression(sp: np.ndarray, sr: int) -> np.ndarray:
    """
    低域スペクトルの抑圧
    低域スペクトルの周波数レベルを抑制する

    Parameters
    ----------
    sp: np.ndarray
        スペクトル包絡
    sr: int
        サンプルレート
    
    Returns
    -------
    sp_out: np.ndarray
        低域スペクトルを抑圧したスペクトル包絡
    """
    idxs = np.arange(1, sp.shape[1]+1) * (sr//2/sp.shape[1])
    w = lambda f: np.where(f>1350, 1, np.where(f>550, np.abs((f-550)/(1350-550))**np.e, 0))
    idxs = np.tile(idxs, (sp.shape[0], 1))
    return sp * w(idxs)

def high_frequency_emphasis(sp: np.ndarray, sr: int) -> np.ndarray:
    """
    高域の気息成分の強調
    高域スペクトルの周波数レベルを強調する

    Parameters
    ----------
    sp: np.ndarray
        スペクトル包絡
    sr: int
        サンプルレート
    
    Returns
    -------
    sp_out: np.ndarray
        高域の気息成分を強調したスペクトル包絡
    """
    idxs = np.arange(1, sp.shape[1]+1) * (sr//2/sp.shape[1])
    w = lambda f: np.where(f<10e+2, 1, np.where(f<10e+3, (1/(10e+3-10e+2))*(f-10e+3-10e+2)+2.1111, 2))
    idxs = np.tile(idxs, (sp.shape[0], 1))
    return sp * w(idxs)

def convert_noise(f0: np.ndarray) -> np.ndarray:
    """
    声帯音源信号の代わりに白色雑音で駆動する音声に変換する

    Parameters
    ----------
    f0: np.ndarray
        声帯音源信号
    
    Returns
    -------
    f0_out: np.ndarray
        白色雑音
    """
    return np.random.random(f0.shape[0])

def phantom_silhouette(f0: np.ndarray, sp: np.ndarray, sr: int) -> (np.ndarray, np.ndarray):
    """
    PhantomSilhouette方式で変換

    Parameters
    ----------
    f0: np.ndarray
        声帯音源信号
    sp: np.ndarray
        スペクトル包絡
    sr: int
        サンプルレート
    
    Returns
    -------
    f0_out: np.ndarray
        白色雑音
    sp_out: np.ndarray
        囁き声に変換したスペクトル包絡
    """
    f0_out = convert_noise(f0)
    sp_out = formant_shift(sp, sr)
    sp_out = low_frequency_suppression(sp_out, sr)
    sp_out = high_frequency_emphasis(sp_out, sr)
    sp_out[sp_out==0] = 1e-8
    return f0_out, sp_out