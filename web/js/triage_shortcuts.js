/** Keyboard shortcut controller for merchant triage. */
(function exposeTriageShortcuts(root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.VeriSlipTriageShortcuts = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function createApi() {
  const activeControllers = new WeakMap();
  const editableSelector = [
    "input",
    "textarea",
    "select",
    "button",
    "a[href]",
    "[contenteditable]:not([contenteditable='false'])",
    "[role='textbox']",
    "[role='searchbox']",
    "[role='combobox']",
    "[role='spinbutton']"
  ].join(",");

  function isEditableTarget(target) {
    if (!target || typeof target !== "object") return false;
    if (target.isContentEditable) return true;
    return typeof target.closest === "function" && Boolean(target.closest(editableSelector));
  }

  function actionIsAvailable(button, isActionAvailable) {
    return Boolean(
      button &&
      !button.disabled &&
      button.getAttribute("aria-disabled") !== "true" &&
      (!isActionAvailable || isActionAvailable())
    );
  }

  function install(options) {
    const doc = options.document;
    if (!doc || typeof doc.addEventListener !== "function") {
      throw new TypeError("A document-like event target is required.");
    }
    const existing = activeControllers.get(doc);
    if (existing) return existing.cleanup;

    function handleKeydown(event) {
      if (event.repeat || event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
      if (isEditableTarget(event.target || doc.activeElement)) return;

      let button = null;
      if (event.code === "Space" || event.key === " ") button = options.acceptButton;
      else if (event.key === "x" || event.key === "X") button = options.flagButton;

      if (button) {
        if (!actionIsAvailable(button, options.isActionAvailable)) return;
        if (event.code === "Space" || event.key === " ") event.preventDefault();
        button.click();
        return;
      }
      if (typeof options.onUnhandledKeydown === "function") options.onUnhandledKeydown(event);
    }

    function cleanup() {
      const current = activeControllers.get(doc);
      if (!current || current.handleKeydown !== handleKeydown) return;
      doc.removeEventListener("keydown", handleKeydown);
      activeControllers.delete(doc);
    }

    doc.addEventListener("keydown", handleKeydown);
    activeControllers.set(doc, { handleKeydown, cleanup });
    return cleanup;
  }

  return { install, isEditableTarget };
});
