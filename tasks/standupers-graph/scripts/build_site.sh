#!/usr/bin/env bash
# Build the static GitHub Pages site for the newest standupers graph.
# Usage: build_site.sh <output-dir>   (run from the repository root)
# The newest graph is the highest-numbered graph/batch-NN/ that has a view.html.
# It is published at <output-dir>/standupers/, so the public URL never changes.
set -euo pipefail

out=${1:?usage: build_site.sh <output-dir>}
graph_root=tasks/standupers-graph/graph

latest=$(find "$graph_root" -mindepth 2 -maxdepth 2 -path "$graph_root/batch-[0-9]*/view.html" \
  | grep -E '/batch-[0-9]+/view\.html$' | sort -V | tail -n 1 | xargs -r dirname)
[[ -n "$latest" ]] || { echo "No $graph_root/batch-NN/view.html found" >&2; exit 1; }

# A view with machine-local paths would publish broken images.
if grep -nE '(src|href)="(/|file:)' "$latest/view.html"; then
  echo "$latest/view.html uses absolute local paths; make them relative to its folder" >&2
  exit 1
fi

rm -rf "$out"
mkdir -p "$out/standupers"
cp "$latest/view.html" "$out/standupers/index.html"
cp "$latest/graph.svg" "$out/standupers/"
[[ -d "$latest/assets" ]] && cp -r "$latest/assets" "$out/standupers/"

cat > "$out/index.html" <<'HTML'
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>token-burner</title>
<meta http-equiv="refresh" content="0; url=standupers/"></head>
<body><a href="standupers/">Standupers graph</a></body></html>
HTML

echo "Published $latest -> $out/standupers/"
