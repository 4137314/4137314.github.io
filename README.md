# Mattia Fait — Personal website

Static portfolio published at <https://4137314.github.io/>. Built with semantic HTML and CSS, without a JavaScript runtime, external fonts, or analytics.

## Content

- `index.html`: introduction, selected projects, education, working approach, and contact.
- `config/style.css`: shared responsive styles for the homepage and project index.
- `asset/system-map.svg`: lightweight conceptual system diagram, not a schematic or measured result.
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

## Visual direction

Technical editorial: ink-blue surfaces, mint accents, a restrained drafting grid, and monospace labels alongside system-font headings. Project cards separate conceptual flows from repository evidence and link to both project briefs and source. Keep diagrams explicitly conceptual; do not add fictional plots, benchmarks, or validation badges.

Navigation and project links remain keyboard-accessible, with visible focus, mobile touch targets, and reduced-motion support. Images reserve layout space; there are no external font or script requests. The shared stylesheet also applies to the generated portfolio index without modifying its generated content.

## Editorial boundaries

Describe an undergraduate profile on the Electronics track at the University of Trento, with a bachelor's degree still in progress. Do not imply a completed degree, professional registration, client history, or production engineering experience.

Education summaries are based on the supplied study plan. Only list courses as completed when the source explicitly records a pass; attendance is not completion. Do not publish the private transcript, student identifier, or grades. Avoid graduation dates and credit-completion claims unless independently confirmed.

Project descriptions should point to source code and distinguish implementation, simulation, synthesis, and physical hardware validation. Personal Lean and knowledge-management work is exploratory, not evidence of professional formal-verification expertise. Collaboration language should remain bounded by current experience and study commitments.

## Single-page CV

`asset/cv/main.tex` is the XeLaTeX entry point for the English, one-page A4 CV aimed at scoped freelance Linux systems and automation contracts. It uses 11 pt text, a single-column layout, selectable text, and two selected independent systems projects. Keep the BSc explicitly in progress; do not imply client infrastructure experience, an active VAT registration, or unrestricted availability without confirmation.

Build from `asset/cv/` with `xelatex -interaction=nonstopmode -halt-on-error main.tex` (twice for stable links), then copy `main.pdf` to `cv_mattia_fait.pdf`. Required packages include `fontspec`, Latin Modern fonts, `geometry`, `titlesec`, `enumitem`, `tabularx`, and `hyperref`. Keep intermediate files outside the repository using `-output-directory` when building locally.

With Poppler installed, `python3 -m unittest discover -s tests -p 'test_cv.py' -v` verifies one A4 page and readable key content. The CV workflow installs Poppler and runs these checks before publishing its PDF. Inspect the rendered page as well: automated checks do not prove visual quality. Website copy changes do not automatically update CV content.
