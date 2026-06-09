# 🇧🇷 EstudarBR

A mobile-first web app to discover postgraduate programs across Brazil.

## 🚀 Deploy to Netlify (5 minutes)

### Step 1 — Push to GitHub
1. Create a new repo on [github.com](https://github.com)
2. Upload all these files (drag & drop works on GitHub's web UI)
3. Make sure the repo is created with a `main` branch

### Step 2 — Connect Netlify
1. Go to [netlify.com](https://netlify.com) and sign in with GitHub
2. Click **Add new site → Import an existing project**
3. Select **GitHub** and authorize access
4. Pick your `estudarbr` repository

### Step 3 — Build Settings (auto-detected, verify these)
| Field | Value |
|---|---|
| Branch | `main` |
| Build command | `npm run build` |
| Publish directory | `dist` |

4. Click **Deploy site** — done in ~90 seconds!

### Step 4 — Customize Your URL
Under **Site configuration → Domain management**, change the random URL to something like `estudarbr.netlify.app`.

---

## 🛠 Local Development

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

---

## 🤖 Automated Weekly Scraper

The `.github/workflows/auto_scrape.yml` file runs the Python scraper every Sunday at midnight UTC. It:
1. Fetches fresh links from university portals
2. Updates `discovered_programs.json`
3. Commits the changes → Netlify auto-rebuilds the site

To trigger manually: Go to **GitHub → Actions → Weekly Brazil University Scraper → Run workflow**

---

## 📁 Project Structure

```
├── .github/workflows/auto_scrape.yml   # Weekly automation
├── public/_redirects                    # Netlify SPA routing
├── src/
│   ├── App.jsx                          # Main React component
│   ├── main.jsx                         # React entry point
│   └── index.css                        # Tailwind imports
├── index.html
├── netlify.toml                         # Netlify build config
├── package.json
├── scraper.py                           # Python scraper
├── requirements.txt
├── tailwind.config.js
├── vite.config.js
└── discovered_programs.json            # Auto-updated data
```
