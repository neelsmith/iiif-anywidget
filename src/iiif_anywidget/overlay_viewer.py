from pathlib import Path

import anywidget
import traitlets


class IIIFImageOverlayViewer(anywidget.AnyWidget):
    _esm = Path(__file__).parent / "static" / "overlay_viewer.js"
    url = traitlets.Unicode("").tag(sync=True)
    rectangles_csv = traitlets.Unicode("").tag(sync=True)
