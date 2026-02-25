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

```python
import marimo as mo
from iiif_anywidget import IIIFViewer

viewer = IIIFViewer(
    url="https://framemark.vam.ac.uk/collections/2006AN7529/info.json"
)

mo.md("### IIIF Viewer")
viewer
```
