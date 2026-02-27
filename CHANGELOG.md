# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).



## 0.5.0 - 2026-02-27

### Adds

- Adds `Manifest` model in `iiifutils` with URL parsing (`Manifest.from_url`) and serialization helpers (`to_dict` / `from_dict`) for synced widget state.
- Adds `canvaslabel_for_imageid(manifest_json, image_id)` utility to resolve the canvas label for an image id across IIIF Presentation 2 and 3 manifest structures.
- Adds and expands `scripts/smoke_thumbnail_gallery_manifest.py` smoke checks for manifest syncing, thumbnail extraction, and canvas-label lookup (IIIF v2 + v3).

### Changes

- Refactors `IIIFThumbnailGallery` to instantiate a `Manifest` object from `manifest_url` and expose it as a synced traitlet (`manifest`).
- Updates thumbnail gallery frontend to react to `manifest` changes and derive thumbnails from `manifest.manifest_json`, with `items_json` fallback for compatibility.



## 0.4.1 - 2026-02-26

### Fixes

- fixes an error in publishing configuration


## 0.4.0 - 2026-02-26

### Adds

- Adds an optional `height` parameter to `IIIFViewer` and `IIIFImageOverlayViewer` classes


## 0.3.0 - 2026-02-25

### Adds

- `IIIFImageOverlayViewer` class, an `anywidget` object that displays IIIF images with outlined rectangle overlays from normalized CSV rows (`x,y,width,height` in `[0,1]`), and reports both pixel and normalized x,y coordinates on alt-click.


## 0.2.0 - 2026-02-25

### Adds

- `IIIFThumbnailGallery` class, an `anywidget` object that takes an IIIF manifest and creates a gallery of thumbnail images with interactive user selection.


## 0.1.0 - 2026-02-25

Initial release

### Adds

- `IIIFViewer` class, an `anywidget` object for panning and zooming slippy-tile images served from an IIIF source.
