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


@app.cell
def _(IIIFImageOverlayViewer):
    viewer = IIIFImageOverlayViewer(
        url="https://framemark.vam.ac.uk/collections/2006AN7529/info.json",
        rectangles_csv="0.10,0.12,0.20,0.18\n0.45,0.35,0.16,0.22",
    )
    return (viewer,)


@app.cell
def _(viewer):
    viewer
    return


if __name__ == "__main__":
    app.run()
