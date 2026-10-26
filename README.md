# مخزن قطع الغيار (Spare Parts Store) — standalone

Static PWA for tracking a maintenance spare-parts store: production lines, equipment,
parts with minimum stock, withdrawals tied to equipment, deposits, and a full movement log.
No build server, no backend. Data lives on the device (localStorage); use
Settings → Backup to export/import, and Settings → Excel reports for CSV files.

## Files

| File | What it is |
| --- | --- |
| `app.html` | The app source (page body). Also published as the Claude artifact. |
| `build.py` | Wraps `app.html` into `index.html`, stamps the version into `sw.js`, draws the icons. |
| `index.html` | Generated. The installable page. |
| `sw.js` | Service worker: network-first page, offline fallback, auto-update on open. |
| `manifest.webmanifest`, `icon-*.png` | Install metadata and icons. |

## Release

1. Edit `app.html`, bump `APP_BUILD` (version shows as `0.<build>` until phase one is done).
2. `python3 build.py`
3. Commit and push. GitHub Pages redeploys; installed phones update on next open.

## Hosting

Must be served over HTTPS (service worker + install).

- **GitHub Pages:** Settings → Pages → Deploy from a branch → `main` / root.
- **Nginx:** copy the folder to e.g. `/var/www/spare-parts`, add a server block, then
  `certbot --nginx -d stock.example.com`. Serve `sw.js` with `Cache-Control: no-cache`.

## Install on the phone

- **Android (Chrome):** open the link → menu ⋮ → Install app / Add to Home screen.
- **iPhone (Safari):** open the link → Share → Add to Home Screen.
