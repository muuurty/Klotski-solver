# Klotski-solver - Flask + CV solver

This PR adds a Flask backend and a web UI to detect Klotski board pieces from an image and solve the puzzle using a BFS solver.

Running locally

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the server:

```bash
python app.py
```

3. Open http://localhost:5000 in your browser. Allow camera access to capture a snapshot, or upload an image of the Klotski board. Press "Detect Pieces", review/adjust pieces, then press "Solve".

Notes

- CV is a best-effort pipeline using OpenCV. It warps the detected board to a canonical 400x500 image, then detects piece contours and maps bounding boxes to grid cells.
- Solver is a straightforward BFS that returns a shortest-move solution. The server returns the path which the client animates.

Future improvements

- Improve detection robustness and add a calibration UI.
- Add drag-to-move piece editing and better collision hints.
- Add unit tests for the CV and solver components.
