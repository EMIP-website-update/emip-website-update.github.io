# EMIP website

Source for [www.emipws.org](https://www.emipws.org), built with Jekyll on GitHub Pages.

The homepage is only about this year's workshop: a banner of the host city, the title beside Fig. 1 (a real scanpath from the EMIP dataset), then about, call for papers, important dates, submission and organizers on one scrolling page. The top menu jumps to those sections. The rest of the website (past workshops, the dataset pages, tools and resources, steering committee, sponsors) is in the side menu, a column on the left on wide screens and the panel behind the Menu button on smaller ones.

## Updating the site each year

Most of the homepage comes from two data files, so a new year is mostly editing them.

1. **Next workshop:** `_data/emip.yml`: year, ordinal, host conference, place, conference dates, the `dates` list and `status`:
   - `planned`: shows "Call for papers coming soon"; the button jumps to the call.
   - `open`: set `paper_deadline` and `submit_url`; shows "Submissions open" and a "Submit a paper" button.
   - `program`: set `program_url`; shows "Program published" and a "See the program" button.
2. **Call for papers:** `_data/call.yml`: introduction, topics and submission rules. Update `source`, the note shown under the topics.
3. **Organizers:** `organizers` (name, affiliation, url, photo) and `program_committee` ("Name, Affiliation" lines) in `_data/emip.yml`. Until organizers are set, the homepage shows the steering committee; until the committee is set, "Program committee: to be announced". People without a photo get their initials.
4. **Banner photo of the host city:** a JPEG about 1600 px wide plus an 800 px copy in `images/venues/`, referenced under `photo` in `_data/emip.yml`; `position` chooses the part of it the wide banner shows. Prefer public-domain (CC0) photos or your own. If a photo's license asks for credit (for example CC BY), add `credit`, `source`, `license` and `license_url`; the credit then appears under the photo.
5. **After the workshop:** write its page as `pages/workshop/emip-YYYY.md` (copy a recent year), add the next year at the top of `_data/editions.yml`, and update `_data/emip.yml` for the following workshop. The side menu and the Past Workshops page list every edition before the next one. If the year has subpages (program, call for papers), add an `emip-YYYY` group with `children` to `_data/navigation.yml` so the side menu lists them under that year.
6. **Steering committee:** `_data/steering.yml`, shown on the Steering Committee page. Portraits go in `images/portraits/web/` as square JPEGs around 480 px.
7. **Menus:** the top menu is `main` and the side menu's groups are `site` in `_data/navigation.yml`.

Page titles written as `EMIP 2026 Workshop - Program` are shown as a small line ("EMIP 2026 Workshop") above the heading ("Program").

## Theme

The layouts (`_layouts/default.html`, `single.html`, `home.html`, `moved.html`), includes (`masthead.html`, `site-menu.html`, `footer.html`, `editions-table.html`, `people-grid.html`, `scanpath.html`, `photo-credit.html`) and styles (`_sass/emip/`) are specific to this site. `layout: moved` makes a small page that sends an old address on to its new place (for example `/workshop/emip-2027/` to the homepage). Fonts (Source Serif 4, IBM Plex Sans and Mono, SIL Open Font License) are served from `assets/fonts/` rather than a font CDN. The older Minimal Mistakes files in `_sass/minimal-mistakes/` and `assets/js/` are no longer loaded and can be removed later.

## Fig. 1

`_includes/scanpath.html` is generated from the corrected EMIP dataset (`finalset_line_part.csv` from the [EMIP Toolkit](https://github.com/nalmadi/EMIP-Toolkit)):

```
python3 _scripts/make_scanpath.py finalset_line_part.csv --participant 60 --n 45 > _includes/scanpath.html
```

Change `--participant` or `--n` to show a different reader or a longer stretch of reading.

## Local preview

```
bundle install
bundle exec jekyll serve
```
