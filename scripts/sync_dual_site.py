from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]
DARK = ROOT / "dark"

SYNC_ITEMS = [
    "index.html", "about.html", "contact.html", "research.html", "ongoing-work.html",
    "publications.html", "404.html", "ai-security", "ai-foundations", "posts",
    "papers_articles", "assets/img", "assets/docs", "assets/js"
]

DARK_ONLY_FILES = {
    Path("assets/css/learning-portal.css"),
    Path("assets/css/style.css"),
}


def copy_any(src_rel: str) -> None:
    src = ROOT / src_rel
    dst = DARK / src_rel
    if not src.exists():
        return
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def patch_dark_html(html: Path) -> None:
    rel = html.relative_to(DARK)
    depth = len(rel.parents) - 1
    root_index = ("../" * depth) + "index.html" if depth > 0 else "index.html"

    text = html.read_text(encoding="utf-8")

    # Ensure dark pages keep the dark stylesheet after root files are mirrored in.
    text = text.replace('href="assets/css/learning-portal.css"', 'href="assets/css/style.css"')

    # Convert any copied light-view toggle into a local dark->light toggle.
    text = re.sub(
        r'<a class="brand-hint"[^>]*>\s*Mobile View \(Dark\)\s*</a>',
        f'<a class="brand-hint" href="{root_index}">Light View</a>',
        text,
        flags=re.IGNORECASE,
    )

    # Fallback for older exact strings.
    text = text.replace(
        'href="dark/index.html">Mobile View (Dark)</a>',
        f'href="{root_index}">Light View</a>'
    )
    text = text.replace(
        'href="https://brojogopalsapui.github.io/AISecurityResearch-test/dark/" rel="noopener noreferrer" target="_blank">Mobile View (Dark)</a>',
        f'href="{root_index}">Light View</a>'
    )

    html.write_text(text, encoding="utf-8")


def patch_dark_brand_hints() -> None:
    for html in DARK.rglob("*.html"):
        patch_dark_html(html)


def main() -> None:
    DARK.mkdir(exist_ok=True)
    backups = {}
    for rel in DARK_ONLY_FILES:
        p = DARK / rel
        if p.exists():
            backups[rel] = p.read_bytes()
    for item in SYNC_ITEMS:
        copy_any(item)
    for rel, data in backups.items():
        p = DARK / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    patch_dark_brand_hints()
    print("Done: root content synced into /dark/ with dark theme preserved. Review, then commit + push.")

if __name__ == "__main__":
    main()
