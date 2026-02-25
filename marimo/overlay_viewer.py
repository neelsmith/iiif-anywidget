# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "iiif-anywidget==0.2.0",
#     "marimo>=0.20.2",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import importlib
    import marimo as mo
    import sys
    from pathlib import Path

    try:
        from iiif_anywidget import IIIFImageOverlayViewer
    except (ImportError, AttributeError):
        repo_src = Path(__file__).resolve().parents[1] / "src"
        if str(repo_src) not in sys.path:
            sys.path.insert(0, str(repo_src))
        stale_modules = [
            module_name
            for module_name in list(sys.modules)
            if module_name == "iiif_anywidget" or module_name.startswith("iiif_anywidget.")
        ]
        for module_name in stale_modules:
            del sys.modules[module_name]
        importlib.invalidate_caches()
        from iiif_anywidget import IIIFImageOverlayViewer

    return IIIFImageOverlayViewer, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # IIIF image overlay viewer
    Rectangles are normalized CSV rows: `x,y,width,height`, each in `[0,1]`.
    """)
    return


@app.cell
def _(mo):
    url = mo.ui.text(
        value="https://framemark.vam.ac.uk/collections/2006AN7529/info.json",
        full_width=True,
        label="*IIIF info.json URL*",
    )
    return (url,)


@app.cell
def _(mo):
    rectangles_csv = mo.ui.text_area(
        value="0.10,0.12,0.20,0.18\n0.45,0.35,0.16,0.22\n0.72,0.10,0.18,0.28",
        full_width=True,
        label="*Rectangles CSV (x,y,width,height normalized to [0,1])*",
    )
    return (rectangles_csv,)


@app.cell
def _(IIIFImageOverlayViewer, rectangles_csv, url):
    widget = IIIFImageOverlayViewer(url=url.value, rectangles_csv=rectangles_csv.value)
    return (widget,)


@app.cell(hide_code=True)
def _(mo, rectangles_csv, url, widget):
    mo.vstack([
        url,
        rectangles_csv,
        widget,
    ])
    return


if __name__ == "__main__":
    app.run()
