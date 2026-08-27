const ADS_CONFIG = {
  enabled: true,
  publisherId: "ca-pub-8407690253451748",
  slots: {
    header: {
      active: true,
      code: '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8407690253451748" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
    },
    midForm: {
      active: true,
      code: '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8407690253451748" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
    },
    nativeResult: {
      active: true,
      code: '<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-8407690253451748" data-ad-slot="auto" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
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
