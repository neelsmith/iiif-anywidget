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
    import importlib.util
    import marimo as mo
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

    overlay_path = repo_src / "iiif_anywidget" / "overlay_viewer.py"
    spec = importlib.util.spec_from_file_location("iiif_anywidget_overlay_local", overlay_path)
    overlay_module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(overlay_module)
    IIIFImageOverlayViewer = overlay_module.IIIFImageOverlayViewer
    return IIIFImageOverlayViewer, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # IIIF image overlay viewer
    Rectangles are normalized CSV rows: `x,y,width,height`, each in `[0,1]`.
    Alt/Option-click the image to read pixel and normalized coordinates.
    """)
    return


@app.cell(hide_code=True)
def _(url):
    url
    return


@app.cell
def _(IIIFImageOverlayViewer, rectangles_csv, url):
    widget = IIIFImageOverlayViewer(url=url.value, rectangles_csv=rectangles_csv.value)
    return (widget,)


@app.cell(hide_code=True)
def _(mo, widget):
    mo.md(f"Last click: x/y: {widget.pixel_x}/{widget.pixel_y}")
    return


@app.cell(hide_code=True)
def _(widget):
    widget
    return


@app.cell
def _(set_coords_state, widget):
    names = [
        "pixel_x",
        "pixel_y",
        "normalized_x",
        "normalized_y",
    ]

    old_observer = getattr(widget, "_marimo_observer", None)
    if old_observer is not None:
        widget.unobserve(old_observer, names=names)

    def push_state(_change=None):
        set_coords_state(
            {
                "pixel_x": float(widget.pixel_x),
                "pixel_y": float(widget.pixel_y),
                "normalized_x": float(widget.normalized_x),
                "normalized_y": float(widget.normalized_y),
            }
        )

    widget.observe(push_state, names=names)
    widget._marimo_observer = push_state
    push_state()
    return


@app.cell
def _():
    #c = coords_state()
    #mo.md(f"""
    #Pixel: ({c['pixel_x']:.2f}, {c['pixel_y']:.2f})
    #
    #Normalized: ({c['normalized_x']:.6f}, {c['normalized_y']:.6f})
    #""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Mock some data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    url = mo.ui.text(
        value="https://framemark.vam.ac.uk/collections/2006AN7529/info.json",
        full_width=True,
        label="*IIIF info.json URL*",
    )
    return (url,)


@app.cell(hide_code=True)
def _(url):
    url
    return


@app.cell
def _(mo):
    coords_state, set_coords_state = mo.state(
        {
            "pixel_x": -1.0,
            "pixel_y": -1.0,
            "normalized_x": -1.0,
            "normalized_y": -1.0,
        }
    )
    return (set_coords_state,)


@app.cell(hide_code=True)
def _(rectangles_csv):
    rectangles_csv
    return


@app.cell(hide_code=True)
def _(mo):
    rectangles_csv = mo.ui.text_area(
        value="0.10,0.12,0.20,0.18\n0.45,0.35,0.16,0.22\n0.72,0.10,0.18,0.28",
        full_width=True,
        label="*Rectangles CSV (x,y,width,height normalized to [0,1])*",
    )
    return (rectangles_csv,)


if __name__ == "__main__":
    app.run()
