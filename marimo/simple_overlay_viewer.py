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
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # View IIIF image with overlays
    """)
    return


@app.cell(hide_code=True)
def _(height_pixels, imgurl, mo):
    mo.vstack([imgurl,height_pixels])
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
def _():
    mockrectangles = "0.10,0.12,0.20,0.18\n0.45,0.35,0.16,0.22"
    return (mockrectangles,)


@app.cell
def _(IIIFImageOverlayViewer, height, imgurl, mockrectangles):
    viewer = IIIFImageOverlayViewer( url=imgurl.value, rectangles_csv= mockrectangles, height=height)
    return (viewer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## User selections
    """)
    return


@app.cell
def _(mo):
    imgurl = mo.ui.text(value="https://framemark.vam.ac.uk/collections/2006AN7529/info.json",
        full_width=True, label="*IIIF info.json URL for image*")
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
    # careful loading for development work:
    try:
        from iiif_anywidget import IIIFImageOverlayViewer
    except (ImportError, AttributeError):
        import importlib
        import sys
        from pathlib import Path

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
    return (IIIFImageOverlayViewer,)


if __name__ == "__main__":
    app.run()
