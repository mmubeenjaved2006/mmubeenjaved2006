# Setup — Mubeen Javed GitHub Profile

## 1. Create your special GitHub profile repository

Go to https://github.com/new and create a **Public** repository named exactly `mmubeenjaved2006`. Leave **Add a README** unchecked if creating from scratch.

## 2. Unzip and open in VS Code

Extract this ZIP and open the `mubeen-github-profile` folder in VS Code.

## 3. Generate art locally (optional; art is already included)

```powershell
python scripts/render.py
```

Static preview (disables animations, for screenshots):

```powershell
$env:STATIC="1"
python scripts/render.py
Remove-Item Env:STATIC
python scripts/render.py
```

## 4. Push to GitHub

Run these commands in the extracted project folder (PowerShell):

```powershell
git init
git add .
git commit -m "feat: create animated developer profile"
git branch -M mmubeenjaved2006
git remote add origin https://github.com/mmubeenjaved2006/mmubeenjaved2006.git
git push -u origin mmubeenjaved2006
```

If the repository was initialized with a README on GitHub, clone it first and copy the package contents into the clone instead of using `git init`.

## 5. Set GitHub Actions default branch

Go to repository Settings → General → Default branch, and choose `mmubeenjaved2006` if it is not already the default. GitHub scheduled workflows only run on the default branch. For Actions permissions, ensure workflow can write repository contents (Settings → Actions → General → Workflow permissions → Read and write permissions, if available).

## 6. First live graph refresh

Repository → Actions → Refresh animated profile → Run workflow. It fetches **real** public contribution data and creates the graph. If GitHub changes its HTML format, the job fails safely instead of publishing fabricated numbers.

## 7. Verify

Open https://github.com/mmubeenjaved2006 and check the README and clickable project cards. Animations may behave differently in image previews and reduced-motion environments.

## Customize

- Change text, links, and stack in `README.md`.
- Change card text and colors in `scripts/render.py`, then run `python scripts/render.py` and commit the updated `cards/`.
- `cards/activity.svg` is generated only after real contribution data has been fetched.
- No API keys, external font files, or paid services required.

## Troubleshooting

- If the README doesn't appear, confirm repo name = username, repository is Public, and README.md is at root.
- If daily refresh fails, check Actions logs; the public contribution endpoint may have changed.
- If SVG changes don't appear, hard-refresh your GitHub profile; GitHub image caching can delay updates.
