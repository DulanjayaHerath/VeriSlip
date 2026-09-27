(function (root) {
  "use strict";

  class MotionGate {
    constructor(settleMs = 600, threshold = 18, fraction = 0.015) {
      this.settleMs = settleMs;
      this.threshold = threshold;
      this.fraction = fraction;
      this.anchor = null;
      this.generation = 0;
      this.consumed = false;
    }
    update(pixels, now) {
      let changed = 0;
      if (this.anchor) {
        for (let i = 0; i < pixels.length; i++) {
          if (Math.abs(pixels[i] - this.anchor[i]) > this.threshold) changed++;
        }
      }
      const moving = !this.anchor || changed / pixels.length >= this.fraction;
      if (moving) {
        this.anchor = pixels.slice();
        this.since = now;
        this.generation++;
        this.consumed = false;
      }
      return { moving, generation: this.generation,
        ready: !moving && !this.consumed && now - this.since >= this.settleMs };
    }
  }

  function createController(options) {
    const { video, overlay, status, metric, startButton, stopButton, rescanButton,
      request, mediaDevices, createCanvas, raf, cancelRaf } = options;
    const probe = createCanvas();
    probe.width = 80; probe.height = 60;
    const probeContext = probe.getContext("2d", { willReadFrequently: true });
    const gray = new Uint8Array(80 * 60);
    const capture = createCanvas();
    const drawing = overlay.getContext("2d");
    let stream = null, session = 0, animation = null, pending = null;
    let gate = new MotionGate(), lastTick = -Infinity, lastVideoTime = -1;
    let nextScanAt = 0, fpsStart = 0, frames = 0;

    function clearOverlay() { drawing.clearRect(0, 0, overlay.width, overlay.height); }

    function stop(message = "Camera stopped") {
      session++;
      if (animation !== null) cancelRaf(animation);
      animation = null;
      if (pending) pending.abort();
      pending = null;
      if (stream) stream.getTracks().forEach(track => track.stop());
      stream = null;
      video.srcObject = null;
      clearOverlay();
      startButton.disabled = false;
      stopButton.disabled = true;
      rescanButton.disabled = true;
      status.textContent = message;
      metric.textContent = "Camera off";
    }

    function drawRegions(result) {
      clearOverlay();
      const [width, height] = result.frame_size;
      if (!(width > 0 && height > 0)) return;
      const sx = overlay.width / width, sy = overlay.height / height;
      drawing.strokeStyle = "#fb7185";
      drawing.lineWidth = Math.max(2, overlay.width / 400);
      for (const region of result.flagged_regions || []) {
        const [x, y, w, h] = region.box;
        drawing.strokeRect(x * sx, y * sy, w * sx, h * sy);
      }
    }

    async function analyze(generation, token) {
      const controller = new AbortController();
      pending = controller;
      gate.consumed = true;
      status.textContent = "Analyzing the stationary document…";
      const timeout = setTimeout(() => controller.abort(), 30000);
      try {
        const scale = Math.min(1, 1920 / Math.max(video.videoWidth, video.videoHeight));
        capture.width = Math.round(video.videoWidth * scale);
        capture.height = Math.round(video.videoHeight * scale);
        capture.getContext("2d").drawImage(video, 0, 0, capture.width, capture.height);
        const blob = await new Promise(resolve => capture.toBlob(resolve, "image/jpeg", 0.92));
        if (token !== session || controller.signal.aborted) return;
        if (!blob) throw new Error("Could not capture the camera frame.");
        const form = new FormData();
        form.append("file", blob, "camera.jpg");
        const response = await request("/api/v1/live/verify", {
          method: "POST", body: form, signal: controller.signal
        });
        if (token !== session) return;
        if (!response.ok) {
          const retry = Number(response.headers.get("Retry-After"));
          nextScanAt = performance.now() + Math.max(2000, (Number.isFinite(retry) ? retry : 2) * 1000);
          if (response.status === 401 || response.status === 403) {
            stop("Access denied. Set your API key in Merchant History, then start again.");
            return;
          }
          throw new Error(response.status === 429 ? "Scan limit reached. Waiting before retrying." :
            "Analysis unavailable. Retrying shortly…");
        }
        const result = await response.json();
        if (token !== session || generation !== gate.generation) return;
        drawRegions(result);
        status.textContent = result.status === "verified" ?
          `${result.verdict.replaceAll("_", " ")} · ${result.tamper_risk_percentage}% risk. ${result.recommendation}` :
          "Pre-screen did not trigger a full check. This document is not verified.";
      } catch (error) {
        if (token === session && generation === gate.generation) {
          clearOverlay();
          status.textContent = controller.signal.aborted ? "Analysis timed out. Retrying shortly…" : error.message;
          gate.consumed = false;
          nextScanAt = Math.max(nextScanAt, performance.now() + 2000);
        }
      } finally {
        clearTimeout(timeout);
        if (pending === controller) pending = null;
      }
    }

    function tick(now) {
      if (!stream) return;
      animation = raf(tick);
      if (now - lastTick < 1000 / 30 || video.readyState < 2 || !video.videoWidth ||
          video.currentTime === lastVideoTime) return;
      lastTick = Number.isFinite(lastTick) ? now - ((now - lastTick) % (1000 / 30)) : now;
      lastVideoTime = video.currentTime;
      if (!fpsStart) fpsStart = now;
      frames++;
      if (now - fpsStart >= 1000) {
        metric.textContent = `${(frames * 1000 / (now - fpsStart)).toFixed(1)} sampled FPS · target 30`;
        frames = 0; fpsStart = now;
      }
      if (overlay.width !== video.videoWidth || overlay.height !== video.videoHeight) {
        overlay.width = video.videoWidth; overlay.height = video.videoHeight;
        gate.anchor = null;
        gate.generation++;
        gate.consumed = false;
      }
      probeContext.drawImage(video, 0, 0, 80, 60);
      const pixels = probeContext.getImageData(0, 0, 80, 60).data;
      for (let i = 0; i < gray.length; i++) {
        gray[i] = Math.round(0.299 * pixels[i * 4] + 0.587 * pixels[i * 4 + 1] + 0.114 * pixels[i * 4 + 2]);
      }
      const motion = gate.update(gray, now);
      if (motion.moving) {
        clearOverlay();
        status.textContent = "Hold the document still…";
      }
      if (motion.ready && !pending && now >= nextScanAt) analyze(motion.generation, session);
    }

    async function start() {
      stop();
      const token = session;
      startButton.disabled = true;
      stopButton.disabled = false;
      status.textContent = "Waiting for camera permission…";
      try {
        if (!mediaDevices || !mediaDevices.getUserMedia) throw new Error("Camera access requires HTTPS or localhost.");
        const acquired = await mediaDevices.getUserMedia({ audio: false, video: {
          facingMode: { ideal: "environment" }, width: { ideal: 1280 }, height: { ideal: 720 },
          frameRate: { ideal: 30, max: 30 }
        } });
        if (token !== session) { acquired.getTracks().forEach(track => track.stop()); return; }
        stream = acquired;
        stream.getTracks().forEach(track => track.addEventListener("ended", () => {
          if (token === session) stop("Camera disconnected. Start again to reconnect.");
        }));
        video.srcObject = stream;
        await video.play();
        if (token !== session) return;
        gate = new MotionGate();
        lastTick = -Infinity; lastVideoTime = -1; nextScanAt = 0; frames = 0; fpsStart = 0;
        rescanButton.disabled = false;
        status.textContent = "Hold the document still…";
        animation = raf(tick);
      } catch (error) {
        if (token === session) stop(error.name === "NotAllowedError" ?
          "Camera permission denied. Allow access in your browser, then start again." : error.message);
      }
    }

    function rescan() {
      gate.anchor = null;
      gate.consumed = false;
      gate.generation++;
      clearOverlay();
      status.textContent = "Hold the document still for another scan…";
    }
    return { start, stop, rescan };
  }

  function mount(request) {
    const byId = id => document.getElementById(id);
    const controller = createController({
      video: byId("live-video"), overlay: byId("live-overlay"), status: byId("live-status"),
      metric: byId("live-fps"), startButton: byId("live-start"), stopButton: byId("live-stop"),
      rescanButton: byId("live-rescan"), request, mediaDevices: navigator.mediaDevices,
      createCanvas: () => document.createElement("canvas"),
      raf: callback => requestAnimationFrame(callback), cancelRaf: id => cancelAnimationFrame(id)
    });
    byId("live-start").addEventListener("click", controller.start);
    byId("live-stop").addEventListener("click", () => controller.stop());
    byId("live-rescan").addEventListener("click", controller.rescan);
    window.addEventListener("pagehide", () => controller.stop());
    document.addEventListener("visibilitychange", () => { if (document.hidden) controller.stop(); });
    return controller;
  }
  const api = { MotionGate, createController, mount };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.VeriSlipLiveScanner = api;
})(typeof window !== "undefined" ? window : globalThis);
