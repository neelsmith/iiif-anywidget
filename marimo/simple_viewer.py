# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "iiif_anywidget",
#   "marimo>=0.20.2",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Simple IIIF Viewer
    Minimal example using `iiif_anywidget.IIIFViewer`.
    """)
    return


@app.cell(hide_code=True)
def _():
    import importlib
    import sys
    from pathlib import Path

    import marimo as mo

    repo_root = Path.cwd().resolve().parent if Path.cwd().name == "marimo" else Path.cwd().resolve()
    src_path = str((repo_root / "src").resolve())
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    for mod_name in list(sys.modules):
        if mod_name == "iiif_anywidget" or mod_name.startswith("iiif_anywidget."):
            del sys.modules[mod_name]

    importlib.invalidate_caches()
    from iiif_anywidget import IIIFViewer

    return IIIFViewer, mo


@app.cell
def _(height, height_unit, height_value, imgurl, mo):
    mo.vstack([
        imgurl,
        height_value,
        height_unit,
        mo.md(f"Current viewer height: **{height}**"),
    ])
    return


@app.cell
def _(IIIFViewer, height, imgurl):
    viewer = IIIFViewer(url=imgurl.value, height=height) if imgurl.value else None
    return (viewer,)


@app.cell
def _(viewer):
    viewer
    return


@app.cell
def _(mo):
    imgurl = mo.ui.text(
        full_width=True,
        label="*IIIF info.json URL*",
        value="https://framemark.vam.ac.uk/collections/2006AN7529/info.json"
    )
    height_value = mo.ui.slider(
        start=100,
        stop=1200,
        step=10,
        value=600,
        label="*Viewer height value*"
    )
    height_unit = mo.ui.dropdown(
        options=["px", "vh", "%"],
        value="px",
        label="*Height unit*"
    )
    return height_unit, height_value, imgurl


@app.cell
def _(height_unit, height_value):
    height = f"{height_value.value}{height_unit.value}"
    return (height,)


if __name__ == "__main__":
    app.run()
