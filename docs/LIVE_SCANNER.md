# Live document camera scanner (#128)

The Live Camera tab and standalone scanner keep camera preview independent of
forensic inference. They request a 30 FPS feed, keep only the newest frame, and
scan once after a scene has been stationary for 600 ms. Moving the document
clears old overlays and invalidates an in-flight result. A stationary document
does not cause repeated uploads; use **Scan again** to explicitly repeat a check.

## Browser

Start the existing API server and open its cockpit on HTTPS or localhost. Select
**Live Camera**, then **Start camera** and allow camera access. No microphone is
requested. The browser uses the WebRTC media-capture API (`getUserMedia`); preview
stays local. Stationary JPEG snapshots (longest side capped at 1920 pixels) go to
`POST /api/v1/live/verify` using the cockpit's existing API key.

The camera stops on Stop, tab navigation, page hide, browser backgrounding, or
device disconnection. Only one request is in flight per client; the server
permits one live inference per process and returns 503 with Retry-After when
busy. Existing authentication, rate limits, upload-byte limits, image sanitizing,
and request tracing apply. Frames are processed in memory and not saved by the
live endpoint. Full results include `frame_size` so boxes map to preview pixels.

The browser shows permission, authentication, timeout and retry states. Requests
time out after 30 seconds. Stopping or moving cannot apply a late result to a new
scene. The server may finish an already-running inference after a client aborts.

## Standalone

Use the project's Python environment:

```bash
python scripts/live_stream_scanner.py --source 0
python scripts/live_stream_scanner.py --source 0 --headless --duration 30
python scripts/live_stream_scanner.py --source path/to/test-video.mp4 --headless
```

`--source` accepts a camera index or local video path; `--fps` defaults to 30.
`--settle-seconds` controls the quiet interval. The standalone tool prints a
compact result for each accepted scene and a final JSON summary of preview FPS,
frame count, scan count, and buffer allocations. Press Q or Escape to stop the
native preview. A single capture thread owns and releases the device, a reusable
buffer drops superseded frames, and one inference process handles stable snapshots
without competing for the preview process's Python interpreter lock. FPS excludes
the final wait for an already-running inference to shut down.

The normal server dependency is `opencv-python-headless`, which has no native
window support. Use `--headless` or the browser with that installation. For a
native window, use a separate environment with `opencv-python` in place of
`opencv-python-headless`; do not install both packages together.

## Optional trained fast path

No trained lightweight pre-screen checkpoint is included. By default, every
stable scene gets full forensic analysis. There is **no randomly initialized CNN
making skip decisions**.

To enable a separately trained ONNX CNN:

```bash
python scripts/live_stream_scanner.py --source 0 --onnx-model weights/live_prescreen.onnx
```

For the API, set `VERISLIP_LIVE_ONNX_MODEL` before starting the server. The model
contract is RGB float32 NCHW `[1,3,320,320]`, values in `[0,1]`, with one finite
tamper probability in `[0,1]` as output. A score of at least 0.35 triggers full
analysis. Lower scores return `prescreen_only`, never an AUTHENTIC verdict or a
full-verification claim. An invalid configured model fails the request instead
of silently returning a reassuring result. `prescreen_ms` and `analysis_ms`
measure actual elapsed inference time.

## Performance and calibration limits

30 FPS is a capture/preview target, **not 30 full forensic scans per second**.
Frame dropping prevents slow analysis from building a queue. Actual throughput
depends on camera/driver, browser, image size and CPU/GPU. The issue's consistent
30 FPS and sub-12 ms CNN goals need a representative hardware benchmark and a
trained checkpoint; they are not asserted by the unit tests.

A local Windows/Python 3.14 smoke run using a generated 1280x720 MJPEG video
captured 90 frames and processed 89 preview frames in 3.006 seconds (29.6 FPS),
while one full forensic scan took 1.659 seconds. The capture buffer allocated once.
This short prerecorded-video check demonstrates scheduling isolation; it is not
a physical-camera benchmark or a validation of model accuracy.

Motion thresholds use 80x60 luminance samples: intensity difference greater than
18 in at least 1.5% of pixels resets the quiet timer. Comparisons use a fixed
scene anchor to catch accumulated slow movement. Browser luminance is sampled
directly; the OpenCV path also smooths it with a 3x3 Gaussian filter. This is not
a calibrated 2 mm displacement measurement. Camera distance, perspective,
illumination and document size must be calibrated for any physical-unit claim.

Live image forensics assesses visual anomalies, not whether a bank payment
settled. The existing model's accuracy on real camera images still requires
validation, especially for glare, blur, thermal paper and screen recaptures.

## Validation

```bash
python -m pytest tests/test_live_scanner.py -q
node --test tests/frontend/live_scanner.test.cjs
python -m pytest tests/ -q
```

Tests cover quiet intervals, cumulative motion, single-scene triggering, bounded
frame storage, detached snapshots, camera cleanup, CNN input/output contracts,
authentication, upload limits, worker capacity, late permissions, aborted
requests, stale overlays and one-request-at-a-time behavior. Before deployment,
run a 30-second camera trial, record the reported FPS and inference timings,
move/replace a slip during analysis, disconnect the device, and confirm overlays
align at the camera's chosen resolution.
