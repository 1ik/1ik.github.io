"""Create dependency-free and self-contained roadmap previews."""

from pathlib import Path
import argparse
import re
import shutil


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "_site"


def render(source: str) -> str:
    source = re.sub(r"\A---\s.*?\s---\s*", "", source, count=1, flags=re.DOTALL)
    return re.sub(
        r'\{\{\s*"([^"]+)"\s*\|\s*prepend:\s*site\.baseurl\s*\}\}',
        r"/\1",
        source,
    )


def without_frontmatter(source: str) -> str:
    return re.sub(r"\A---\s.*?\s---\s*", "", source, count=1, flags=re.DOTALL)


def self_contained(html: str, css: str, javascript: str) -> str:
    html = re.sub(
        r'\s*<link rel="stylesheet" href="/css/main\.css">',
        f"\n    <style>\n{css}\n    </style>",
        html,
        count=1,
    )
    return re.sub(
        r'\s*<script src="/js/main\.js"></script>',
        f"\n    <script>\n{without_frontmatter(javascript)}\n    </script>",
        html,
        count=1,
    )


parser = argparse.ArgumentParser()
parser.add_argument("--copy-to", type=Path)
arguments = parser.parse_args()

DESTINATION.mkdir(exist_ok=True)
rendered_html = render((ROOT / "index.html").read_text(encoding="utf-8"))
css = (ROOT / "css/main.css").read_text(encoding="utf-8")
javascript = (ROOT / "js/main.js").read_text(encoding="utf-8")

(DESTINATION / "index.html").write_text(rendered_html, encoding="utf-8")

for directory in ("css", "js", "images"):
    target = DESTINATION / directory
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(ROOT / directory, target)

artifact = self_contained(rendered_html, css, javascript)
(ROOT / "interactive-roadmap.html").write_text(artifact, encoding="utf-8")

if arguments.copy_to:
    arguments.copy_to.parent.mkdir(parents=True, exist_ok=True)
    arguments.copy_to.write_text(artifact, encoding="utf-8")
    print(f"Copied self-contained artifact to {arguments.copy_to}")

print(f"Built portable preview at {DESTINATION}")
print(f"Built self-contained artifact at {ROOT / 'interactive-roadmap.html'}")
