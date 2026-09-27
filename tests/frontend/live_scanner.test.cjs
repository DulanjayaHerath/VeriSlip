const { test } = require("node:test");
const assert = require("node:assert/strict");
const { MotionGate, createController } = require("../../web/js/live_scanner.js");

test("motion settles once and anchor catches slow drift", () => {
  const gate = new MotionGate();
  const frame = new Uint8Array(100).fill(100);
  assert.equal(gate.update(frame, 0).moving, true);
  assert.equal(gate.update(frame, 599).ready, false);
  assert.equal(gate.update(frame, 601).ready, true);
  gate.consumed = true;
  assert.equal(gate.update(frame, 700).ready, false);
  assert.equal(gate.update(frame.map(x => x + 10), 800).moving, false);
  assert.equal(gate.update(frame.map(x => x + 20), 900).moving, true);
  assert.equal(gate.update(frame.map(x => x + 20), 1501).ready, true);
});

function harness(getUserMedia, request = async () => { throw Error("unexpected request"); }) {
  let callback, stopped = 0, drawn = 0, pixels = 100;
  const track = { stop() { stopped++; }, addEventListener() {} };
  const stream = { getTracks: () => [track] };
  const context = { clearRect() {}, drawImage() {}, strokeRect() { drawn++; },
    getImageData: () => ({ data: new Uint8Array(80 * 60 * 4).fill(pixels) }) };
  const canvas = () => ({ width: 1280, height: 720, getContext: () => context,
    toBlob: cb => cb(new Blob(["frame"], { type: "image/jpeg" })) });
  const video = { videoWidth: 1280, videoHeight: 720, readyState: 2, currentTime: 0,
    play: async () => {}, srcObject: null };
  const status = {}, metric = {}, startButton = {}, stopButton = {}, rescanButton = {};
  const controller = createController({ video, overlay: canvas(), status, metric,
    startButton, stopButton, rescanButton, request,
    mediaDevices: { getUserMedia: getUserMedia || (async () => stream) },
    createCanvas: canvas, raf: cb => { callback = cb; return 1; }, cancelRaf() { callback = null; } });
  return { controller, stream, status, video, startButton, get stopped() { return stopped; },
    get drawn() { return drawn; }, setPixels(value) { pixels = value; },
    tick(now) { video.currentTime += 1 / 30; callback(now); } };
}
const flush = () => new Promise(resolve => setImmediate(resolve));

test("late permission grant after stop releases the camera", async () => {
  let resolve;
  const h = harness(() => new Promise(r => { resolve = r; }));
  const starting = h.controller.start();
  h.controller.stop();
  resolve(h.stream);
  await starting;
  assert.equal(h.stopped, 1);
  assert.equal(h.video.srcObject, null);
});

test("permission rejection restores usable start control", async () => {
  const h = harness(async () => { const error = Error(); error.name = "NotAllowedError"; throw error; });
  await h.controller.start();
  assert.equal(h.startButton.disabled, false);
  assert.match(h.status.textContent, /permission denied/);
});

test("one in-flight request, stale regions discarded after motion", async () => {
  let resolve, calls = 0;
  const h = harness(null, () => { calls++; return new Promise(r => { resolve = r; }); });
  await h.controller.start();
  h.tick(0); h.tick(700);
  await flush();
  h.tick(800); h.tick(900);
  assert.equal(calls, 1);
  h.setPixels(200); h.tick(1000);
  resolve({ ok: true, json: async () => ({ status: "verified", verdict: "SUSPICIOUS",
    tamper_risk_percentage: 60, frame_size: [1280, 720], flagged_regions: [{ box: [1, 2, 3, 4] }] }) });
  await flush();
  assert.equal(h.drawn, 0);
  assert.match(h.status.textContent, /Hold the document still/);
  h.controller.stop();
});

test("stop aborts pending analysis and releases tracks", async () => {
  let signal;
  const h = harness(null, (url, options) => new Promise((resolve, reject) => {
    signal = options.signal;
    signal.addEventListener("abort", () => reject(Error("aborted")));
  }));
  await h.controller.start(); h.tick(0); h.tick(700); await flush();
  h.controller.stop(); await flush();
  assert.equal(signal.aborted, true);
  assert.equal(h.stopped, 1);
  assert.equal(h.status.textContent, "Camera stopped");
});

test("stable result draws regions and does not repeatedly upload", async () => {
  let calls = 0;
  const h = harness(null, async () => { calls++; return { ok: true, json: async () => ({
    status: "verified", verdict: "SUSPICIOUS", tamper_risk_percentage: 60,
    recommendation: "Review", frame_size: [640, 360], flagged_regions: [{ box: [1, 2, 3, 4] }]
  }) }; });
  await h.controller.start(); h.tick(0); h.tick(700); await flush();
  assert.equal(h.drawn, 1);
  h.tick(1500); await flush();
  assert.equal(calls, 1);
  h.controller.stop();
});
