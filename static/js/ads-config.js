const ADS_CONFIG = {
  enabled: true,
  slots: {
    header: {
      active: true,
      code: '<div style="padding:15px; color:#64748b; font-weight:600;">[ Slot Iklan Banner Header ]</div>'
    },
    midForm: {
      active: true,
      code: '<div style="padding:15px; color:#64748b; font-weight:600;">[ Slot Iklan Banner Mid Form ]</div>'
    },
    nativeResult: {
      active: true,
      code: '<div style="padding:15px; color:#64748b; font-weight:600;">[ Slot Iklan Native Result ]</div>'
    }
  }
};

function renderAds() {
  if (!ADS_CONFIG.enabled) return;
  
  const headerAd = document.getElementById("ad-header");
  if (headerAd && ADS_CONFIG.slots.header.active) {
    headerAd.innerHTML = ADS_CONFIG.slots.header.code;
  }
  
  const midAd = document.getElementById("ad-mid");
  if (midAd && ADS_CONFIG.slots.midForm.active) {
    midAd.innerHTML = ADS_CONFIG.slots.midForm.code;
  }
}

document.addEventListener("DOMContentLoaded", renderAds);
