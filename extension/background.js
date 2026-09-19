const browserApi = globalThis.browser || globalThis.chrome;

function getContextMenuApi() {
  return browserApi?.contextMenus ? browserApi : null;
}

function sendAuditRequest(tabId, imageUrl) {
  if (!tabId || !imageUrl) {
    return;
  }

  const target = browserApi.tabs && browserApi.tabs.sendMessage ? browserApi.tabs.sendMessage : null;
  if (!target) {
    return;
  }

  target(tabId, {
    action: "audit-image",
    imageUrl,
    pageUrl: null
  });
}

function registerContextMenu() {
  const menuApi = getContextMenuApi();
  if (!menuApi || !menuApi.contextMenus) {
    return;
  }

  menuApi.contextMenus.removeAll(() => {
    menuApi.contextMenus.create({
      id: "verislip-audit",
      title: "Audit with VeriSlip",
      contexts: ["image"],
      documentUrlPatterns: [
        "https://web.whatsapp.com/*",
        "https://mail.google.com/*",
        "https://*.facebook.com/*",
        "https://*.messenger.com/*"
      ]
    });
  });

  menuApi.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId !== "verislip-audit") {
      return;
    }

    sendAuditRequest(tab?.id, info.srcUrl || info.pageUrl || "");
  });
}

registerContextMenu();
