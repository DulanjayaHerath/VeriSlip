(function () {
  const browserApi = globalThis.browser || globalThis.chrome;

  function ensureSidebar() {
    const existing = document.getElementById("verislip-extension-panel");
    if (existing) {
      return Promise.resolve(existing);
    }

    const styleLink = document.createElement("link");
    styleLink.rel = "stylesheet";
    styleLink.href = browserApi.runtime.getURL("sidebar.css");
    document.head.appendChild(styleLink);

    const sidebarScript = document.createElement("script");
    sidebarScript.src = browserApi.runtime.getURL("sidebar.js");
    document.head.appendChild(sidebarScript);

    return new Promise((resolve, reject) => {
      sidebarScript.onload = () => {
        fetch(browserApi.runtime.getURL("sidebar.html"))
          .then((response) => response.text())
          .then((markup) => {
            const wrapper = document.createElement("div");
            wrapper.innerHTML = markup.trim();
            const panel = wrapper.firstElementChild;
            document.body.appendChild(panel);
            resolve(panel);
          })
          .catch(reject);
      };
      sidebarScript.onerror = () => reject(new Error("The VeriSlip sidebar could not be loaded."));
    });
  }

  function dataUrlToBlob(dataUrl) {
    const byteString = atob(dataUrl.split(",")[1]);
    const mimeString = dataUrl.split(",")[0].split(":")[1].split(";")[0];
    const arrayBuffer = new Uint8Array(byteString.length);
    for (let index = 0; index < byteString.length; index += 1) {
      arrayBuffer[index] = byteString.charCodeAt(index);
    }
    return new Blob([arrayBuffer], { type: mimeString || "image/png" });
  }

  function imageToDataUri(src) {
    return new Promise((resolve, reject) => {
      if (src.startsWith("data:")) {
        resolve(src);
        return;
      }

      const image = new Image();
      image.crossOrigin = "anonymous";
      image.onload = () => {
        const canvas = document.createElement("canvas");
        canvas.width = image.naturalWidth;
        canvas.height = image.naturalHeight;
        const context = canvas.getContext("2d");
        context.drawImage(image, 0, 0);
        resolve(canvas.toDataURL("image/png"));
      };
      image.onerror = () => reject(new Error("The selected image could not be loaded."));
      image.src = src;
    });
  }

  async function runAudit(imageUrl) {
    const panel = await ensureSidebar();
    if (window.VeriSlipSidebar && typeof window.VeriSlipSidebar.registerPanelHandlers === "function") {
      window.VeriSlipSidebar.registerPanelHandlers();
    }

    const auditForm = new FormData();
    const dataUrl = await imageToDataUri(imageUrl);
    const file = dataUrlToBlob(dataUrl);
    const baseUrl = localStorage.getItem("verislip_api_base") || "http://127.0.0.1:8000";
    const apiKey = localStorage.getItem("verislip_api_key") || "verislip-dev-key";

    auditForm.append("file", file, "receipt.png");
    auditForm.append("bank_code", "GENERIC_CEFTS");

    const response = await fetch(`${baseUrl}/api/v1/verify`, {
      method: "POST",
      headers: {
        "X-API-Key": apiKey
      },
      body: auditForm
    });

    if (!response.ok) {
      const payload = await response.json().catch(() => ({ detail: "The VeriSlip API rejected the request." }));
      throw new Error(payload.detail || "The VeriSlip API rejected the request.");
    }

    const payload = await response.json();
    if (panel && window.VeriSlipSidebar && typeof window.VeriSlipSidebar.renderAuditResult === "function") {
      window.VeriSlipSidebar.renderAuditResult(payload);
    }
    return payload;
  }

  browserApi.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message?.action === "audit-image") {
      runAudit(message.imageUrl)
        .then(() => sendResponse({ ok: true }))
        .catch((error) => {
          if (window.VeriSlipSidebar && typeof window.VeriSlipSidebar.renderError === "function") {
            window.VeriSlipSidebar.renderError(error.message || "Unknown audit error");
          }
          sendResponse({ ok: false, error: error.message || "Unknown audit error" });
        });
      return true;
    }

    return false;
  });
})();
