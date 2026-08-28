const ADS_CONFIG = {
  enabled: true,
  adsterraCode: `<script async="async" data-cfasync="false" src="https://pl31064694.profitableratecpmnetwork.com/fa2a35146fbf1897240fbf8dfb9a28aa/invoke.js"></script><div id="container-fa2a35146fbf1897240fbf8dfb9a28aa"></div>`,
  slots: {
    header: { active: true },
    midForm: { active: true },
    nativeResult: { active: true }
  }
};

function renderAds() {
  if (!ADS_CONFIG.enabled) return;
  
  const slots = ["ad-header", "ad-mid", "ad-native"];
  slots.forEach(slotId => {
    const el = document.getElementById(slotId);
    if (el) {
      el.innerHTML = ADS_CONFIG.adsterraCode;
      
      // Force execution of injected script tags
      const scripts = el.querySelectorAll("script");
      scripts.forEach(oldScript => {
        const newScript = document.createElement("script");
        Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
        if (oldScript.src) {
          newScript.src = oldScript.src;
        } else {
          newScript.textContent = oldScript.textContent;
        }
        oldScript.parentNode.replaceChild(newScript, oldScript);
      });
    }
  });
}

document.addEventListener("DOMContentLoaded", renderAds);
