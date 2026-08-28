const ADS_CONFIG = {
  enabled: true,
  adsterraNativeCode: `<script async="async" data-cfasync="false" src="https://pl31064694.profitableratecpmnetwork.com/fa2a35146fbf1897240fbf8dfb9a28aa/invoke.js"></script><div id="container-fa2a35146fbf1897240fbf8dfb9a28aa"></div>`,
};

function renderAds() {
  if (!ADS_CONFIG.enabled) return;
  
  // Hide empty header ad container to keep layout clean
  const headerAd = document.getElementById("ad-header");
  if (headerAd) {
    headerAd.style.display = "none";
  }

  // Render Adsterra Native Banner neatly in Mid Form container
  const midAd = document.getElementById("ad-mid");
  if (midAd) {
    midAd.innerHTML = ADS_CONFIG.adsterraNativeCode;
    
    // Execute script
    const scripts = midAd.querySelectorAll("script");
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

  // Hide empty result native container until needed
  const nativeAd = document.getElementById("ad-native");
  if (nativeAd) {
    nativeAd.style.display = "none";
  }
}

document.addEventListener("DOMContentLoaded", renderAds);
