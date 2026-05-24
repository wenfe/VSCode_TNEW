"""
make_movie.py
Creates stabilised animated GIF + MP4 for two TEM image sequences:
  • W  sequence : 0_W.png,  2_W.png  … 18_W.png
  • WO sequence : 0s_WO.png, 2s_WO.png … 20s_WO.png
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import numpy as np
from scipy.ndimage import shift as nd_shift

FOLDER = os.path.dirname(os.path.abspath(__file__))

# ── sequences to process ─────────────────────────────────────────────────────
SEQUENCES = [
    {
        "name"   : "W",
        "steps"  : list(range(0, 19, 2)),          # 0,2,4…18
        "pattern": lambda t: f"{t}_W.png",
        "label"  : lambda t: f"{t} s",
        "gif1"   : "TEM_sequence_W.gif",
        "gif2"   : "TEM_sequence_W_mpl.gif",
        "mp4"    : "TEM_sequence_W.mp4",
    },
    {
        "name"   : "WO",
        "steps"  : list(range(0, 21, 2)),          # 0,2,4…20
        "pattern": lambda t: f"{t}s_WO.png",
        "label"  : lambda t: f"{t} s",
        "gif1"   : "TEM_sequence_WO.gif",
        "gif2"   : "TEM_sequence_WO_mpl.gif",
        "mp4"    : "TEM_sequence_WO.mp4",
    },
]

# ── stabilisation helpers ────────────────────────────────────────────────────
def phase_align(ref_gray, img_gray, max_shift=40):
    h, w = ref_gray.shape
    ch, cw = int(h * 0.6), int(w * 0.6)
    y0, x0 = (h - ch) // 2, (w - cw) // 2
    r = ref_gray[y0:y0+ch, x0:x0+cw].astype(float)
    g = img_gray[y0:y0+ch, x0:x0+cw].astype(float)
    win = np.outer(np.hanning(ch), np.hanning(cw))
    r *= win;  g *= win
    R = np.fft.fft2(r);  I = np.fft.fft2(g)
    cross = R * np.conj(I)
    cross /= (np.abs(cross) + 1e-10)
    cc = np.abs(np.fft.ifft2(cross))
    cc_roll = np.fft.fftshift(cc)
    cy, cx = ch // 2, cw // 2
    search = cc_roll[cy-max_shift:cy+max_shift+1,
                     cx-max_shift:cx+max_shift+1]
    idx = np.unravel_index(np.argmax(search), search.shape)
    return float(idx[0] - max_shift), float(idx[1] - max_shift)

def align_sequence(images):
    min_h = min(im.shape[0] for im in images)
    min_w = min(im.shape[1] for im in images)
    images = [im[:min_h, :min_w] for im in images]
    ref = np.mean(images[0], axis=2).astype(float)
    aligned = [images[0]]
    for i, img in enumerate(images[1:], 1):
        gray = np.mean(img, axis=2).astype(float)
        dy, dx = phase_align(ref, gray)
        print(f"  frame {i}: shift = ({dy:+.1f}, {dx:+.1f}) px")
        corrected = np.stack(
            [nd_shift(img[:, :, c], (dy, dx), mode="nearest") for c in range(3)],
            axis=2
        ).clip(0, 255).astype(np.uint8)
        aligned.append(corrected)
    return aligned

# ── GIF / MP4 writers ────────────────────────────────────────────────────────
def save_gif_pil(imgs, path, duration_ms=600):
    pil = [Image.fromarray(im) for im in imgs]
    dur = [duration_ms] * len(pil);  dur[-1] *= 3
    pil[0].save(path, save_all=True, append_images=pil[1:],
                loop=0, duration=dur, optimize=False)
    print(f"  GIF  → {os.path.basename(path)}")

def save_gif_mpl(imgs, labels, path, fps=1.5):
    fig, ax = plt.subplots(figsize=(5, 5), dpi=150)
    fig.patch.set_facecolor("black");  ax.axis("off")
    im_obj = ax.imshow(imgs[0], animated=True)
    ttl    = ax.set_title(labels[0], color="white", fontsize=16,
                          fontweight="bold", loc="right", pad=8)
    def update(i):
        im_obj.set_data(imgs[i]);  ttl.set_text(labels[i])
        return im_obj, ttl
    ani = animation.FuncAnimation(fig, update, frames=len(imgs),
                                  interval=int(1000/fps), blit=True, repeat=True)
    ani.save(path, writer="pillow", fps=fps, dpi=150)
    plt.close(fig)
    print(f"  GIF  → {os.path.basename(path)}")

def save_mp4(imgs, labels, path, fps=2):
    fig, ax = plt.subplots(figsize=(5, 5), dpi=150)
    fig.patch.set_facecolor("black");  ax.axis("off")
    im_obj = ax.imshow(imgs[0], animated=True)
    ttl    = ax.set_title(labels[0], color="white", fontsize=16,
                          fontweight="bold", loc="right", pad=8)
    def update(i):
        im_obj.set_data(imgs[i]);  ttl.set_text(labels[i])
        return im_obj, ttl
    ani = animation.FuncAnimation(fig, update, frames=len(imgs),
                                  interval=int(1000/fps), blit=True, repeat=True)
    try:
        Writer = animation.FFMpegWriter(fps=fps, bitrate=2000,
                                        extra_args=["-vcodec","libx264",
                                                    "-pix_fmt","yuv420p"])
        ani.save(path, writer=Writer, dpi=150)
        print(f"  MP4  → {os.path.basename(path)}")
    except Exception as e:
        print(f"  MP4 skipped (ffmpeg not found): {e}")
    plt.close(fig)

# ── main loop ────────────────────────────────────────────────────────────────
for seq in SEQUENCES:
    print(f"\n=== Processing sequence: {seq['name']} ===")
    fpaths = [os.path.join(FOLDER, seq["pattern"](t)) for t in seq["steps"]]
    fpaths = [f for f in fpaths if os.path.exists(f)]
    if not fpaths:
        print("  No files found, skipping."); continue
    steps_found = [seq["steps"][i] for i, f in
                   enumerate([os.path.join(FOLDER, seq["pattern"](t))
                               for t in seq["steps"]]) if os.path.exists(f)]
    labels = [seq["label"](t) for t in steps_found]
    imgs_raw = [np.array(Image.open(f).convert("RGB")) for f in fpaths]
    print(f"  Aligning {len(imgs_raw)} frames …")
    imgs = align_sequence(imgs_raw)
    save_gif_pil(imgs, os.path.join(FOLDER, seq["gif1"]))
    save_gif_mpl(imgs, labels, os.path.join(FOLDER, seq["gif2"]))
    save_mp4    (imgs, labels, os.path.join(FOLDER, seq["mp4"]))

print("\nDone.")

