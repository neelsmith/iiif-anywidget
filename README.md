# iiif-anywidget

`anywidget`s for working with images served from IIIF sources.

## Usage

```python
from iiif_anywidget import IIIFViewer

viewer = IIIFViewer(
	url="https://framemark.vam.ac.uk/collections/2006AN7529/info.json"
)
viewer
```

## Usage in marimo

A complete marimo notebook:

![Image viewer](./simpleviewer.png)