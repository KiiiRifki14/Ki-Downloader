async function pasteClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    if (text) {
      document.getElementById("urlInput").value = text;
      toggleClearButton();
    }
  } catch (err) {
    alert("Gagal membaca clipboard. Tempelkan link secara manual.");
  }
}

function clearInput() {
  const input = document.getElementById("urlInput");
  input.value = "";
  toggleClearButton();
  input.focus();
}

function toggleClearButton() {
  const input = document.getElementById("urlInput");
  const btnClear = document.getElementById("btnClear");
  if (btnClear) {
    if (input.value.trim().length > 0) {
      btnClear.classList.remove("hidden");
      btnClear.classList.add("flex");
    } else {
      btnClear.classList.add("hidden");
      btnClear.classList.remove("flex");
    }
  }
}

async function processDownload() {
  const urlInput = document.getElementById("urlInput").value.trim();
  const btnCheck = document.getElementById("btnCheck");
  const resultsCard = document.getElementById("resultsCard");
  const mediaGrid = document.getElementById("mediaGrid");

  if (!urlInput) {
    alert("Harap masukkan link video!");
    return;
  }

  btnCheck.disabled = true;
  btnCheck.innerHTML = `<span class="material-symbols-outlined animate-spin text-[24px]">sync</span> <span>Sedang Memproses...</span>`;
  resultsCard.style.display = "none";
  mediaGrid.innerHTML = "";

  try {
    const res = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlInput })
    });

    let data;
    try {
      data = await res.json();
    } catch (parseError) {
      throw new Error("Server sedang bersiap (restarting). Harap coba klik 'Download Sekarang' sekali lagi.");
    }

    if (res.ok && data.status === "success") {
      resultsCard.style.display = "block";
      document.getElementById("mediaTitle").innerText = `Ditemukan ${data.files.length} File Media`;

      data.files.forEach((file, index) => {
        const card = document.createElement("div");
        card.className = "bg-surface-container-low rounded-xl p-4 flex flex-col gap-3 border border-slate-border shadow-sm";

        let previewHtml = "";
        let btnIcon = "download";
        let btnLabel = `Unduh File #${index + 1}`;

        if (file.is_image) {
          previewHtml = `<div class="relative w-full h-[240px] rounded-lg overflow-hidden bg-surface-container"><img src="${file.relative_url}" class="w-full h-full object-cover" alt="Preview Gambar #${index + 1}"></div>`;
          btnIcon = "image";
          btnLabel = `Unduh Gambar #${index + 1}`;
        } else if (file.is_video) {
          previewHtml = `<div class="relative w-full rounded-lg overflow-hidden bg-charcoal-dark"><video src="${file.relative_url}" class="w-full max-h-[300px] object-contain" controls></video></div>`;
          btnIcon = "movie";
          btnLabel = `Unduh Video MP4 #${index + 1}`;
        }

        card.innerHTML = `
          ${previewHtml}
          <div class="flex flex-col sm:flex-row gap-2 mt-1">
            <a href="${file.relative_url}" download="${file.filename}" class="flex-1 h-[48px] bg-primary text-on-primary rounded-full font-label-md flex items-center justify-center gap-2 active:scale-95 transition-transform shadow-sm hover:bg-primary-hover font-semibold text-sm">
              <span class="material-symbols-outlined text-[20px]">${btnIcon}</span>
              <span>${btnLabel}</span>
            </a>
          </div>
        `;
        mediaGrid.appendChild(card);
      });

      // Smooth scroll to results
      resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } else {
      alert(data.detail || "Gagal memproses video.");
    }
  } catch (err) {
    alert(err.message || "Terjadi kesalahan jaringan atau server.");
  } finally {
    btnCheck.disabled = false;
    btnCheck.innerHTML = `<span class="material-symbols-outlined">download</span> <span>Download Sekarang</span>`;
  }
}
