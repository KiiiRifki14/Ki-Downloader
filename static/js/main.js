async function pasteClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    if (text) {
      document.getElementById("urlInput").value = text;
    }
  } catch (err) {
    alert("Gagal membaca clipboard. Tempelkan link secara manual.");
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
  btnCheck.innerText = "⏳ Sedang memproses media...";
  resultsCard.style.display = "none";
  mediaGrid.innerHTML = "";

  try {
    const res = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlInput })
    });

    const data = await res.json();
    if (res.ok && data.status === "success") {
      resultsCard.style.display = "block";
      document.getElementById("mediaTitle").innerText = `Ditemukan ${data.files.length} File Media`;

      data.files.forEach((file, index) => {
        const card = document.createElement("div");
        card.className = "media-item";

        let previewHtml = "";
        if (file.is_image) {
          previewHtml = `<img src="${file.relative_url}" class="media-preview" alt="Preview Media">`;
        } else if (file.is_video) {
          previewHtml = `<video src="${file.relative_url}" class="media-preview" controls></video>`;
        }

        card.innerHTML = `
          ${previewHtml}
          <a href="${file.relative_url}" download="${file.filename}" class="btn-download">⬇️ Download Media #${index + 1}</a>
        `;
        mediaGrid.appendChild(card);
      });
    } else {
      alert(data.detail || "Gagal memproses video.");
    }
  } catch (err) {
    alert("Terjadi kesalahan jaringan atau server.");
  } finally {
    btnCheck.disabled = false;
    btnCheck.innerText = "⬇️ Download Sekarang";
  }
}

function openEmbedModal() {
  const embedCode = `<iframe src="${window.location.origin}/embed" width="100%" height="480" frameborder="0"></iframe>`;
  prompt("Salin kode iframe berikut untuk dipasang di website Anda:", embedCode);
}
