(function () {
  const browserApi = globalThis.browser || globalThis.chrome;

  function getDefaults() {
    const baseUrl = localStorage.getItem("verislip_api_base") || "http://127.0.0.1:8000";
    const apiKey = localStorage.getItem("verislip_api_key") || "verislip-dev-key";
    return { baseUrl, apiKey };
  }

  function toDisplayVerdict(value) {
    if (!value) {
      return "Pending";
    }
    return value.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
  }

  function renderAuditResult(payload) {
    const panel = document.getElementById("verislip-extension-panel");
    if (!panel) {
      return;
    }

    const loading = panel.querySelector(".verislip-extension-loading");
    const body = panel.querySelector(".verislip-extension-body");
    const error = panel.querySelector(".verislip-extension-error");
    const riskScore = panel.querySelector("#verislip-risk-score");
    const bankName = panel.querySelector("#verislip-bank-name");
    const verdict = panel.querySelector("#verislip-verdict");
    const tags = panel.querySelector("#verislip-tamper-tags");

    loading.classList.add("hidden");
    error.classList.add("hidden");
    body.classList.remove("hidden");

    const score = Number(payload?.tamper_risk_percentage ?? 0);
    riskScore.textContent = `${Math.max(0, Math.min(100, score)).toFixed(1)}%`;
    bankName.textContent = payload?.extracted_metadata?.bank_name || payload?.bank_name || "Unknown";
    verdict.textContent = toDisplayVerdict(payload?.verdict || "pending");

    const findings = Array.isArray(payload?.findings_summary) ? payload.findings_summary : [];
    if (!findings.length) {
      tags.innerHTML = "<li>No tamper tags</li>";
      return;
    }

    tags.innerHTML = findings.slice(0, 4).map((finding) => `<li>${String(finding).slice(0, 32)}</li>`).join("");
  }

  function renderError(message) {
    const panel = document.getElementById("verislip-extension-panel");
    if (!panel) {
      return;
    }

    const loading = panel.querySelector(".verislip-extension-loading");
    const body = panel.querySelector(".verislip-extension-body");
    const error = panel.querySelector(".verislip-extension-error");

    loading.classList.add("hidden");
    body.classList.add("hidden");
    error.textContent = message || "The audit failed.";
    error.classList.remove("hidden");
  }

  function loadAndRender(payload) {
    renderAuditResult(payload);
  }

  function registerPanelHandlers() {
    const panel = document.getElementById("verislip-extension-panel");
    if (!panel || panel.dataset.bound === "true") {
      return;
    }

    panel.dataset.bound = "true";
    panel.querySelector(".verislip-extension-close").addEventListener("click", () => {
      panel.remove();
    });

    const openCockpit = panel.querySelector("#verislip-open-cockpit");
    openCockpit.addEventListener("click", () => {
      const { baseUrl } = getDefaults();
      window.open(`${baseUrl}/`, "_blank", "noopener,noreferrer");
    });
  }

  window.VeriSlipSidebar = {
    renderAuditResult,
    renderError,
    loadAndRender,
    registerPanelHandlers,
    getDefaults
  };

  if (browserApi?.runtime?.onMessage) {
    browserApi.runtime.onMessage.addListener((message, _sender, sendResponse) => {
      if (message?.type === "verislip:result") {
        loadAndRender(message.payload);
        sendResponse({ status: "ok" });
      }
      if (message?.type === "verislip:error") {
        renderError(message.message);
        sendResponse({ status: "ok" });
      }
      return true;
    });
  }
})();
