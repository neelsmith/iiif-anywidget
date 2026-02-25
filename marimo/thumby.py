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
def _():
    import importlib
    import json
    import marimo as mo
    import sys
    from pathlib import Path
    from urllib.request import urlopen

    try:
        from iiif_anywidget import IIIFThumbnailGallery, IIIFViewer, extract_thumbnails
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
        from iiif_anywidget import IIIFThumbnailGallery, IIIFViewer, extract_thumbnails
    return (
        IIIFThumbnailGallery,
        IIIFViewer,
        extract_thumbnails,
        json,
        mo,
        urlopen,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # View images from IIIF manifest in marimo
    """)
    return


@app.cell(hide_code=True)
def _(manifest_url):
    manifest_url
    return


@app.cell(hide_code=True)
def _(mo, selected_canvas_info_url):
    mo.md(f"""
    Viewing `{selected_canvas_info_url}`
    """)
    return


@app.cell(hide_code=True)
def _(mo, thumbnail_gallery, viewer):
    mo.hstack([
        viewer,
        mo.md(""),
        thumbnail_gallery

    ], widths = [75, 5, 20])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html("<br/><br/><br/><br/><br/>")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Computation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Manifest URL
    """)
    return


@app.cell
def _(mo):
    manifest_url = mo.ui.text(
        value="https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN623133725/manifest",
        full_width=True,
        label="*Enter IIIF manifest URL*:",
    )
    return (manifest_url,)


@app.cell
def _(json, manifest_url, urlopen):
    def straight_fetch_json(url_input: str) -> dict:
        with urlopen(url_input) as response:
            return json.load(response)

    jsonmanifest = straight_fetch_json(manifest_url.value)
    return (jsonmanifest,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Thumbnail extraction
    """)
    return


@app.cell
def _(extract_thumbnails, jsonmanifest):
    thumbnails = extract_thumbnails(jsonmanifest)
    return (thumbnails,)


@app.cell
def _(thumbnails):
    if thumbnails and isinstance(thumbnails[0], dict):
        default_info_url = (thumbnails[0].get("info_url") or "").strip()
    else:
        default_info_url = ""
    return (default_info_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ### Widgets
    """)
    return


@app.cell
def _(IIIFThumbnailGallery, default_info_url, json, thumbnails):
    thumbnail_gallery = IIIFThumbnailGallery(
        items_json=json.dumps(thumbnails),
        selected_info_url=default_info_url,
    )
    return (thumbnail_gallery,)


@app.cell
def _(IIIFViewer, selected_canvas_info_url):
    viewer = IIIFViewer(url=selected_canvas_info_url)
    return (viewer,)


@app.cell
def _(thumbnail_gallery):
    selected_canvas_info_url = thumbnail_gallery.selected_info_url.strip()
    return (selected_canvas_info_url,)


if __name__ == "__main__":
    app.run()
