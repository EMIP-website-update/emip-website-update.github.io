# EMIP website

Source for [www.emipws.org](https://www.emipws.org), built with Jekyll on GitHub Pages.

## Updating the site each year

1. **Next workshop on the homepage:** edit `_data/emip.yml` (year, ordinal, host conference, place, dates, call for papers link). Leave a value empty to hide its row.
2. **Workshop list:** add the new year at the top of `_data/editions.yml`. The homepage table, the Previous Workshops page and the year list beside each workshop page all read from it.
3. **Workshop page:** copy `pages/workshop/emip-2027.md` to a new year, change `permalink`, `title` and `sidebar.nav`, and add a matching group to `_data/navigation.yml` (with `children` for a program page).
4. **Top menu:** the first item of `main` in `_data/navigation.yml` points to the current workshop.
5. **Steering committee:** `_data/steering.yml`. Portraits go in `images/portraits/web/` as square JPEGs around 480 px.

Page titles written as `EMIP 2026 Workshop - Program` are shown as a small line ("EMIP 2026 Workshop") above the heading ("Program").

## Theme

The layouts (`_layouts/default.html`, `single.html`, `home.html`), includes (`masthead.html`, `footer.html`, `nav_list`, `editions-table.html`, `people-grid.html`, `scanpath.html`) and styles (`_sass/emip/`) are specific to this site. Fonts (Source Serif 4, IBM Plex Sans and Mono, SIL Open Font License) are served from `assets/fonts/` rather than a font CDN. The older Minimal Mistakes files in `_sass/minimal-mistakes/` and `assets/js/` are no longer loaded and can be removed later.

## Homepage figure

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
