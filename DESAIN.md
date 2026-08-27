# 🎨 DOKUMEN SPESIFIKASI DESAIN & STYLING UI/UX (MOBILE-FIRST)

**Nama Project:** Ki.Downloader (Multi-Social Media Video & Media Downloader)  
**Versi Spesifikasi:** 3.0 (Mobile-Optimized & Premium UX Edition)  
**Prinsip Desain Utama:** Modern, Minimalis, Responsive Mobile-First, Ultra Sleek, **STRICT NO NEON COLORS**.

---

## 🛑 STRICT COLOR & AESTHETIC POLICY

- **TIDAK BOLEH MENGGUNAKAN WARNA NEON / STABILO NORAK!** (Tidak ada warna hijau stabilo `#00ff00`, pink menyala `#ff00ff`, cyan terang menyala, atau efek glow menyilaukan mata).
- **Skema Warna "Emerald Obsidian & Clean White":**
  - `Latar Utama (Background)`: Snow White (`#ffffff`) & Slate Light (`#f8fafc`)
  - `Kartu Container`: Pure White (`#ffffff`) dengan border metallic slate (`#e2e8f0`) & soft elevation shadow (`box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04)`).
  - `Warna Aksen Utama (Primary Action)`: Deep Emerald Green (`#059669` ➔ `#047857`)
  - `Warna Aksen Sekunder`: Soft Mint Slate (`#ecfdf5` / `#d1fae5`)
  - `Warna Teks & Headings`: Charcoal Dark (`#0f172a` / `#1e293b`)
  - `Subteks`: Muted Slate (`#64748b`)

---

## 📱 DOKUMENTASI DESAIN TAMPILAN MOBILE & DESKTOP

### 1. Header & Navigasi (Mobile-First)
- **Top Brand Bar:**
  - Logo "Ki.Downloader" (Karakter 'Ki' tebal + '.Downloader' warna Emerald).
  - Badge Status "⚡ Multi-Media Ready".
  - Tombol Action Mobile "⚡ Embed Widget".
- **Responsive Navigation:**
  - Ringkas & rapi di layar HP tanpa elemen yang berdesakan.

### 2. Form Input Utama (Touch-Optimized)
- **Input Field:**
  - Ukuran font input 16px (mencegah auto-zoom browser iOS Safari di HP).
  - Sudut rounded melengkung rapi (`border-radius: 14px`).
  - Efek fokus: Border hijau emerald hangat + soft ring shadow (`rgba(5, 150, 105, 0.15)`).
- **Action Buttons:**
  - Tombol "📋 Tempel" berdampingan dengan input.
  - Tombol utama "⬇️ Download Sekarang" dengan ukuran besar (min-height: 54px) khusus kenyamanan jempol di layar HP.

### 3. Area Hasil Download & Galeri Media
- **Kartu Hasil (Result Card):**
  - Judul media & badge platform (TikTok, Instagram, YouTube, dll).
  - Grid responsif: 1 kolom penuh di layar HP (mobile), 2-3 kolom di tablet/desktop.
- **Media Preview:**
  - Foto: Gambar thumbnail dipotong rasio rapi (`object-fit: cover`, max-height: 240px).
  - Video: Native HTML5 video player dengan kontrol cepat.
- **Pilihan Format Download (Pill Buttons):**
  - Tombol download MP4 HD, MP3 Audio, dan Foto Slide dengan ukuran yang pas ditap di layar HP.

### 4. Penempatan Slot Iklan (Monetisasi Siap Pakai)
- `Header Banner Slot`: Di atas hero section (728x90 desktop / 320x50 mobile).
- `Mid-Form Banner Slot`: Tepat di bawah tombol download utama.
- `Native Result Item Slot`: Di dalam kartu hasil sebelum daftar tombol download.
- `Bottom Sticky Anchor Ad`: Banner melayang di bagian paling bawah layar HP.

