# Stage 4 — avatar enhancement

Date: 2026-10-30. Added profile photos and a laughing-person silhouette fallback to D2 nodes, with labels below the images. No performer batch started.

`scripts/avatars.py` resolves relative profile image URLs, downloads/decodes supported image formats, saves 160×160 PNGs beside the output, and records source metadata in graph JSON. Missing, failed, invalid, or oversized downloads fall back locally. Cached photos work offline; synthetic runs do not fetch photos. Pillow 12.3.0 was already installed and is now pinned as a project dependency.

Updated `graph/synthetic-demo/` shows the fallback. `graph/avatar-preview/` is an appearance-only example using saved image URLs for Daniel Midas and Łukasz Lotek Lodkowski, plus a missing-photo node; it has no fan evidence or edges. Photo sources are recorded in its JSON: [Midas](https://standup.pl/images/avatars/daniel-midas.png), [Lotek](https://standup.pl/images/avatars/lukasz-lotek-lodkowski.png).

All 16 tests pass, including real WebP decoding from synthetic bytes, cache reuse, failed downloads, invalid bytes, corrupt caches, URL resolution, and D2 label placement. Both previews were rendered with installed D2/ELK and inspected. SVG embeds photo data; editable D2 needs its adjacent assets directory. Live image availability was checked for these two performers only.
