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
import json
from iiif_anywidget import IIIFThumbnailGallery, extract_thumbnails

thumbnails = extract_thumbnails(manifest_json)
gallery = IIIFThumbnailGallery(
	items_json=json.dumps(thumbnails),
	selected_info_url=thumbnails[0]["info_url"] if thumbnails else "",
)
gallery
```

## Examples in marimo

A complete image viewer:

![Image viewer](./simpleviewer.png)