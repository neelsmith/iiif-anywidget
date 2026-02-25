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


@app.cell
def _():
    import marimo as mo

    return (mo,)


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


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # IIIF image viewer with user interaction
    """)
    return


@app.cell(hide_code=True)
def _(coords_state, mo):
    c = coords_state()
    mo.md(f"""
    *Last click* (pixels): `{c['pixel_x']:.2f},  {c['pixel_y']:.2f}`

    *Normalized* (0.0:1.0): `{c['normalized_x']:.6f}, {c['normalized_y']:.6f}`
    """)
    return


@app.cell
def _(mo):
    imgurl = mo.ui.text(
        full_width=True,
        label="*IIIF info.json URL*",
        value="https://framemark.vam.ac.uk/collections/2006AN7529/info.json",
    )
    height_value = mo.ui.slider(
        start=100,
        stop=1200,
        step=10,
        value=600,
        label="*Viewer height value*",
    )
    height_unit = mo.ui.dropdown(
        options=["px", "vh", "%"],
        value="px",
        label="*Height unit*",
    )
    return height_unit, height_value, imgurl


@app.cell
def _(height_unit, height_value):
    height = f"{height_value.value}{height_unit.value}"
    return (height,)


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
def _(IIIFImageOverlayViewer, height, imgurl):

    viewer = IIIFImageOverlayViewer(
        url=imgurl.value,
        rectangles_csv="0.10,0.12,0.20,0.18\n0.45,0.35,0.16,0.22",
        height=height,
    )
    return (viewer,)


@app.cell(hide_code=True)
def _(viewer):
    viewer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Configuring observer for coordinates
    """)
    return


@app.cell
def _(set_coords_state, viewer):
    def push_state(_change=None):
        "Update valie of coordinates state from viewer object."
        set_coords_state(
            {
                "pixel_x": float(viewer.pixel_x),
                "pixel_y": float(viewer.pixel_y),
                "normalized_x": float(viewer.normalized_x),
                "normalized_y": float(viewer.normalized_y),
            }
        )

    return (push_state,)


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
    return coords_state, set_coords_state


@app.cell
def _(push_state, viewer):
    names = ["pixel_x", "pixel_y", "normalized_x", "normalized_y"]

    old_observer = getattr(viewer, "_marimo_observer", None)
    if old_observer is not None:
        viewer.unobserve(old_observer, names=names)

    viewer.observe(push_state, names=names)
    viewer._marimo_observer = push_state
    push_state()
    return


if __name__ == "__main__":
    app.run()
