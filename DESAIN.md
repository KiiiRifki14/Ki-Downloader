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
