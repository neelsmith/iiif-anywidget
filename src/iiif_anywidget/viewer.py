from pathlib import Path

import anywidget
import traitlets


class IIIFViewer(anywidget.AnyWidget):
    _esm = Path(__file__).parent / "static" / "index.js"
    url = traitlets.Unicode().tag(sync=True)
    height = traitlets.Unicode("500px").tag(sync=True)
