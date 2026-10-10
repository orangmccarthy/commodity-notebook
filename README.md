# Commodities & Geopolitics Notebook

A weekly blog on commodity markets and geopolitics, with an automatically updated price
dashboard and a paper-traded book. Hosted free on GitHub Pages.

## What's where

| File / folder | What it does |
|---|---|
| `_posts/` | Your weekly notes. One Markdown file per post, named `YYYY-MM-DD-title.md`. |
| `dashboard.md` | The dashboard page (prices table and charts). Filled automatically. |
| `trades.md` + `_data/trades.csv` | The trade log. Add a row to the CSV for each trade. |
| `about.md` | About you, how you use AI, and the disclaimer. |
| `_config.yml` | Site title, your name, your domain. |
| `scripts/update_data.py` | Pulls prices and draws charts. Edit `MARKETS` to change markets. |
| `.github/workflows/site.yml` | Runs the data update every Monday and publishes the site. |

## One-time setup

1. Create a **public** repository on GitHub (e.g. `commodity-notebook`).
2. Upload everything in this folder, including the hidden `.github` folder
   (use "Add file → Upload files", or GitHub Desktop). If the `.github` folder doesn't
   come across (it's hidden on Mac and Windows), use "Add file → Create new file", name it
   `.github/workflows/site.yml`, and paste in the contents.
3. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Repo **Settings → Actions → General → Workflow permissions: Read and write**.
5. **Actions** tab → "Update data and publish site" → **Run workflow**. After a few minutes
   your site is live at `https://YOUR-USERNAME.github.io/commodity-notebook/`.

While you're on the `github.io/commodity-notebook` address, set `baseurl: "/commodity-notebook"`
in `_config.yml` so links work. Set it back to `""` once your own domain is connected.

## Connecting your domain

1. Settings → Pages → Custom domain: enter `www.yourdomain.com` and save.
2. At your registrar, add a **CNAME** record: `www` → `YOUR-USERNAME.github.io`
3. Add **A** records for the bare domain (`@`) pointing to:
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
4. Once DNS updates, tick **Enforce HTTPS** in Settings → Pages.
5. Put `url: "https://www.yourdomain.com"` and `baseurl: ""` in `_config.yml`.

## Weekly routine

1. Monday morning: the dashboard updates itself.
2. Write your note as a new file in `_posts/` (copy the shape of the Week 1 post).
3. Log any new trades in `_data/trades.csv`.
4. Commit — the site republishes in a couple of minutes.

*Educational paper portfolio. Not investment advice.*
