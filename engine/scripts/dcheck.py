"""Final /d/ release audibility for a word: vowel peak, closure, release burst level (full band and 2-8 kHz),
and the length of any vocalic tail after the burst ('duh'). Times in seconds; levels in dB (10 ms RMS; 5 ms for burst).
import as module: measure(x, sr, w_start, w_end_limit) -> dict"""
import numpy as np
from scipy.signal import butter, sosfiltfilt
def _db(x):
    return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
def measure(x, sr, t0, t1):
    hf = sosfiltfilt(butter(4, [2000, 8000], "bandpass", fs=sr, output="sos"), x)
    h = int(0.005 * sr)
    ts = np.arange(t0, t1, 0.005)
    full = np.array([_db(x[int(t * sr):int(t * sr) + h]) for t in ts])
    hfe = np.array([_db(hf[int(t * sr):int(t * sr) + h]) for t in ts])
    # vowel = loudest stretch of the word; vowel end = last frame within 15 dB of the peak before the first deep dip
    pk = full.max(); ipk = int(full.argmax())
    ve = ipk
    while ve + 1 < len(full) and full[ve + 1] > pk - 15:
        ve += 1
    # closure: following frames; release: loudest HF frame 15-150 ms after the vowel end
    a, b = ve + 3, min(ve + 30, len(full))
    if a >= b:
        return None
    ir = a + int(hfe[a:b].argmax())
    closure = full[ve + 1:ir].min() if ir > ve + 1 else full[ve + 1]
    # vocalic tail after the burst: frames after the release within 25 dB of the vowel peak
    k = ir + 1; tail = 0
    while k < len(full) and full[k] > pk - 25:
        tail += 1; k += 1
    return dict(vowel_peak=round(pk, 1), vowel_end=round(ts[ve], 3), closure=round(closure, 1),
                rel_t=round(ts[ir], 3), rel_ms=int(round((ts[ir] - ts[ve]) * 1000)),
                rel_full=round(full[ir], 1), rel_full_vs_vowel=round(full[ir] - pk, 1),
                rel_hf=round(hfe[ir], 1), vowel_hf=round(np.median(hfe[max(0, ipk - 10):ve + 1]), 1),
                tail_ms=tail * 5)
