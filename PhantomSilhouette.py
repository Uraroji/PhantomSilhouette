import numpy as np
from skimage.transform import PiecewiseAffineTransform, warp
from scipy import interpolate

def spec_warp(sp, curve, sr):
    image = sp.T
    rows, cols = image.shape[0], image.shape[1]
    src_cols = np.linspace(0, cols, 20)
    src_rows = np.linspace(0, rows, 30)
    src_rows, src_cols = np.meshgrid(src_rows, src_cols)
    src = np.dstack([src_cols.flat, src_rows.flat])[0]
    dst_rows = curve(src[:, 1], sr)
    dst_cols = src[:, 0]
    dst1 = np.vstack([dst_cols, dst_rows]).T
    tform = PiecewiseAffineTransform()
    tform.estimate(src, dst1)
    out_rows = image.shape[0]
    out_cols = image.shape[1]
    out1 = warp(image, tform, output_shape=(out_rows, out_cols))
    sp_out = out1.T.copy()
    return sp_out

def curve(x, sr):
    f = interpolate.interp1d([0, (1100/(sr//2))*513,  (1600/(sr//2))*513, 513], [0, (1000/(sr//2))*513,  (1600/(sr//2))*513, 513], kind='linear')
    return f(x)

def low_frequency_suppression(x, sr):
    idxs = np.arange(1, 513+1) * (sr//2/513)
    w = lambda f: np.where(f>1350, 1, np.where(f>550, np.abs((f-550)/(1350-550))**np.e, 0))
    idxs = np.tile(idxs, (x.shape[0], 1))
    return x * w(idxs)

def high_frequency_emphasis(x, sr):
    idxs = np.arange(1, 513+1) * (sr//2/513)
    w = lambda f: np.where(f<10e+2, 1, np.where(f<10e+3, (1/(10e+3-10e+2))*(f-10e+3-10e+2)+2.1111, 2))
    idxs = np.tile(idxs, (x.shape[0], 1))
    return x * w(idxs)

def phantom_silhouette(f0, sp, sr):
    sp_out = spec_warp(sp, curve, sr)
    sp_out = low_frequency_suppression(sp_out, sr)
    sp_out = high_frequency_emphasis(sp_out, sr)
    sp_out[sp_out==0] = 0.00000001
    f0_out = np.random.random(f0.shape[0])
    return f0_out, sp_out