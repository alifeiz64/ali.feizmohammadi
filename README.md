# Ali Feizmohammadi — personal academic website

Website address: https://alifeiz64.github.io/ali.feizmohammadi/

Ready to publish with GitHub Pages. No installation or build is needed for the included pages.

## Publish

1. Put the **contents of this folder** at the root of the `ali.feizmohammadi` repository. `index.html` must be directly in the repository, not inside another enclosing folder.
2. In the repository, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select **main** and **/(root)**, then save. If your default branch has another name, select that branch instead.
5. GitHub will show the published URL in the Pages settings after deployment.

For this repository name, the usual URL is `https://alifeiz64.github.io/ali.feizmohammadi/`. The repository name does not need to change. A root address such as `https://alifeiz64.github.io/` instead requires the special repository name `alifeiz64.github.io`.

## Preview

Open `index.html` in a browser. Navigation, search, and publication filtering also work from local files.

## Edit

The generated HTML files are directly editable. For larger or repeated updates, use the source:

- `source/content/publications.json`: papers and journal details.
- `source/content/talks.json`: talks and recordings.
- `source/content/teaching.json`: courses.
- `source/build.py`: biography, research descriptions, page layout, and contact details.
- `source/assets/site.css`: design.
- `source/assets/site.js`: publication search and mobile menu.

After changing the source, regenerate from the repository directory:

```bash
python3 source/build.py --output .. --base-path /ali.feizmohammadi/
```

Python 3 is only needed to regenerate pages; the hosted site needs no server or dependencies. Commit the regenerated files alongside the source edits. Changes made directly to generated HTML will be overwritten by the next regeneration, so keep recurring edits in the source.

After the GitHub username is known, add canonical metadata and a sitemap by building with:

```bash
python3 source/build.py --output .. --base-path /ali.feizmohammadi/ --base-url https://alifeiz64.github.io/ali.feizmohammadi/
```

All site paths are relative, so assets and navigation work beneath a repository path. The custom 404 page is configured for `/ali.feizmohammadi/`; change `--base-path` if the repository path changes.

## Contents

Home, research, publications, talks, teaching, and a custom 404 page. Includes 37 papers, direct journal/arXiv/PDF links, publication search and filters, a BibLaTeX-compatible bibliography, responsive navigation, a print stylesheet, and contact links. No analytics or third-party runtime requests are included.

The current appointment is Research Associate, Department of Mathematics, University of Toronto, St. George, September 2026–August 2027. The bibliography and activity lists were migrated from the existing website and checked against arXiv. Details are in `SOURCE_NOTES.md`.
