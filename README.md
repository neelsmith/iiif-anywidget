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


## Examples in marimo

A complete image viewer:

![Image viewer](./simpleviewer.png)