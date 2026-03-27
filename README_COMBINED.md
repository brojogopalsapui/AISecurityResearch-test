# Combined single-repo site

This package keeps both versions in one GitHub Pages repo:
- `/` = main site
- `/dark/` = second mirrored path

## Routine workflow
1. Update the main site at the repo root.
2. Run your normal notebook.
3. Run:
   `python scripts/sync_dual_site.py`
4. Review both `/` and `/dark/` locally.
5. Commit and push once.

## Important note
This combined package was built from the uploaded repo and mirrored into `/dark/` as a one-repo deployment scaffold. If you later keep custom dark-only CSS inside `dark/assets/css/`, the sync script preserves those files during routine sync.
