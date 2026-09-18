const test = require("node:test");
const assert = require("node:assert/strict");
const { install } = require("../../web/js/triage_shortcuts.js");

class FakeDocument {
  constructor() { this.listeners = new Map(); this.activeElement = null; }
  addEventListener(type, listener) {
    const listeners = this.listeners.get(type) || [];
    listeners.push(listener);
    this.listeners.set(type, listeners);
  }
  removeEventListener(type, listener) {
    this.listeners.set(type, (this.listeners.get(type) || []).filter(item => item !== listener));
  }
  dispatch(event) {
    for (const listener of this.listeners.get("keydown") || []) listener(event);
  }
}

function target(selectorMatch = false) {
  return { isContentEditable: false, closest: () => selectorMatch ? {} : null };
}

function keyboardEvent(key, code, overrides = {}) {
  return {
    key, code, target: target(), repeat: false, defaultPrevented: false,
    altKey: false, ctrlKey: false, metaKey: false,
    preventDefault() { this.defaultPrevented = true; },
    ...overrides
  };
}

function setup() {
  const document = new FakeDocument();
  const actions = [];
  const button = action => ({
    disabled: false,
    getAttribute: () => null,
    click: () => actions.push(action)
  });
  const acceptButton = button("accept");
  const flagButton = button("flag");
  const cleanup = install({ document, acceptButton, flagButton });
  return { document, actions, acceptButton, flagButton, cleanup };
}

test("Space triggers Accept and prevents browser scrolling", () => {
  const ctx = setup();
  const event = keyboardEvent(" ", "Space");
  ctx.document.dispatch(event);
  assert.deepEqual(ctx.actions, ["accept"]);
  assert.equal(event.defaultPrevented, true);
  ctx.cleanup();
});

test("X and x trigger Flag", () => {
  const ctx = setup();
  ctx.document.dispatch(keyboardEvent("x", "KeyX"));
  ctx.document.dispatch(keyboardEvent("X", "KeyX"));
  assert.deepEqual(ctx.actions, ["flag", "flag"]);
  ctx.cleanup();
});

test("shortcuts are ignored in typing and interactive controls", () => {
  const ctx = setup();
  for (const key of ["input", "textarea", "select", "search", "editable", "button"]) {
    ctx.document.dispatch(keyboardEvent("x", "KeyX", { target: target(true) }));
  }
  assert.deepEqual(ctx.actions, []);
  ctx.cleanup();
});

test("disabled and unavailable actions are ignored without preventing Space", () => {
  const ctx = setup();
  ctx.acceptButton.disabled = true;
  const event = keyboardEvent(" ", "Space");
  ctx.document.dispatch(event);
  assert.deepEqual(ctx.actions, []);
  assert.equal(event.defaultPrevented, false);
  ctx.cleanup();

  const document = new FakeDocument();
  const actions = [];
  const button = { disabled: false, getAttribute: () => null, click: () => actions.push("accept") };
  const cleanup = install({ document, acceptButton: button, flagButton: button, isActionAvailable: () => false });
  document.dispatch(keyboardEvent(" ", "Space"));
  assert.deepEqual(actions, []);
  cleanup();
});

test("repeated keydown cannot duplicate an action", () => {
  const ctx = setup();
  ctx.document.dispatch(keyboardEvent("x", "KeyX", { repeat: true }));
  assert.deepEqual(ctx.actions, []);
  ctx.cleanup();
});

test("existing button interaction remains available", () => {
  const ctx = setup();
  ctx.acceptButton.click();
  ctx.flagButton.click();
  assert.deepEqual(ctx.actions, ["accept", "flag"]);
  ctx.cleanup();
});

test("installation is idempotent and cleanup removes the global listener", () => {
  const ctx = setup();
  const secondCleanup = install({ document: ctx.document, acceptButton: ctx.acceptButton, flagButton: ctx.flagButton });
  assert.equal((ctx.document.listeners.get("keydown") || []).length, 1);
  secondCleanup();
  ctx.document.dispatch(keyboardEvent("x", "KeyX"));
  assert.deepEqual(ctx.actions, []);
  assert.equal((ctx.document.listeners.get("keydown") || []).length, 0);
});
