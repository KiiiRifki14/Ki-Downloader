# Multi-Social Media Video Downloader Web App - Design Document

## Overview
A high-performance, ultra-sleek, multi-platform video and media downloader web application built with a FastAPI Python backend and modern HTML5/CSS3/JS frontend. Designed for high concurrent user traffic, ad monetization integration, and cross-site embeddability (`<iframe/widget>`) on third-party websites. Features a clean, bright Emerald & Crisp White aesthetic (strictly no tacky neon colors).

## Architectural Design

### Backend (FastAPI + Asynchronous Task Engine)
- **Framework:** FastAPI with Uvicorn server.
- **Media Engine:** `yt-dlp` + `instaloader` with fallback extraction handlers for:
  - TikTok (No-watermark video & photo slideshow carousels)
  - Instagram (Reels, Posts, Carousel photos/videos)
  - YouTube (HD/SD Videos, Shorts, MP3 Audio extraction)
  - Twitter/X, Facebook, Threads, Pinterest (Direct media fetcher)
- **Endpoints:**
  - `POST /api/analyze`: Accepts `{ "url": "string" }`, inspects platform, extracts metadata (title, thumbnail, duration, media slides list) instantly without downloading full payloads.
  - `POST /api/download`: Accepts `{ "url": "string", "format": "string", "media_id": "optional" }`, downloads requested media to a unique temporary directory (`temp_downloads/{uuid}`), and returns the file download payload.
  - `GET /api/file/{uuid}/{filename}`: Serves downloaded files safely with appropriate mime types.
  - `GET /embed`: Renders the embeddable lightweight downloader widget page.
  - `GET /api/health`: Provides system health status and active sessions metrics.
- **Storage & Auto Cleanup Engine:**
  - Asynchronous background scheduler runs periodically to scrub temporary downloaded files older than 15 minutes to guarantee disk efficiency under high traffic.

### Frontend UI & Aesthetic System (Clean Light Emerald)
- **Theme Palette:**
  - `Background`: Snow White (`#ffffff`) & Soft Slate Grey (`#f8fafc`)
  - `Cards & Containers`: Pure White (`#ffffff`) with subtle drop shadows (`0 4px 20px rgba(0,0,0,0.04)`) and slate borders (`#e2e8f0`)
  - `Primary Accent`: Deep Emerald Green (`#059669` to `#047857`)
  - `Secondary Accent`: Soft Mint Slate (`#ecfdf5` / `#d1fae5`)
  - `Headings & Dark Text`: Charcoal Obsidian (`#0f172a` / `#1e293b`)
  - `Body Text`: Slate Grey (`#64748b`)
  - `No-Neon Guarantee`: Strictly avoids bright fluorescent greens, neon pinks, or cyan glows.
- **Typography:** `Plus Jakarta Sans` / `Inter` from Google Fonts.
- **Key UI Modules:**
  - `Header Bar`: Logo ("Ki.Downloader"), Multi-Platform badges, and "⚡ Embed ke Web Saya" action button.
  - `Top Leaderboard Ad Slot`: Reserved container for 728x90 / 320x50 ad banners.
  - `Hero & Link Form`: Clean URL input bar with "📋 Tempel Link" (Clipboard API) button and "⬇️ Download Sekarang" primary action button.
  - `Results & Gallery Renderer`: Dynamic card listing post metadata, thumbnail, format options (MP4 HD, MP3 Audio, HD Image), and slide carousel for TikTok photos / IG posts.
  - `Native Result Ad Slot`: Placed directly above/below download buttons.
  - `Footer Anchor Ad Slot`: Sticky bottom banner slot.

### Monetization Architecture (Ad Slots Manager)
- Centralized configuration file `static/js/ads-config.js`:
  ```javascript
  const ADS_CONFIG = {
    enabled: true,
    slots: {
      header: { active: true, code: '<!-- AdSense Header Code -->' },
      midForm: { active: true, code: '<!-- AdSense Mid-Form Code -->' },
      nativeResult: { active: true, code: '<!-- Native Ad Code -->' },
      stickyFooter: { active: true, code: '<!-- Sticky Footer Code -->' }
    }
  };
  ```
- Graceful fallback placeholders when ads are disabled or blocked, preventing layout shifts.

### Embed Engine (`/embed` Endpoint & Modal Generator)
- `/embed` route serves `static/embed.html` with minimalist design stripped of main navigation headers/footers.
- Embed Modal Generator: Provides a simple code generator for external site owners:
  ```html
  <iframe src="https://your-domain.com/embed" width="100%" height="480" frameborder="0" allowfullscreen></iframe>
  ```
- Middleware configured with open CORS and adjusted iframe security policies for `/embed` route.

## Verification Plan
1. **API & Downloader Test:** Run pytest / curl requests against `/api/analyze` and `/api/download` with test links (TikTok, IG, YouTube).
2. **Ad Slots Test:** Verify script injection and placeholder behavior in `ads-config.js`.
3. **Embed Test:** Open `/embed` in an iframe sandbox to ensure seamless layout rendering without scrollbars or layout breakage.
4. **UI Aesthetics Test:** Verify light emerald & white styling, responsive layout across mobile and desktop breakpoints.
