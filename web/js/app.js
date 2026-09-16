/**
 * VeriSlip Frontend Application Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // State
  let currentImageBlob = null;
  let currentBase64 = null;
  let currentResults = null;
  let activeView = "original";

  // Elements
  const tabs = document.querySelectorAll(".nav-tab");
  const tabPanes = document.querySelectorAll(".tab-pane");

  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const btnBrowse = document.getElementById("btn-browse");
  const btnRunScan = document.getElementById("btn-run-scan");

  const btnSampleAuth = document.getElementById("btn-sample-auth");
  const btnSampleTamperAmt = document.getElementById("btn-sample-tamper-amt");
  const btnSampleTamperRef = document.getElementById("btn-sample-tamper-ref");

  const bankSelect = document.getElementById("bank-select");
  const refInput = document.getElementById("ref-input");

  const displayImage = document.getElementById("display-image");
  const overlayCanvas = document.getElementById("overlay-canvas");
  const placeholderEmpty = document.getElementById("placeholder-empty");
  const loadingSpinner = document.getElementById("loading-spinner");
  const currentViewBadge = document.getElementById("current-view-badge");

  const togglePills = document.querySelectorAll(".toggle-pill");

  // Verdict Elements
  const verdictTag = document.getElementById("verdict-tag");
  const gaugeFill = document.getElementById("gauge-fill");
  const riskScoreText = document.getElementById("risk-score-text");
  const recText = document.getElementById("rec-text");
  const btnDownloadReport = document.getElementById("btn-download-report");

  const l1Score = document.getElementById("l1-score");
  const l1Desc = document.getElementById("l1-desc");
  const l2Score = document.getElementById("l2-score");
  const l2Desc = document.getElementById("l2-desc");
  const l3Score = document.getElementById("l3-score");
  const l3Desc = document.getElementById("l3-desc");
  const findingsList = document.getElementById("findings-list");

  // WhatsApp Elements
  const waChatBody = document.getElementById("wa-chat-body");
  const btnWaAuth = document.getElementById("btn-wa-auth");
  const btnWaTamper = document.getElementById("btn-wa-tamper");

  // Calculator Elements
  const sellerSlider = document.getElementById("seller-slider");
  const courierSlider = document.getElementById("courier-slider");
  const sellerCount = document.getElementById("seller-count");
  const courierCount = document.getElementById("courier-count");
  const calcMrr = document.getElementById("calc-mrr");

  // 1. TAB NAVIGATION
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tabPanes.forEach(p => p.classList.remove("active"));

      tab.classList.add("active");
      const targetId = `tab-${tab.dataset.tab}`;
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add("active");
    });
  });

  // 2. UPLOAD & DROPZONE
  btnBrowse.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("click", (e) => {
    if (e.target !== btnBrowse) fileInput.click();
  });

  dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
  });

  dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));

  dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelected(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelected(e.target.files[0]);
    }
  });

  function handleFileSelected(file) {
    if (!file.type.startsWith("image/")) {
      alert("Please upload a valid image file.");
      return;
    }
    currentImageBlob = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      currentBase64 = e.target.result;
      showLoadedImage(currentBase64);
    };
    reader.readAsDataURL(file);
  }

  function showLoadedImage(src) {
    placeholderEmpty.classList.add("hidden");
    displayImage.src = src;
    displayImage.classList.remove("hidden");
    activeView = "original";
    updateViewToggles();
    clearCanvasOverlay();
  }

  // 3. QUICK TEST SAMPLES
  btnSampleAuth.addEventListener("click", () => loadSampleSlip(false));
  btnSampleTamperAmt.addEventListener("click", () => loadSampleSlip(true, "ALTER_AMOUNT"));
  btnSampleTamperRef.addEventListener("click", () => loadSampleSlip(true, "ALTER_REFERENCE"));

  async function loadSampleSlip(tampered, tamperType = "ALTER_AMOUNT") {
    setLoading(true);
    try {
      const bank = bankSelect.value || "COMBANK";
      const res = await fetch(`/api/v1/forensics/synthetic-sample?bank_code=${bank}&tampered=${tampered}&tamper_type=${tamperType}`);
      if (!res.ok) throw new Error("Failed to generate sample");
      const data = await res.json();
      currentBase64 = data.image_base64;

      // Convert base64 to blob
      const resBlob = await fetch(data.image_base64);
      currentImageBlob = await resBlob.blob();

      showLoadedImage(data.image_base64);

      // Auto-populate ref input if available
      if (data.metadata && data.metadata.reference_no) {
        refInput.value = data.metadata.reference_no;
      }

      // Automatically trigger forensic analysis for instant demo feedback
      await runAnalysis();
    } catch (err) {
      alert(`Sample error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  // 4. RUN FORENSIC ANALYSIS
  btnRunScan.addEventListener("click", runAnalysis);

  async function runAnalysis() {
    if (!currentImageBlob) {
      alert("Please upload or select a payment slip screenshot first.");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", currentImageBlob, "slip.jpg");
      if (bankSelect.value) formData.append("bank_code", bankSelect.value);
      if (refInput.value) formData.append("reference_no", refInput.value);

      const res = await fetch("/api/v1/verify", {
        method: "POST",
        body: formData
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Verification failed");
      }

      const results = await res.json();
      currentResults = results;
      displayVerdict(results);

      // Default to tamper view if high risk, else original
      if (results.verdict === "HIGH_RISK_TAMPERED" || results.verdict === "SUSPICIOUS") {
        setView("tamper");
      } else {
        setView("original");
      }

      btnDownloadReport.disabled = false;
    } catch (err) {
      alert(`Analysis error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  function displayVerdict(data) {
    const risk = data.tamper_risk_percentage;
    riskScoreText.textContent = `${risk.toFixed(1)}%`;
    gaugeFill.style.width = `${risk}%`;

    verdictTag.className = "verdict-tag";
    if (data.verdict === "AUTHENTIC") {
      verdictTag.classList.add("safe");
      verdictTag.textContent = "VERIFIED SAFE";
    } else if (data.verdict === "SUSPICIOUS") {
      verdictTag.classList.add("caution");
      verdictTag.textContent = "SUSPICIOUS";
    } else {
      verdictTag.classList.add("danger");
      verdictTag.textContent = "HIGH RISK FORGERY";
    }

    recText.textContent = data.recommendation;

    // Multi-layer breakdown
    const l1 = data.layer_breakdowns.layer1_structural;
    l1Score.textContent = `${(l1.score * 100).toFixed(0)}%`;
    l1Score.style.color = l1.is_anomalous ? "var(--accent-rose)" : "var(--accent-emerald)";

    const l2 = data.layer_breakdowns.layer2_classical;
    l2Score.textContent = `${(l2.score * 100).toFixed(0)}%`;
    l2Score.style.color = l2.is_anomalous ? "var(--accent-rose)" : "var(--accent-emerald)";

    const l3 = data.layer_breakdowns.layer3_noise;
    l3Score.textContent = `${(l3.score * 100).toFixed(0)}%`;
    l3Score.style.color = l3.is_anomalous ? "var(--accent-rose)" : "var(--accent-emerald)";

    // Findings
    findingsList.innerHTML = "";
    if (data.findings_summary && data.findings_summary.length > 0) {
      data.findings_summary.forEach(finding => {
        const li = document.createElement("li");
        li.textContent = finding;
        if (data.verdict !== "AUTHENTIC") li.classList.add("warn");
        findingsList.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.className = "findings-empty";
      li.textContent = "No anomalies detected. Structure, ELA, and noise residuals align with authentic slip profiles.";
      findingsList.appendChild(li);
    }
  }

  // 5. VIEW TOGGLES & CANVAS DRAWING
  togglePills.forEach(pill => {
    pill.addEventListener("click", () => {
      setView(pill.dataset.view);
    });
  });

  function setView(viewMode) {
    activeView = viewMode;
    updateViewToggles();

    if (!currentBase64) return;

    if (viewMode === "original") {
      displayImage.src = currentBase64;
      clearCanvasOverlay();
      currentViewBadge.textContent = "Original Screenshot";
    } else if (viewMode === "tamper") {
      displayImage.src = currentBase64;
      drawBoundingBoxes();
      currentViewBadge.textContent = "Localized Tamper Bounding Boxes";
    } else if (viewMode === "ela") {
      clearCanvasOverlay();
      if (currentResults && currentResults.forensic_maps && currentResults.forensic_maps.ela_heatmap_base64) {
        displayImage.src = currentResults.forensic_maps.ela_heatmap_base64;
        currentViewBadge.textContent = "Error Level Analysis (ELA) Heatmap";
      } else {
        alert("Please run forensic scan first to generate ELA map.");
      }
    } else if (viewMode === "noise") {
      clearCanvasOverlay();
      if (currentResults && currentResults.forensic_maps && currentResults.forensic_maps.noise_heatmap_base64) {
        displayImage.src = currentResults.forensic_maps.noise_heatmap_base64;
        currentViewBadge.textContent = "High-Pass Noise Residual Map";
      } else {
        alert("Please run forensic scan first to generate Noise map.");
      }
    }
  }

  function updateViewToggles() {
    togglePills.forEach(p => {
      if (p.dataset.view === activeView) {
        p.classList.add("active");
      } else {
        p.classList.remove("active");
      }
    });
  }

  function drawBoundingBoxes() {
    if (!currentResults || !currentResults.flagged_regions || currentResults.flagged_regions.length === 0) {
      clearCanvasOverlay();
      return;
    }

    const img = displayImage;
    const canvas = overlayCanvas;
    canvas.width = img.clientWidth;
    canvas.height = img.clientHeight;

    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const scaleX = canvas.width / img.naturalWidth;
    const scaleY = canvas.height / img.naturalHeight;

    currentResults.flagged_regions.forEach((reg) => {
      const [x, y, w, h] = reg.box;
      const rx = x * scaleX;
      const ry = y * scaleY;
      const rw = w * scaleX;
      const rh = h * scaleY;

      // Draw bounding box
      ctx.lineWidth = 3;
      ctx.strokeStyle = "#ef4444";
      ctx.fillStyle = "rgba(239, 68, 68, 0.22)";
      ctx.fillRect(rx, ry, rw, rh);
      ctx.strokeRect(rx, ry, rw, rh);

      // Label background
      ctx.fillStyle = "#ef4444";
      const labelText = `${reg.label || "Tampered Area"} (${(reg.confidence * 100).toFixed(0)}%)`;
      ctx.font = "bold 11px Plus Jakarta Sans, sans-serif";
      const textWidth = ctx.measureText(labelText).width;

      const badgeY = Math.max(16, ry - 6);
      ctx.fillRect(rx, badgeY - 14, textWidth + 10, 18);
      ctx.fillStyle = "#ffffff";
      ctx.fillText(labelText, rx + 5, badgeY - 1);
    });
  }

  function clearCanvasOverlay() {
    const canvas = overlayCanvas;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  window.addEventListener("resize", () => {
    if (activeView === "tamper") drawBoundingBoxes();
  });

  displayImage.addEventListener("load", () => {
    if (activeView === "tamper") drawBoundingBoxes();
  });

  // 6. DOWNLOAD AUDIT REPORT
  btnDownloadReport.addEventListener("click", () => {
    if (!currentResults) return;
    const reportData = {
      title: "VeriSlip Forensic Examination Certificate",
      timestamp: new Date().toISOString(),
      verdict: currentResults.verdict,
      risk_percentage: currentResults.tamper_risk_percentage,
      recommendation: currentResults.recommendation,
      layer_signals: currentResults.layer_breakdowns,
      findings: currentResults.findings_summary,
      signature: "CRYPTOGRAPHICALLY_VERIFIED_BY_VERISLIP_AI"
    };

    const blob = new Blob([JSON.stringify(reportData, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `verislip-audit-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  });

  // 7. WHATSAPP BOT SIMULATION
  btnWaAuth.addEventListener("click", () => simulateWhatsAppCheck(false));
  btnWaTamper.addEventListener("click", () => simulateWhatsAppCheck(true));

  async function simulateWhatsAppCheck(isTampered) {
    appendWaMessage("sent", "Forwarded screenshot: [Bank Transfer Receipt.jpg]");

    // Show typing dots
    const typingElem = document.createElement("div");
    typingElem.className = "wa-msg wa-received";
    typingElem.textContent = "VeriSlip Bot is analyzing slip...";
    waChatBody.appendChild(typingElem);
    waChatBody.scrollTop = waChatBody.scrollHeight;

    try {
      // Fetch synthetic sample first
      const sampleRes = await fetch(`/api/v1/forensics/synthetic-sample?bank_code=COMBANK&tampered=${isTampered}&tamper_type=ALTER_AMOUNT`);
      const sampleData = await sampleRes.json();

      // Call whatsapp webhook
      const waRes = await fetch("/api/v1/webhook/whatsapp", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          from_phone: "+94771234567",
          image_base64: sampleData.image_base64,
          caption: "Is this payment genuine?"
        })
      });

      const waData = await waRes.json();
      waChatBody.removeChild(typingElem);

      appendWaMessage("received", waData.reply_text.replace(/\n/g, "<br>"));
    } catch (err) {
      if (typingElem.parentNode) waChatBody.removeChild(typingElem);
      appendWaMessage("received", `Error connecting to WhatsApp webhook: ${err.message}`);
    }
  }

  function appendWaMessage(type, htmlContent) {
    const msg = document.createElement("div");
    msg.className = `wa-msg wa-${type}`;
    msg.innerHTML = htmlContent;

    const time = document.createElement("span");
    time.className = "wa-time";
    const now = new Date();
    time.textContent = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    msg.appendChild(time);

    waChatBody.appendChild(msg);
    waChatBody.scrollTop = waChatBody.scrollHeight;
  }

  // 8. UNIT ECONOMICS CALCULATOR
  sellerSlider.addEventListener("input", updateCalculator);
  courierSlider.addEventListener("input", updateCalculator);

  function updateCalculator() {
    const sellers = parseInt(sellerSlider.value);
    const courierCalls = parseInt(courierSlider.value);

    sellerCount.textContent = sellers.toLocaleString();
    courierCount.textContent = courierCalls.toLocaleString();

    // LKR 1,490 per seller/month + LKR 8 per courier API call
    const sellerRev = sellers * 1490;
    const courierRev = courierCalls * 8;
    const totalRevLkr = sellerRev + courierRev;

    calcMrr.textContent = `LKR ${totalRevLkr.toLocaleString()}`;
  }

  function setLoading(isLoading) {
    if (isLoading) {
      loadingSpinner.classList.remove("hidden");
    } else {
      loadingSpinner.classList.add("hidden");
    }
  }
});
