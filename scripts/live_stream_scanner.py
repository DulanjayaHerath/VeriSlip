#!/usr/bin/env python3
"""Live document-camera preview; press Q to stop. See docs/LIVE_SCANNER.md."""

import argparse
import json
import sys
import threading
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import cv2

# Allow execution as a script from outside the repository's working directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.forensics.live_stream import (  # noqa: E402
    LatestFrameBuffer,
    LiveFrameAnalyzer,
    MotionGate,
    OnnxPreScreen,
)
from core.forensics.unified_scorer import VeriSlipForensicEngine  # noqa: E402

_analyzer = None


def _initialize_inference(model_path):
    global _analyzer
    cv2.setNumThreads(1)
    screen = OnnxPreScreen(model_path) if model_path else None
    _analyzer = LiveFrameAnalyzer(VeriSlipForensicEngine(), screen)


def _infer(frame):
    return _analyzer.analyze_bgr(frame)


def _worker_ready():
    return True


class CameraCapture:
    """Capture runs independently of preview/inference and owns VideoCapture."""

    def __init__(self, source, fps=30):
        self.source = source
        self.fps = fps
        self.frames = LatestFrameBuffer()
        self.stop_event = threading.Event()
        self.done = threading.Event()
        self.error = None
        self.thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        camera = None
        try:
            camera = cv2.VideoCapture(self.source)
            if not camera.isOpened():
                raise RuntimeError("Could not open the camera or video source")
            camera.set(cv2.CAP_PROP_FPS, self.fps)
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            period = 1 / self.fps
            while not self.stop_event.is_set():
                started = time.monotonic()
                ok, frame = camera.read()
                if not ok:
                    break
                self.frames.publish(frame)
                # Event.wait uses a coarse Windows timer; sleep uses Python's
                # high-resolution waitable timer and keeps a 30 FPS cadence.
                time.sleep(max(0, period - (time.monotonic() - started)))
        except Exception as exc:
            self.error = str(exc)
        finally:
            if camera is not None:
                camera.release()
            self.done.set()

    def start(self):
        self.thread.start()
        return self

    def close(self):
        self.stop_event.set()
        self.thread.join(timeout=2)


def draw_result(frame, result):
    if not result:
        return
    width, height = result["frame_size"]
    sx, sy = frame.shape[1] / width, frame.shape[0] / height
    for region in result["flagged_regions"]:
        x, y, w, h = region["box"]
        cv2.rectangle(
            frame,
            (int(x * sx), int(y * sy)),
            (int((x + w) * sx), int((y + h) * sy)),
            (40, 60, 240),
            2,
        )


def run(args):
    # Keep OpenCV's thread pool from oversubscribing a small camera workstation.
    cv2.setNumThreads(1)
    gate = MotionGate(settle_seconds=args.settle_seconds)
    source = int(args.source) if args.source.isdecimal() else args.source
    worker = ProcessPoolExecutor(
        max_workers=1, initializer=_initialize_inference, initargs=(args.onnx_model,)
    )
    try:
        worker.submit(_worker_ready).result()
    except BaseException:
        worker.shutdown(wait=True, cancel_futures=True)
        raise
    capture = CameraCapture(source, args.fps).start()
    future = None
    submitted_generation = None
    result = None
    frames = scans = 0
    sequence = 0
    started = time.monotonic()
    status = "Hold the document still"
    try:
        while not args.duration or time.monotonic() - started < args.duration:
            tick = time.monotonic()
            snapshot = capture.frames.snapshot(sequence)
            if snapshot is None:
                if capture.done.is_set():
                    break
                time.sleep(0.002)
                continue
            sequence, frame = snapshot
            frames += 1
            motion = gate.update(frame, tick)
            if motion.moving:
                result = None
                status = "Hold the document still"
            if future is not None and future.done():
                try:
                    completed = future.result()
                    if submitted_generation == motion.generation:
                        result = completed
                        status = completed["verdict"] or "Pre-screen only; not verified"
                        print(json.dumps(completed), flush=True)
                except Exception:
                    status = "Analysis failed; move the document to retry"
                future = None
            if motion.ready and future is None:
                future = worker.submit(_infer, frame.copy())
                submitted_generation = motion.generation
                gate.mark_submitted()
                scans += 1
                status = "Analyzing stable document"
            if not args.headless:
                draw_result(frame, result)
                fps = frames / max(time.monotonic() - started, 0.001)
                cv2.putText(
                    frame,
                    f"{fps:.1f} FPS | {status}",
                    (12, 28),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 220, 220),
                    2,
                )
                cv2.imshow("VeriSlip Live Camera", frame)
                if cv2.waitKey(1) & 0xFF in (ord("q"), 27):
                    break
            time.sleep(max(0, 1 / args.fps - (time.monotonic() - tick)))
    finally:
        elapsed = time.monotonic() - started
        capture.close()
        worker.shutdown(wait=True, cancel_futures=True)
        if not args.headless:
            cv2.destroyAllWindows()
    print(
        json.dumps(
            {
                "preview_frames": frames,
                "elapsed_seconds": elapsed,
                "preview_fps": frames / max(elapsed, 0.001),
                "captured_frames": capture.frames.sequence,
                "scans_submitted": scans,
                "buffer_allocations": capture.frames.allocations,
            }
        )
    )
    if capture.error:
        raise RuntimeError(capture.error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source", default="0", help="Camera index or local video path"
    )
    parser.add_argument(
        "--fps", type=int, default=30, choices=range(1, 61), metavar="1-60"
    )
    parser.add_argument("--settle-seconds", type=float, default=0.6)
    parser.add_argument(
        "--duration", type=float, default=0, help="Stop after N seconds; 0 is unlimited"
    )
    parser.add_argument("--onnx-model", help="Trained 320x320 RGB probability CNN")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="No native window; output results and FPS",
    )
    args = parser.parse_args()
    if args.duration < 0:
        parser.error("duration must be nonnegative")
    run(args)


if __name__ == "__main__":
    main()
