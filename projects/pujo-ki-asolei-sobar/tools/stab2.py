"""Similarity stabiliser (translation + rotation + scale) without OpenCV.

estimate(smalls): per frame pair, subpixel phase correlation on a grid of textured patches -> displacement vectors
                  -> RANSAC similarity fit (rejects the moving subject) -> 3x3 inter-frame transforms -> camera path.
plan(path, ...):  smooth (gaussian per parameter) or lock; returns per-frame correction matrices (margin-res px).
warp(frame, C, out_hw, origin): applies a correction and crops the output window (bilinear).
measure(gray_frames): residual high-frequency shake: translation RMS (px), rotation RMS (deg), scale RMS (%).
"""
import numpy as np
from scipy import ndimage

def _pc(a, b, win):
    A = np.fft.fft2((a - a.mean()) * win); B = np.fft.fft2((b - b.mean()) * win)
    R = A * np.conj(B); R /= np.abs(R) + 1e-9; r = np.fft.ifft2(R).real
    py, px = np.unravel_index(np.argmax(r), r.shape); h, w = r.shape
    def sub(v0, v1, v2):
        den = v0 - 2 * v1 + v2; return 0.5 * (v0 - v2) / den if abs(den) > 1e-9 else 0.0
    dy = sub(r[(py - 1) % h, px], r[py, px], r[(py + 1) % h, px]); dx = sub(r[py, (px - 1) % w], r[py, px], r[py, (px + 1) % w])
    y = py + dy; x = px + dx
    if y > h / 2: y -= h
    if x > w / 2: x -= w
    return y, x, float(r.max())

def _grid(shape, ps=48, ny=7, nx=4, roi=None):
    H, W = shape; ys = np.linspace(ps, H - ps, ny).astype(int); xs = np.linspace(ps, W - ps, nx).astype(int)
    pts = [(y, x) for y in ys for x in xs]
    if roi: pts = [(y, x) for y, x in pts if roi[0] * H <= y <= roi[1] * H and roi[2] * W <= x <= roi[3] * W]
    return pts

def _fit_sim(P, Q, iters=200, thr=0.8, rng=np.random.default_rng(0)):
    """Q ~ s R P + t, P,Q (n,2) as (x,y). Returns 3x3 matrix, inlier mask."""
    n = len(P)
    if n < 3: return np.eye(3), np.ones(n, bool)
    def solve(p, q):
        A = np.zeros((2 * len(p), 4)); bb = np.zeros(2 * len(p))
        A[0::2] = np.c_[p[:, 0], -p[:, 1], np.ones(len(p)), np.zeros(len(p))]; A[1::2] = np.c_[p[:, 1], p[:, 0], np.zeros(len(p)), np.ones(len(p))]
        bb[0::2] = q[:, 0]; bb[1::2] = q[:, 1]
        a, b, tx, ty = np.linalg.lstsq(A, bb, rcond=None)[0]
        return np.array([[a, -b, tx], [b, a, ty], [0, 0, 1.0]])
    best, bestin = np.eye(3), np.zeros(n, bool)
    for _ in range(iters):
        idx = rng.choice(n, 2, replace=False)
        if np.linalg.norm(P[idx[0]] - P[idx[1]]) < 20: continue
        M = solve(P[idx], Q[idx]); pr = (M[:2, :2] @ P.T).T + M[:2, 2]
        inl = np.linalg.norm(pr - Q, axis=1) < thr
        if inl.sum() > bestin.sum(): best, bestin = M, inl
    if bestin.sum() >= 3: best = solve(P[bestin], Q[bestin])
    return best, bestin

