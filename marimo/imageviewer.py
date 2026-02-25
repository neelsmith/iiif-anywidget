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
    # View IIIF image in marimo
    """)
    return


@app.cell(hide_code=True)
def _(imgurl):
    imgurl
    return


@app.cell(hide_code=True)
def _(viewer):
    viewer

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Computation
    """)
    return


@app.cell
def _():
    defaultimg = "https://framemark.vam.ac.uk/collections/2006AN7529/info.json"
    return (defaultimg,)


@app.cell
def _(IIIFViewer, imgurl):
    viewer = None
    if imgurl.value:
        viewer = IIIFViewer(url=imgurl.value)
    return (viewer,)


@app.cell
def _(defaultimg, mo):
    imgurl = mo.ui.text(full_width=True,label="*Request URL*",value=defaultimg)
    return (imgurl,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### IIIF Viewer class
    """)
    return


@app.cell
def _(Path, anywidget, traitlets):
    class IIIFViewer(anywidget.AnyWidget):
        _esm = Path(__file__).parent / "iiif_viewer.js"
        url = traitlets.Unicode().tag(sync=True)


    return (IIIFViewer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Imports
    """)
    return


@app.cell
def _():
    import html
    import json
    from urllib.error import URLError
    from urllib.request import urlopen

    return


@app.cell
def _():
    import anywidget
    import traitlets

    return anywidget, traitlets


@app.cell
def _():
    from pathlib import Path

    return (Path,)


if __name__ == "__main__":
    app.run()
