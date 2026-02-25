# iiif-anywidget

`anywidget`s to work with images served from IIIF sources in marimo notebooks.



## IIIF image viewer widget

```python
from iiif_anywidget import IIIFViewer

viewer = IIIFViewer(
	url="https://framemark.vam.ac.uk/collections/2006AN7529/info.json"
)
viewer
```


## IIIF manifest browser



```python
from iiif_anywidget import IIIFThumbnailGallery

gallery = IIIFThumbnailGallery(
	manifest_url="https://manifests.sub.uni-goettingen.de/iiif/presentation/PPN623133725/manifest"
)
gallery
```

## IIIF image overlay viewer

```python
from iiif_anywidget import IIIFImageOverlayViewer

viewer = IIIFImageOverlayViewer(
	url="https://framemark.vam.ac.uk/collections/2006AN7529/info.json",
	rectangles_csv="0.10,0.12,0.20,0.18\n0.45,0.35,0.16,0.22",
)
viewer

# Clicked image coordinates (updated after each Alt/Option-click)
viewer.pixel_x, viewer.pixel_y
viewer.normalized_x, viewer.normalized_y
```

`rectangles_csv` expects one rectangle per line as `x,y,width,height`, with normalized values in `[0,1]`.
Alt/Option-clicking the image updates `pixel_x`, `pixel_y`, `normalized_x`, and `normalized_y`.


## Examples in marimo

A complete image viewer:

![Image viewer](./simpleviewer.png)

Minimal overlay example:

- `marimo/minimal_overlay_viewer.py`

### Why Cells 4 and 5 matter in `minimal_overlay_viewer.py`

In that notebook, Cells 4 and 5 are necessary if you want the displayed coordinate values to update live after each Alt/Option-click:

- **Cell 4** creates marimo state (`coords_state`, `set_coords_state`) that the output cell can react to.
- **Cell 5** attaches a `viewer.observe(...)` handler to widget traits (`pixel_x`, `pixel_y`, `normalized_x`, `normalized_y`) and pushes trait changes into that state.

Without this bridge, reading `viewer.pixel_x` directly in a markdown cell is often non-reactive in marimo, so the UI may not refresh even though the widget traits are changing.