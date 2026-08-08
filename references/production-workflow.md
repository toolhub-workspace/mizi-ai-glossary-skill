# Production workflow

Use this workflow after the user approves the five terms, copy, and six-scene storyboard.

## 1. Freeze the issue

- Record the issue number, final page order, cover title, definitions, analogies, and sources.
- Keep exactly one cover plus five terms.
- Create a fresh `咪子分享/第X期/` directory. If it already contains final files, create a disclosed revision directory instead of overwriting it.

## 2. Generate art-only bases

- Use built-in ImageGen once per page; do not use a template-filled vector composition.
- Use the approved Issue 01 anchors as style-and-energy references, never as edit targets or pose templates.
- Generate exactly one original realistic cat, one oversized core prop, and at most one tiny helper element.
- Preserve one connected, usable copy region for typography. Keep it close enough to the action to avoid an arbitrary empty half-page; vary its position and shape to suit each scene.
- Generate no letters, Chinese characters, numbers, labels, logos, or screen text.
- Default to no arrow or doodle. When a mark is essential, generate it physically inside the raster scene—such as an uneven wax-crayon path on real paper. Never add decorative arrows during post-processing.
- Reject neutral faces, extra props, noisy rooms, corporate polish, vector UI, and accidental text.

## 3. Add deterministic typography

- Copy `assets/templates/issue-config.example.json` beside the issue, fill in the approved copy and per-page coordinates, then run:

```bash
python scripts/render_issue.py --config /absolute/path/to/issue-config.json
```

- Use Marker Felt for short English terms, PingFang for large Chinese cover titles, and the system-installed `WawaSC-Regular.otf` (`娃娃体-简`) for every definition and orange analogy. The renderer finds Wawati SC automatically on macOS and falls back to the bundled `assets/fonts/XiaolaiSC-Regular.ttf` elsewhere.
- Place the large term below the extreme top margin. Do not pin it to the corner.
- Mark the full cat silhouette as a protected region before typesetting. Never place text over the cat.
- Start with deliberately large title and body sizes. Use one gray definition and one larger orange analogy as substantial visual masses, not captions. Reduce size only to protect the cat, preserve contrast, and keep clean line breaks.
- Move the term downward when the page has a dead upper or lower pocket. Prefer two or three confident lines for each body block.
- Allow text to overlap a blank or expendable part of a secondary prop when this improves page balance. Keep the concept-bearing connection and the cat fully readable.
- Do not add small metadata, repeated brand marks, cards, badges, or page numbers.
- Adjust every page independently. The example coordinates are starting points, not a fixed layout system.
- Keep Chinese punctuation with the preceding line. Never leave `、`、`，`、`。` or similar punctuation at a line start or alone on a line.

## 4. Save source records

Save these under `source/`:

- `approved-copy.md`
- `visual-storyboard.md`
- `sources.md`
- `image-prompts.md`
- the filled typography config or render script used for the issue
- the generated contact sheet

## 5. Perform the zero-tolerance QA pass

1. Confirm exactly six PNG and six JPG files exist.
2. Confirm every output is exactly 3000 × 4000 pixels.
3. Inspect the contact sheet for repeated cats, clutter, rigid templating, visual imbalance, dead whitespace, and concept mismatch.
4. Inspect the cover plus at least two term pages at full size.
5. Compare every visible character with `approved-copy.md`, including English capitalization and punctuation.
6. Reject accidental generated text, punctuation-only lines, weak contrast, timid body text, extreme-top titles, isolated blank pockets, vector-like arrows, corner metadata, malformed paws, or neutral expressions.
7. Regenerate the art base when the cat or metaphor fails; revise only typography when the art is sound and the text layout fails.
