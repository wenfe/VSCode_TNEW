"""
Extract frames from a video file and save cropped images to a target folder.

Improvement: Crop the region of interest (ROI) directly from the in-memory frame
and save once, avoiding an unnecessary write+read cycle.

Adjust the ROI (x, y, w, h) as needed for your video content.
"""

from typing import Tuple
import argparse
import cv2  # OpenCV for video I/O and image processing
import os


def ensure_dir(path: str) -> None:
    """Create directory if it doesn't exist."""
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f'Error: Creating directory {path}')


def crop_roi(frame, x: int, y: int, w: int, h: int):
    """Return cropped region; if ROI exceeds bounds, it will be clipped to the frame."""
    H, W = frame.shape[:2]
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    return frame[y0:y1, x0:x1]


def extract_frames(
    video_path: str = "300kV_50nA.mp4",
    out_dir: str = "data_300kV_50nA",
    roi: Tuple[int, int, int, int] = (564, 200, 638, 578),
    start_frame: int = 0,
    max_frames: int = -1,
) -> int:
    """
    Extract frames from a video, crop a ROI, and save as PNGs.

    Returns the number of frames written.
    """
    cam = cv2.VideoCapture(video_path)
    ensure_dir(out_dir)

    x, y, w, h = roi
    currentframe = 0
    written = 0

    # Fast-forward to start_frame if requested
    if start_frame > 0:
        cam.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        currentframe = start_frame

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        # Crop directly from in-memory frame
        crop = crop_roi(frame, x, y, w, h)

        name = os.path.join(out_dir, f"frame{currentframe}.png")
        print(f"Creating... {name}")
        cv2.imwrite(name, crop)

        currentframe += 1
        written += 1

        if max_frames > 0 and written >= max_frames:
            break

    cam.release()
    cv2.destroyAllWindows()
    return written


def main():
    parser = argparse.ArgumentParser(description="Extract and crop frames from a video")
    parser.add_argument("--video", type=str, default="300kV_50nA.mp4", help="Input video path")
    parser.add_argument("--outdir", type=str, default="data_300kV_50nA", help="Output directory")
    parser.add_argument("--x", type=int, default=564, help="ROI top-left x")
    parser.add_argument("--y", type=int, default=200, help="ROI top-left y")
    parser.add_argument("--w", type=int, default=638, help="ROI width")
    parser.add_argument("--h", type=int, default=578, help="ROI height")
    parser.add_argument("--start", type=int, default=0, help="Start from this frame index")
    parser.add_argument("--max-frames", type=int, default=-1, help="Maximum frames to write (-1 for all)")
    args = parser.parse_args()

    n = extract_frames(
        video_path=args.video,
        out_dir=args.outdir,
        roi=(args.x, args.y, args.w, args.h),
        start_frame=args.start,
        max_frames=args.max_frames,
    )
    print(f"Done. Wrote {n} frames to {args.outdir}")


if __name__ == "__main__":
    main()