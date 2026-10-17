[README.md](https://github.com/user-attachments/files/33600746/README.md)
# CommunityConnectNT

Emergency warnings, shelters and help for the Northern Territory, in the
languages people in Darwin actually speak.

**This is a prototype. It is not an official emergency service.**
Always follow AusAlert, the Bureau of Meteorology and SecureNT.

---

## What is in here

| Path | What it is |
| --- | --- |
| `index.html` | The whole app. One file: markup, styles and script. |
| `scripts/fetch_warnings.py` | Reads NT warnings from the Bureau's FTP service and writes `warnings.json`. Python standard library only, no packages to install. |
| `.github/workflows/warnings.yml` | Runs that script every 10 minutes on GitHub's servers and commits the result. |
| `robots.txt` | Tells search engines not to index the site while it is a prototype. |
| `bom-email-draft.txt` | Ready-to-send email to the Bureau about Registered User status. |
| `LICENSE` | MIT. Covers the code only, not the data. |

The app looks for `warnings.json` next to itself. If the file is missing it
falls back to clearly-labelled example data. If the file is there but older
than 30 minutes, the app hides every warning and tells the reader to go to an
official source instead.

---

## Step 1 — Run it on your own computer

You do not need a web server for this, but using one avoids browser security
warnings about local files.

```bash
cd communityconnectnt
python3 -m http.server 8000
```

Then open <http://localhost:8000> in your browser.

To stop it, press `Ctrl + C`.

## Step 2 — Test the warnings script

```bash
python3 scripts/fetch_warnings.py
```

It prints every NT warning file it finds on the Bureau's FTP service and
writes `warnings.json` into the folder. Reload the browser and the app should
switch from "Sample data" to "Live from the Bureau of Meteorology".

If the Bureau has no warnings in force, the file will be nearly empty. That is
correct behaviour, not a bug.

## Step 3 — Put it on GitHub

Create an empty repository on GitHub first. Do not add a README there, because
this folder already has one.

```bash
cd communityconnectnt
git init
git add .
git commit -m "First version of CommunityConnectNT"
git branch -M main
git remote add origin https://github.com/subediparku-eng/communityconnectnt.git
git push -u origin main
```

## Step 4 — Turn on GitHub Pages

In the repository on github.com:

1. **Settings** → **Pages**
2. Under **Source**, choose **Deploy from a branch**
3. Branch: `main`, folder: `/ (root)`, then **Save**

After a minute or two the app is live at:

```
https://subediparku-eng.github.io/communityconnectnt/
```

## Step 5 — Let the robot write warnings.json

The scheduled job needs permission to commit back to your own repository.
This is the step people usually miss.

1. **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Choose **Read and write permissions**, then **Save**

Then run it once by hand to check it works:

1. Open the **Actions** tab
2. Choose **Update NT warnings** on the left
3. **Run workflow** → **Run workflow**

Watch the run. If it goes green and a `warnings.json` appears in the
repository, it is working. From then on it runs every 10 minutes on its own.

---

## Why this repository is public

Public was a deliberate choice, for three reasons.

1. **It is dated proof of the work.** Every commit carries a timestamp. If
   anyone builds something similar later, the history shows who did it first.
2. **The free plan needs it.** GitHub Pages only works on public repositories
   unless you pay for Pro. More importantly, GitHub Actions is unlimited and
   free on public repositories, but a private one gets only 2,000 minutes a
   month — and the ten-minute schedule needs about 4,300.
3. **It can be shown to anyone.** Code Fair, the NT Government, a future
   employer. A link is enough.

### Findable by a link, not by Google

`robots.txt` blocks search engines, and `index.html` carries a
`noindex, nofollow` tag. Anyone you send the link to can open it. Someone
searching "darwin cyclone shelter" in a panic will not land on a prototype by
accident.

**Delete both when the app is finished and official.** Until then they stay.

### Before you share the link widely

The Bureau's anonymous FTP service is licensed for personal and internal use.
Its own documentation says you may not supply the material to another person,
and that anyone publishing Bureau data should do so as a **Registered User**.

Open `bom-email-draft.txt`, check the details, and send it to
**webreg@bom.gov.au**. Do that before the link goes to anyone outside your
own circle.

---

## Things that are deliberately not finished

- **First Languages are listed but switched off.** Kriol, Yolŋu Matha,
  Pitjantjatjara, Warlpiri, Tiwi and Arrernte emergency wording has to come
  from accredited interpreters and be checked with community representatives.
  The Aboriginal Interpreter Service is the right partner, and the Bureau
  already works with them during cyclones.
- **The shelter list is from the SecureNT website**, which publishes it as
  plain HTML with no capacity figures and no feed. Treat it as a starting
  point, not as live data.
- **The weather card still uses example data.** The fetch script for it has
  not been written yet.

---

## Licence and credit

Warnings and weather data come from the Australian Government Bureau of
Meteorology. Shelter information comes from SecureNT, Northern Territory
Government. Neither endorses this app.

Built by Prakash Subedi, Charles Darwin University.
