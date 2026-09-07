# cordian.de — Hugo edition

The same design as the plain-HTML version, rebuilt as a minimal **custom Hugo
site with no theme**. Every shared element is defined exactly once:

| What you edit                    | Where                        |
|----------------------------------|------------------------------|
| Menu                             | `hugo.toml` (`[[menu.main]]`)|
| Header / footer / contact info   | `layouts/partials/` + `hugo.toml` `[params]` |
| Hero text, "Upcoming" line, short intro | `content/_index.md` |
| Aurora gallery                   | drop your `.jpg`/`.png` files into `content/aurora/` — picked up automatically, ordered by filename; Hugo generates the display sizes |
| About page (bio; also shows service, events, positions) | `content/about.md` (Markdown) |
| Teaching                         | `content/teaching.md` (Markdown) |
| Research themes                  | `data/research.yaml`         |
| Conferences & schools organized  | `data/events.yaml` (two more entries sit commented out, awaiting details) |
| Service roles, positions         | `data/service.yaml`, `data/positions.yaml` |
| **Publications**                 | `data/publications.yaml` — one block per paper; add `selected: true` to feature it on the front page |
| Stylesheet                       | `static/css/style.css` (one file) |
| Hero figure                      | `layouts/partials/orbit.html` |

Adding a paper is now: open `data/publications.yaml`, copy a block, done —
both the publications page and the front page update on the next build.

## Deploying (Netlify — your current setup)

Your site deploys via Netlify from the GitHub repository Cordian/HomepageNew
(branch `master`); the DNS for cordian.de is managed by Netlify. Nothing
about that pipeline needs to change — only the repository contents:

1. In a local clone of Cordian/HomepageNew, delete everything except `.git`:
   `find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +`
2. Copy this folder's contents in (including the hidden files):
   `cp -a /path/to/cordian-new/. .`
3. Copy your portrait from the old site (recover it from git):
   `git show HEAD~1:content/authors/admin/avatar.jpg > static/images/portrait.jpg`
   (adjust `HEAD~1` if you have already committed) — and optionally your CV:
   `git show HEAD~1:static/uploads/demo_resume.pdf > static/uploads/cv.pdf`
4. `git add -A && git commit -m "New site: custom Hugo, no theme" && git push`

Netlify picks up the push, reads the included `netlify.toml` (which pins
Hugo 0.128.0 and drops the old Wowchemy cache plugin), builds, and publishes
to www.cordian.de. Watch the deploy at app.netlify.com if you want to see it
happen. No DNS or dashboard changes required.

## Working locally (optional)

Install Hugo (a single binary, no dependencies: https://gohugo.io), then:

    hugo server        # live preview at localhost:1313
    hugo               # build into public/

## Site structure

The front page is deliberately short: hero, research themes, a brief
introduction, and selected publications. Everything else lives on subpages:
`/about/` (biography, service & leadership, organized conferences & schools,
positions & education), `/teaching/`, `/publications/`, and `/aurora/` — a
photo gallery that always renders in the dark "polar night" palette.

## Notes

- No theme, no modules, no npm — the entire template layer is the handful of
  small files in `layouts/`, which you own.
- Things to double-check are the same as before: "current" start years in
  `data/service.yaml`, and the preprints that may since have been published
  (marked `venue: "preprint"` in `data/publications.yaml`).
