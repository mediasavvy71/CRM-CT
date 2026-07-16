# Chronic Trace CRM — web deployment

This folder is a clean, deploy-ready copy of the CRM: just `index.html`, a
`vercel.json`, and a `.gitignore`. On purpose, it does **not** include
`app.py` / `data_manager.py` / `requirements.txt` — those are the separate
Python desktop app, and having them in the same repo is what caused Vercel's
earlier error (it saw a `requirements.txt` and tried to run the folder as a
Python web service instead of serving static files).

I verified `index.html` serves correctly from a local static server (200
response, correct title, byte-identical to the source file) before handing
this off.

## Important: what hosting this actually gives you

This is a static site — all the CRM's data still lives in each visitor's own
browser (localStorage), exactly like the local file did. Deploying it to a
URL does **not** create a shared database. If you open the Vercel URL on
your phone and on your laptop, they'll each have their own independent copy
of the data (starting from the same sample data, then diverging). Use
**Settings → Export to Excel** to move data between them, same as before.

If you actually want multiple people or devices sharing one live dataset,
that requires a real backend + database — a different (bigger) build. Let me
know if that's what you're after and I'll scope it separately.

## 1. Push this folder to GitHub

From this folder:

```bash
cd ChronicTraceCRM-Web
git init
git add .
git commit -m "Chronic Trace CRM — static web app"
git branch -M main
```

Create a new empty repo on GitHub (github.com → New repository — don't
initialize it with a README, since you already have files locally). Then:

```bash
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

## 2. Deploy to Vercel

**Option A — Vercel dashboard (easiest):**

1. Go to vercel.com and sign in (GitHub login is simplest).
2. "Add New" → "Project" → import the GitHub repo you just pushed.
3. Framework Preset: choose **Other** (or leave it — Vercel auto-detects
   static sites when there's no `package.json`).
4. Leave Build Command and Output Directory blank/default.
5. Click **Deploy**. You'll get a `*.vercel.app` URL in under a minute.

**Option B — Vercel CLI:**

```bash
npm install -g vercel
cd ChronicTraceCRM-Web
vercel login
vercel        # deploys a preview
vercel --prod # promotes to your production URL
```

Either way, every time you `git push` to `main`, Vercel automatically
redeploys — no manual steps after the first setup.

## Custom domain (optional)

In the Vercel project → Settings → Domains, you can attach a domain you own
(e.g. `crm.chronictrace.com`) instead of the `*.vercel.app` URL.
