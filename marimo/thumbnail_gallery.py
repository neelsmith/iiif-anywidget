# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "iiif-anywidget==0.1.0",
#     "marimo>=0.20.2",
# ]
# ///

import marimo

__generated_with = "0.20.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # View images from IIIF manifest in marimo

    Combine a `IIIFThumbnailGallery` (right) with an `IIIFViewer` (left).
    """)
    return


@app.cell(hide_code=True)
def _(manifest_url):
    manifest_url
    return


@app.cell(hide_code=True)
def _(galleryblock):
    galleryblock
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Creating a browser app
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Create thumbnail gallery from IIIF manifest:
    """)
    return


@app.cell
def _(IIIFThumbnailGallery, manifest_url):
    thumbnail_gallery = IIIFThumbnailGallery(manifest_url=manifest_url.value)
    return (thumbnail_gallery,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Find currently selected image in gallery:d
    """)
    return


@app.cell
def _(thumbnail_gallery):
    image_info_url = thumbnail_gallery.selected_info_url.strip()
    return (image_info_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Display currently selected image in viewer:
    """)
    return


@app.cell
def _(IIIFViewer, image_info_url):
    viewer = IIIFViewer(url=image_info_url)
    return (viewer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## User selection
    """)
    return


@app.cell
def _(mo):
    manifest_url = mo.ui.text(
        value="https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN623133725/manifest",
        full_width=True,label="*Enter IIIF manifest URL*:")
    return (manifest_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Notebook layout
    """)
    return


@app.cell
def _(mo, thumbnail_gallery, viewer):
    galleryblock = mo.hstack([
            viewer,
            mo.md(""),
            thumbnail_gallery
        ], widths=[75, 5, 20])
    return (galleryblock,)


@app.cell(hide_code=True)
def _():
    import importlib
    import marimo as mo
    import sys
    from pathlib import Path

    try:
        from iiif_anywidget import IIIFThumbnailGallery, IIIFViewer
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
        from iiif_anywidget import IIIFThumbnailGallery, IIIFViewer
    return IIIFThumbnailGallery, IIIFViewer, mo


@app.cell(hide_code=True)
def _(mo, thumbnail_gallery):
    error = (thumbnail_gallery.manifest_error or "").strip()
    if error:
        mo.md(f"⚠️ Could not load manifest: `{error}`")
    return


if __name__ == "__main__":
    app.run()