### 5. Seksi Panduan ("Cara Menggunakan") & Fitur
- 3 Kartu Langkah Visual (Langkah 1: Salin Tautan, Langkah 2: Tempelkan Link, Langkah 3: Simpan Media).
- 4 Kartu Fitur Unggulan (Tanpa Watermark, Slide Foto & Carousel, DP HD & IG Story/Sorotan, 100% Gratis & Tanpa Login).

### 6. Footer & Copyright
- Copyright Notice: `Copyright © 2026 Ki.Downloader. All Rights Reserved.`
- Tautan Navigasi (Beranda, Cara Pakai, Embed Widget).
- Penafian penggunaan publik secara legal.

---

## 🛠️ KUMPULAN PROMPT TAMBAHAN UNTUK AI DESAIN (PROMPT PACK)

Anda bisa menyalin (*copy-paste*) prompt di bawah ini sesuai dengan jenis AI yang Anda gunakan:

---

### 📱 PROMPT 1: Untuk AI Code Generator (ChatGPT / Claude / v0.dev / Bolt.new)
> "Tolong rombak dan rancang ulang tampilan CSS dan HTML website Ki.Downloader ini menjadi berpenampilan layaknya Aplikasi Mobile Premium (App-like UX) yang sangat nyaman digunakan di HP. 
> **Aturan Utama:**
> 1. Gunakan skema warna Emerald Green (#059669) dan Pure White (#ffffff). SANGAT DILARANG menggunakan warna neon stabilo yang norak!
> 2. Buat komponen form input URL dengan sudut membulat elegan (rounded-pill), tombol Paste yang responsif, dan tombol Download utama dengan tinggi minimal 54px khusus kenyamanan jempol di layar HP.
> 3. Buat kartu hasil download (media gallery) tampil 1 kolom penuh di mobile dengan bayangan halus (soft shadow) dan tombol unduh berdesain pill button.
> 4. Sertakan penataan slot iklan (ad-header, ad-mid, ad-native) agar tetap rapi tanpa merusak tata letak mobile.
> 5. JANGAN MENGUBAH ID elemen HTML (urlInput, btnCheck, resultsCard, mediaGrid, ad-header, ad-mid) agar logika JavaScript backend tetap berfungsi 100%."

---

### 🎨 PROMPT 2: Untuk AI Image Generator / Visual Mockup (Midjourney / DALL-E 3 / Flux / Ideogram)
> "A ultra-sleek, premium mobile web UI mockup for a modern Video Downloader application named 'Ki.Downloader'. Mobile screen perspective, iOS app-like interface, clean snow white background, deep emerald green buttons (#059669), charcoal dark typography, soft elevation shadows, rounded card containers. Beautiful gallery result cards for TikTok and Instagram posts, elegant search bar with paste icon. Clean corporate aesthetic, strictly NO neon colors, photorealistic UI/UX presentation, 8k resolution --ar 9:16 --v 6.0"

---

### ⚡ PROMPT 3: Untuk Khusus Perbaikan Responsive CSS (Tampilan HP)
> "Fokus perbaiki CSS file `style.css` ini agar 100% Mobile-Friendly. Pastikan:
> - Ukuran font input tidak kurang dari 16px agar browser iOS Safari di HP tidak otomatis melakukan zoom-in saat mengetik.
> - Padding dan margin pada layar mobile (< 600px) menggunakan spacing yang lega dan tidak saling bertumpukan.
> - Kartu langkah 'Cara Menggunakan' dan 'Fitur Unggulan' tampil dalam grid 1 kolom yang rapi di layar HP.
> - Menggunakan warna latar #ffffff dan aksen #059669 tanpa efek neon."

---

### 🌟 PROMPT 4: Untuk Micro-Interactions & Loading States
> "Tambahkan efek mikro-interaksi CSS yang halus pada website ini: efek hover tombol download dengan sedikit elevasi (transform translateY(-2px)), animasi skeleton loading saat media sedang dianalisis, dan border ring hijau emerald yang lembut saat kolom input aktif. Pastikan semua animasi berjalan 60fps tanpa lag di browser seluler."
