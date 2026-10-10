"""Validate the rendered roadmap's required content and interactions."""

from pathlib import Path


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(f"FAIL: {message}")
    print(f"PASS: {message}")


root = Path(__file__).resolve().parents[1] / "_site"
artifact = root.parent / "interactive-roadmap.html"
html = (root / "index.html").read_text(encoding="utf-8")
css = (root / "css/main.css").read_text(encoding="utf-8")
javascript = (root / "js/main.js").read_text(encoding="utf-8")
self_contained = artifact.read_text(encoding="utf-8")

check("YOU ARE HERE" in html, "true starting point is prominent")
check(all(label in html for label in ("Day 0", "Stage 1", "Stage 2")), "roadmap begins at Day 0 and names stages")
check("Trusted with ambiguous work" in html, "final destination is explicit")
check(html.count("<details") >= 10, "roadmap has expandable nodes and branches")
check(html.count("Prerequisite") >= 3, "prerequisites are visible")
check("Readiness gate" in html and "Gate C" in html, "readiness gates are visible")
check("100–160 hours" in html and "300–700 focused hours" in html, "effort ranges are visible")
check('class="skip-link"' in html and "aria-label=" in html, "accessible navigation and labels are present")
check("@media (max-width: 560px)" in css and "@media (prefers-reduced-motion: reduce)" in css, "responsive and reduced-motion styles are present")
check('addEventListener("click"' in javascript and "node.open = shouldOpen" in javascript, "expand and collapse control is interactive")
check("<style>" in self_contained and "<script>" in self_contained, "self-contained artifact embeds its CSS and JavaScript")
check('href="/css/main.css"' not in self_contained and 'src="/js/main.js"' not in self_contained, "self-contained artifact has no local runtime dependencies")
check("http://" not in self_contained and "https://" not in self_contained, "self-contained artifact has no network dependencies")
check("{{" not in self_contained and "}}" not in self_contained, "self-contained artifact has no unrendered Liquid")

print("Roadmap validation complete.")
