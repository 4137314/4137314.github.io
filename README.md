# Mattia Fait — Personal website

Static portfolio published at <https://4137314.github.io/>. Built with semantic HTML and CSS, without a JavaScript runtime, external fonts, or analytics.

## Content

- `index.html`: introduction, selected projects, education, working approach, and contact.
- `config/style.css`: shared responsive styles for the homepage and project index.
- `portfolio/index.html`: project index; the block between `GENERATED PROJECT INDEX` markers is maintained by `.github/workflows/sync-portfolio.yml` using metadata from `4137314/portfolio`. Edit the source metadata, not the generated block.
- `asset/cv/`: CV source and published PDF, maintained separately from the website copy.
- `tests/test_site.py`: local structural, internal-link, and content-boundary checks.

## Preview and verification

From this repository:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
# Open http://127.0.0.1:8000/
```

In another terminal:

```sh
python3 -m unittest discover -s tests -v
git diff --check
```

Check both pages at narrow mobile and desktop widths. Verify navigation, keyboard focus, text readability, and that all content remains available without JavaScript.

## Editorial boundaries

Describe an undergraduate profile on the Electronics track at the University of Trento, with a bachelor's degree still in progress. Do not imply a completed degree, professional registration, client history, or production engineering experience.

Education summaries are based on the supplied study plan. Only list courses as completed when the source explicitly records a pass; attendance is not completion. Do not publish the private transcript, student identifier, or grades. Avoid graduation dates and credit-completion claims unless independently confirmed.

Project descriptions should point to source code and distinguish implementation, simulation, synthesis, and physical hardware validation. Personal Lean and knowledge-management work is exploratory, not evidence of professional formal-verification expertise. Collaboration language should remain bounded by current experience and study commitments.

The CV is a separate artifact: changes to this site's copy do not regenerate or validate its contents.
