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
      btnClear.style.display = "flex";
    } else {
      btnClear.style.display = "none";
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
  btnCheck.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> <span>Sedang Memproses...</span>`;
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
        card.className = "media-item";

        let previewHtml = "";
        let btnIcon = "fa-download";
        let btnLabel = `Unduh File #${index + 1}`;

        if (file.is_image) {
          previewHtml = `<div class="media-preview-box"><img src="${file.relative_url}" alt="Preview Gambar #${index + 1}"></div>`;
          btnIcon = "fa-image";
          btnLabel = `Unduh Gambar #${index + 1}`;
        } else if (file.is_video) {
          previewHtml = `<div class="media-preview-box"><video src="${file.relative_url}" controls></video></div>`;
          btnIcon = "fa-circle-play";
          btnLabel = `Unduh Video MP4 #${index + 1}`;
        }

        card.innerHTML = `
          ${previewHtml}
          <a href="${file.relative_url}" download="${file.filename}" class="btn-dl-file">
            <i class="fa-solid ${btnIcon}"></i>
            <span>${btnLabel}</span>
          </a>
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
    btnCheck.innerHTML = `<i class="fa-solid fa-circle-down"></i> <span>Download Sekarang</span>`;
  }
}
