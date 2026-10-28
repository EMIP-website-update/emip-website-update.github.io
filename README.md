# EMIP website

Source for [www.emipws.org](https://www.emipws.org), built with Jekyll on GitHub Pages.

The homepage is the page of the next workshop, on one scrolling page: venue photo, call for papers, important dates, submission, organizers, then the EMIP dataset and the past workshops. The menu at the top jumps to each section. Every past workshop keeps its own page under `/workshop/`.

## Updating the site each year

Most of the homepage comes from two data files, so a new year is mostly editing them.

1. **Next workshop:** `_data/emip.yml`: year, ordinal, host conference, place, conference dates, the `dates` list and `status`:
   - `planned`: shows "Call for papers coming soon"; the button jumps to the call.
   - `open`: set `paper_deadline` and `submit_url`; shows "Submissions open" and a "Submit a paper" button.
   - `program`: set `program_url`; shows "Program published" and a "See the program" button.
2. **Call for papers:** `_data/call.yml`: introduction, topics and submission rules. Update `source`, the note shown under the topics.
3. **Organizers:** `organizers` (name, affiliation, url, photo) and `program_committee` ("Name, Affiliation" lines) in `_data/emip.yml`. Until they are set, the homepage shows the steering committee (`_data/steering.yml`) and "Program committee: to be announced". People without a photo get their initials.
4. **Venue photo:** a 4:3 JPEG about 1600 px wide plus an 800 px copy in `images/venues/`, referenced under `photos.photo` in `_data/emip.yml`. Prefer public-domain (CC0) photos or your own. If a photo's license asks for credit (for example CC BY), add `credit`, `source`, `license` and `license_url`; the credit then appears under the photo.
5. **After the workshop:** write its page as `pages/workshop/emip-YYYY.md` (copy a recent year), add the next year at the top of `_data/editions.yml`, and update `_data/emip.yml` for the following workshop. The past-workshops table on the homepage lists every edition before the next one. Add a group to `_data/navigation.yml` only if the year has subpages (program, call for papers) to list beside it.
6. **Steering committee:** `_data/steering.yml`. Portraits go in `images/portraits/web/` as square JPEGs around 480 px.

Page titles written as `EMIP 2026 Workshop - Program` are shown as a small line ("EMIP 2026 Workshop") above the heading ("Program").

## Homepage picture

`hero` in `_data/emip.yml` chooses the picture beside the title:

- `photo`: the venue photo.
- `gaze`: Fig. 1, a real scanpath from the EMIP dataset (below).
- `venue-gaze`: an illustrative scanpath over the venue photo (`_includes/venue-gaze.html`, fixations placed by hand; their coordinates fit the current photo, so redo them for a new one).

Add `?hero=gaze` (or another value) to the homepage address to preview a choice without changing the file.

## Theme

The layouts (`_layouts/default.html`, `single.html`, `home.html`, `moved.html`), includes (`masthead.html`, `footer.html`, `nav_list`, `editions-table.html`, `people-grid.html`, `fold.html`, `scanpath.html`, `venue-gaze.html`, `photo-credit.html`) and styles (`_sass/emip/`) are specific to this site. Longer reference texts on the homepage (dataset files, stimulus material, coding scheme and so on) live in `_includes/onepage/` and open in place. Old addresses such as `/organizers/` or `/dataset/` are small pages with `layout: moved` that send visitors to the matching section. Fonts (Source Serif 4, IBM Plex Sans and Mono, SIL Open Font License) are served from `assets/fonts/` rather than a font CDN. The older Minimal Mistakes files in `_sass/minimal-mistakes/` and `assets/js/` are no longer loaded and can be removed later.

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