def estimate(smalls, roi=None, ps=48):
    """smalls: list of 2D float arrays (same size). Returns list of 3x3 inter-frame transforms T_i (frame i-1 -> i)."""
    H, W = smalls[0].shape; win = np.outer(np.hanning(ps * 2), np.hanning(ps * 2))
    pts = _grid((H, W), ps, roi=roi)
    Ts = [np.eye(3)]
    for i in range(1, len(smalls)):
        a, b = smalls[i - 1], smalls[i]; P, Q = [], []
        for (y, x) in pts:
            pa = a[y - ps:y + ps, x - ps:x + ps]; pb = b[y - ps:y + ps, x - ps:x + ps]
            if pa.std() < 4: continue                                     # textureless patch
            dy, dx, peak = _pc(pb, pa, win)
            if peak < 0.08: continue
            P.append((x, y)); Q.append((x + dx, y + dy))
        M, _ = _fit_sim(np.array(P, float).reshape(-1, 2), np.array(Q, float).reshape(-1, 2)) if len(P) >= 3 else (np.eye(3), None)
        Ts.append(M)
    return Ts

def params(M):
    s = np.hypot(M[0, 0], M[1, 0]); return np.array([M[0, 2], M[1, 2], np.arctan2(M[1, 0], M[0, 0]), np.log(s)])

def from_params(p, cx, cy):
    """similarity about the frame centre: translation (tx,ty), angle, log-scale."""
    s = np.exp(p[3]); c, sn = np.cos(p[2]) * s, np.sin(p[2]) * s
    R = np.array([[c, -sn, 0], [sn, c, 0], [0, 0, 1.0]])
    Tc = np.array([[1, 0, cx], [0, 1, cy], [0, 0, 1.0]]); Ti = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1.0]])
    return np.array([[1, 0, p[0]], [0, 1, p[1]], [0, 0, 1.0]]) @ Tc @ R @ Ti

def plan(Ts, scale_up, cx, cy, sigma=16.0, lock=None):
    """Ts at small res; scale_up = full/small. Returns correction matrices (full margin-res) that map OUTPUT->INPUT coords."""
    # cumulative camera path as params about the centre (small res), then to full res
    A = np.eye(3); path = []
    Tc = np.array([[1, 0, cx / scale_up], [0, 1, cy / scale_up], [0, 0, 1.0]]); Ti = np.linalg.inv(Tc)
    for T in Ts:
        A = T @ A; C = Ti @ A @ Tc                                        # about the centre
        p = params(C); p[:2] *= scale_up; path.append(p)
    path = np.array(path); path[:, 2] = np.unwrap(path[:, 2])
    if lock is not None: smooth = np.tile(path[lock[0]:lock[1] + 1].mean(0), (len(path), 1))
    else: smooth = np.stack([ndimage.gaussian_filter1d(path[:, k], sigma, mode="nearest") for k in range(4)], 1)
    corr = []
    for p, q in zip(path, smooth):
        Mp = from_params(p, cx, cy); Mq = from_params(q, cx, cy)
        corr.append(Mp @ np.linalg.inv(Mq))      # output (smooth camera) -> input (actual camera)
    return corr, path, smooth

def warp(frame, C, out_hw, origin):
    """frame HxWx3 float; C maps output->input in margin coords; output window of out_hw at origin (y0,x0) of the margin frame."""
    Ho, Wo = out_hw; y0, x0 = origin
    yy, xx = np.mgrid[0:Ho, 0:Wo].astype(np.float32); xx += x0; yy += y0
    xi = C[0, 0] * xx + C[0, 1] * yy + C[0, 2]; yi = C[1, 0] * xx + C[1, 1] * yy + C[1, 2]
    return np.stack([ndimage.map_coordinates(frame[..., c], [yi, xi], order=1, mode="nearest") for c in range(frame.shape[2])], -1)

def measure(grays, roi=None):
    """residual high-frequency shake on a sequence of 2D frames (full-res units = frame width as given)."""
    Ts = estimate(grays, roi=roi, ps=min(48, grays[0].shape[1] // 8))
    H, W = grays[0].shape; corr, path, smooth = plan(Ts, 1.0, W / 2, H / 2, sigma=4.0)
    hf = path - smooth
    return {"trans_px": float(np.sqrt((hf[:, :2] ** 2).sum(1).mean())), "rot_deg": float(np.degrees(np.sqrt((hf[:, 2] ** 2).mean()))),
            "scale_pct": float(100 * np.sqrt((hf[:, 3] ** 2).mean()))}
