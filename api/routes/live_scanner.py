"""Authenticated live camera snapshots, with bounded inference concurrency."""

import os
import threading
from functools import lru_cache

from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from api.routes.verify import _read_bounded_upload, engine
from core.forensics.live_stream import LiveFrameAnalyzer, OnnxPreScreen
from core.security.image_sanitizer import ImageValidationError, sanitize_image_bytes

router = APIRouter(prefix="/api/v1/live", tags=["Live Camera"])
_capacity = threading.BoundedSemaphore(1)


@lru_cache(maxsize=1)
def get_analyzer():
    checkpoint = os.getenv("VERISLIP_LIVE_ONNX_MODEL")
    screen = OnnxPreScreen(checkpoint) if checkpoint else None
    return LiveFrameAnalyzer(engine, screen)


def _analyze(contents):
    if not _capacity.acquire(blocking=False):
        raise HTTPException(
            503,
            "Camera analysis is busy. Try again shortly.",
            headers={"Retry-After": "2"},
        )
    try:
        return get_analyzer().analyze(sanitize_image_bytes(contents))
    finally:
        _capacity.release()


@router.post("/verify")
async def verify_camera_frame(file: UploadFile = File(...)):
    contents = await _read_bounded_upload_safe(file)
    try:
        return await run_in_threadpool(_analyze, contents)
    except HTTPException:
        raise
    except ImageValidationError as exc:
        raise HTTPException(exc.status_code, exc.detail) from None
    except Exception:
        raise HTTPException(500, "Camera analysis could not be completed.") from None


async def _read_bounded_upload_safe(file):
    try:
        return await _read_bounded_upload(file)
    except ImageValidationError as exc:
        raise HTTPException(exc.status_code, exc.detail) from None
