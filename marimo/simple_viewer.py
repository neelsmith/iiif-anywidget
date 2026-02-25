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


@app.cell
def _():
    import marimo as mo
    from iiif_anywidget import IIIFViewer

    return IIIFViewer, mo


@app.cell
def _(imgurl):
    imgurl
    return


@app.cell
def _(IIIFViewer, imgurl):
    viewer = IIIFViewer(url=imgurl.value, height="100px") if imgurl.value else None
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
    return (imgurl,)


if __name__ == "__main__":
    app.run()
