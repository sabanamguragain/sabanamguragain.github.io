# Sabanam Guragain — Portfolio Site

A single-page static portfolio showcasing two independent data-analytics projects:

1. **Nepal Education & Disability Inclusion Dashboard**
2. **Nepal Economic Indicators Dashboard (FY 2024/25)**

No build step, no dependencies — plain HTML, CSS and vanilla JavaScript.

## Structure

```
portfolio-site/
├── index.html
├── netlify.toml
└── assets/
    ├── css/styles.css
    ├── js/main.js
    ├── img/                  # dashboards shown on the page
    └── downloads/            # full-res PNGs + the Python source, for visitors to download
```

## Deploy to Netlify (free)

**Easiest — drag and drop:**
1. Go to https://app.netlify.com/drop
2. Drag the **`portfolio-site`** folder onto the page.
3. Netlify gives you a live URL (e.g. `random-name.netlify.app`) in seconds.
4. Optional: in Site settings → Domain, rename it to something like `sabanam-guragain.netlify.app`.

**Or via Git (auto-redeploy on push):**
1. Push this folder to a GitHub repo.
2. Netlify → *Add new site* → *Import from Git* → pick the repo.
3. Publish directory: `portfolio-site` (or `.` if the repo root is the site). Build command: leave empty.

## Preview locally

```bash
cd portfolio-site
python3 -m http.server 8000
# open http://localhost:8000
```

## Editing notes

- **Name spelling:** the page uses *Sabanam Guragain* (CV/legal). The LinkedIn link uses the *Sabnam* handle. Change the display name in `index.html` if you prefer *Sabnam* everywhere.
- **Update findings:** stat cards live in `index.html` under each project's `.findings` block.
- **Swap a dashboard image:** replace the file in `assets/img/` (keep the same filename) and the matching one in `assets/downloads/`.
