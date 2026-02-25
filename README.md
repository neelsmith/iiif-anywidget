# iiif-anywidget

`anywidget`s to work with images served from IIIF sources in marimo notebooks.


- [notebooks gallery](https://neelsmith.github.io/iiif-anywidget/)

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