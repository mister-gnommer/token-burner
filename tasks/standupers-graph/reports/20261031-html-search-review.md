What this change does: Adds case- and accent-insensitive name search, including Polish ł, plus a collapsible legend/settings card. Commits b131ae7 and 18c779e update the shared template and five saved interactive pages without changing evidence or graph data.

**Must fix**

1. **Search covers the collapsed legend’s reopen button on narrow screens** (`scripts/interactive_template.html:20–22`, `:82`).
   - **What this is:** The legend is fixed at the top left and search is fixed at the top right, both at 16px.
   - **Problem:** At 375px width the 260px search box starts at 99px. After collapsing, the “+” button occupies about 273–299px at 31–54px vertically; the later-painted search input covers it. Browser hit testing returns the search input at the button’s center. The user cannot reopen settings by clicking or tapping the visible header area.
   - **Fix:** Stack or reposition the two controls below a narrow-width breakpoint so they cannot overlap. A small responsive CSS rule is sufficient; regenerate the five pages from the shared template.
   - **If we skip it:** Narrow-window/phone users can collapse settings but cannot reliably reopen them without resizing, reloading or keyboard workarounds.

Initial verdict: fix 1 first.

Checked against the current 100-node graph for one person using a standalone page: all 22 Python tests pass; desktop browser checks confirm case/diacritic matching, ł/l matching, hidden-result count, toggle-driven reveal, Escape clearing, and collapse/expand aria state. Exact 375px headless rendering reproduces the overlap after collapse. The browser resize tool reported unchanged 1280px geometry, so the narrow-screen reproduction used html_preview at 375px instead of relying on that resize. No runtime console errors appeared.

All five saved DATA payloads are byte-for-byte unchanged from 365d966; the latest saved page reproduces exactly from the updated shared template and current graph inputs. No application code was edited. This review is separate from the planned final evidence/project audit.

Not checked: physical mobile devices or Safari; interaction checks used Chromium. No fixes were requested during the initial review.

Resolution (2026-10-31): fixed at the user’s request. A responsive rule moves the legend below search at widths up to 620px and limits its width to the available space. All five saved pages were regenerated from the shared template, preserving their exact saved DATA payloads. The fix is one CSS rule; no evidence, graph scoring or JavaScript behavior changed.

Browser assertions passed at 320,375,620,621 and 1000px: search/legend rectangles do not overlap, the collapse button receives hit testing in both states, and settings reopen correctly. All 22 Python tests pass. The latest page also reproduces exactly from the shared renderer. No new test dependency or source research was needed. These layout checks use Chromium headless rendering, not physical mobile devices or Safari.

Final verdict: Ship. The plan’s separate final project audit (evidence support, source quality, reproducibility and usability) remains outstanding.
