# VSCode_T Utilities

This workspace contains two small Python utilities:

- `Imagel.py`: thermal model of a spherical microparticle under beam heating with radiative cooling.
- `Retrieval.py`: extract frames from a video and save cropped images.

## Requirements

Install dependencies (preferably in a virtual environment):

```
numpy
scipy
matplotlib
opencv-python
```

You can also install from `requirements.txt`.

## Usage

Imagel (defaults match the original script):

```bash
python Imagel.py --t-end 0.005 --t-steps 500 --output heat_20241127.jpg --xlim 0.0005
```

Retrieval (defaults match the original script):

```bash
python Retrieval.py --video 300kV_50nA.mp4 --outdir data_300kV_50nA --x 564 --y 200 --w 638 --h 578
```

Optional flags for Retrieval:
- `--start`: start frame index (default 0)
- `--max-frames`: limit number of frames to write (-1 for all)

## Notes

- ROI in `Retrieval.py` is clipped to the frame bounds to avoid errors.
- `Imagel.py` implements a forward-Euler integrator; adjust parameters as needed.
