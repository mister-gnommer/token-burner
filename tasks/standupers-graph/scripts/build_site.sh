#!/usr/bin/env bash
# Build the static GitHub Pages site for the standupers graph.
# Usage: build_site.sh <output-dir>   (run from the repository root)
# The page to publish is named in graph/PUBLISHED (a path relative to graph/).
# It is published at <output-dir>/standupers/index.html, so the public URL never changes.
set -euo pipefail

out=${1:?usage: build_site.sh <output-dir>}
graph_root=tasks/standupers-graph/graph
pointer=$graph_root/PUBLISHED

[[ -f "$pointer" ]] || { echo "Missing $pointer" >&2; exit 1; }
page_rel=$(grep -vE '^\s*(#|$)' "$pointer" | head -n 1 | tr -d '[:space:]')
page=$graph_root/$page_rel
[[ -f "$page" && "$page" == *.html ]] || { echo "$pointer points to missing HTML page: $page" >&2; exit 1; }
page_dir=$(dirname "$page")

# A page with machine-local paths would publish broken images or scripts.
if grep -nE '(src|href)="(/|file:)' "$page"; then
  echo "$page uses absolute local paths; make them relative to its folder" >&2
  exit 1
fi

rm -rf "$out"
mkdir -p "$out/standupers"
cp "$page" "$out/standupers/index.html"

# Copy any relative files the page references (none for self-contained pages).
refs=$( { grep -oE '(src|href)="[^"#?]+' "$page" || true; } | sed -E 's/^(src|href)="//' \
  | { grep -vE '^([a-z]+:|//)' || true; } | sort -u)
for ref in $refs; do
    [[ -e "$page_dir/$ref" ]] || { echo "$page references missing file: $ref" >&2; exit 1; }
    mkdir -p "$out/standupers/$(dirname "$ref")"
    cp -r "$page_dir/$ref" "$out/standupers/$ref"
  done

cat > "$out/index.html" <<'HTML'
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>token-burner</title>
<meta http-equiv="refresh" content="0; url=standupers/"></head>
<body><a href="standupers/">Standupers graph</a></body></html>
HTML

echo "Published $page -> $out/standupers/index.html"
