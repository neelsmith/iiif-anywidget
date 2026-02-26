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
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Simple IIIF Viewer
    """)
    return


@app.cell(hide_code=True)
def _(height_pixels, imgurl, mo):
    mo.vstack([imgurl, height_pixels])
    return


@app.cell(hide_code=True)
def _(viewer):
    viewer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Create viewer
    """)
    return


@app.cell
def _(IIIFViewer, height, imgurl):
    viewer = IIIFViewer(url=imgurl.value, height=height) if imgurl.value else None
    return (viewer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## User selections
    """)
    return


@app.cell
def _(mo):
    imgurl =mo.ui.text(value="https://framemark.vam.ac.uk/collections/2006AN7529/info.json",
                       full_width=True,
                       label="*IIIF info.json URL for image*")
    return (imgurl,)


@app.cell
def _(mo):
    height_pixels = mo.ui.slider(start=100,stop=1200,step=10,value=600, label="*Image height (pixels)*",show_value=True)
    return (height_pixels,)


@app.cell
def _(height_pixels):
    height = f"{height_pixels.value}px"
    return (height,)


@app.cell(hide_code=True)
def _():
    import importlib
    import sys
    from pathlib import Path

    # Elaborate fall-back for use in development: not necessary when importing published version of package
    repo_root = Path.cwd().resolve().parent if Path.cwd().name == "marimo" else Path.cwd().resolve()
    src_path = str((repo_root / "src").resolve())
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

    for mod_name in list(sys.modules):
        if mod_name == "iiif_anywidget" or mod_name.startswith("iiif_anywidget."):
            del sys.modules[mod_name]

    importlib.invalidate_caches()
    from iiif_anywidget import IIIFViewer

    return (IIIFViewer,)


if __name__ == "__main__":
    app.run()
