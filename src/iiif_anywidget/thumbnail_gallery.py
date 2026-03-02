import json
from pathlib import Path

import anywidget
import traitlets

from .iiifutils import Manifest


def normalize_url(url_value):
    if not isinstance(url_value, str):
        return ""
    clean = url_value.strip()
    if clean.startswith("http://"):
        return "https://" + clean[len("http://") :]
    return clean


def pick_label(label_value):
    if isinstance(label_value, str):
        return label_value
    if isinstance(label_value, list):
        return str(label_value[0]) if label_value else ""
    if isinstance(label_value, dict):
        if "none" in label_value and isinstance(label_value["none"], list) and label_value["none"]:
            return str(label_value["none"][0])
        for value in label_value.values():
            if isinstance(value, list) and value:
                return str(value[0])
    return ""


def thumb_from_service(service):
    if isinstance(service, list) and service:
        service = service[0]
    if not isinstance(service, dict):
        return ""
    base = service.get("@id") or service.get("id")
    if not base:
        return ""
    return f"{base.rstrip('/')}/full/240,/0/default.jpg"


def thumb_from_thumbnail_field(thumbnail):
    if isinstance(thumbnail, list) and thumbnail:
        thumbnail = thumbnail[0]
    if isinstance(thumbnail, str):
        return normalize_url(thumbnail)
    if isinstance(thumbnail, dict):
        thumb_id = thumbnail.get("id") or thumbnail.get("@id") or ""
        return normalize_url(thumb_id)
    return ""


def info_url_from_service(service):
    if isinstance(service, list) and service:
        service = service[0]
    if not isinstance(service, dict):
        return ""
    base = service.get("@id") or service.get("id")
    if not base:
        return ""
    return f"{base.rstrip('/')}/info.json"


def info_url_from_image_id(image_id):
    if not isinstance(image_id, str) or not image_id.strip():
        return ""
    clean = normalize_url(image_id.strip())
    marker = "/full/"
    if marker in clean:
        return normalize_url(f"{clean.split(marker, 1)[0].rstrip('/')}/info.json")
    return ""


def info_url_from_canvas(canvas_item):
    if not isinstance(canvas_item, dict):
        return ""

    if isinstance(canvas_item.get("items"), list) and canvas_item["items"]:
        anno_page = canvas_item["items"][0]
        if isinstance(anno_page, dict) and isinstance(anno_page.get("items"), list) and anno_page["items"]:
            anno = anno_page["items"][0]
            if isinstance(anno, dict):
                body = anno.get("body", {})
                if isinstance(body, dict):
                    service_info = info_url_from_service(body.get("service"))
                    if service_info:
                        return service_info
                    body_id = body.get("id") or body.get("@id")
                    derived = info_url_from_image_id(body_id)
                    if derived:
                        return derived

    if isinstance(canvas_item.get("images"), list) and canvas_item["images"]:
        image = canvas_item["images"][0]
        if isinstance(image, dict):
            resource = image.get("resource", {})
            if isinstance(resource, dict):
                service_info = info_url_from_service(resource.get("service"))
                if service_info:
                    return service_info
                resource_id = resource.get("@id") or resource.get("id")
                derived = info_url_from_image_id(resource_id)
                if derived:
                    return derived

    thumbnail = canvas_item.get("thumbnail")
    if isinstance(thumbnail, list) and thumbnail:
        thumbnail = thumbnail[0]
    if isinstance(thumbnail, dict):
        thumb_id = thumbnail.get("id") or thumbnail.get("@id")
        return info_url_from_image_id(thumb_id)
    if isinstance(thumbnail, str):
        return info_url_from_image_id(thumbnail)

    return ""


def extract_info_urls(manifest_input):
    """Extracts a list of info.json URLs from a IIIF manifest dictionary."""
    output = []
    if not isinstance(manifest_input, dict):
        return output

    if isinstance(manifest_input.get("items"), list):
        canvases_local = manifest_input.get("items", [])
    elif isinstance(manifest_input.get("sequences"), list) and manifest_input["sequences"]:
        canvases_local = manifest_input["sequences"][0].get("canvases", [])
    else:
        canvases_local = []

    for canvas_item in canvases_local:
        info_url = normalize_url(info_url_from_canvas(canvas_item))
        if info_url and info_url not in output:
            output.append(info_url)

    return output


def info_urls_from_manifest(manifest_source):
    """Extracts a list of IIIF image info URLs from a manifest source, which can be a Manifest object, a dictionary, or a URL string."""
    if isinstance(manifest_source, Manifest):
        manifest_json = manifest_source.manifest_json
    elif isinstance(manifest_source, dict):
        manifest_json = manifest_source
    elif isinstance(manifest_source, str):
        manifest_json = Manifest.from_url(manifest_source).manifest_json
    else:
        return []

    return extract_info_urls(manifest_json)


def thumb_from_info_url(info_url):
    clean = normalize_url(info_url)
    if not clean:
        return ""

    suffix = "/info.json"
    if clean.endswith(suffix):
        return f"{clean[: -len(suffix)].rstrip('/')}/full/240,/0/default.jpg"
    return ""


def extract_thumbnails(manifest_input):
    """Extracts a list of thumbnail information from a manifest input, which can be a dictionary representing the manifest."""
    output = []
    if not isinstance(manifest_input, dict):
        return output

    if isinstance(manifest_input.get("items"), list):
        canvases_local = manifest_input.get("items", [])
    elif isinstance(manifest_input.get("sequences"), list) and manifest_input["sequences"]:
        canvases_local = manifest_input["sequences"][0].get("canvases", [])
    else:
        canvases_local = []

    for canvas_index, canvas_item in enumerate(canvases_local, start=1):
        if not isinstance(canvas_item, dict):
            continue

        canvas_label = pick_label(canvas_item.get("label")) or f"Canvas {canvas_index}"
        canvas_thumb_url = thumb_from_thumbnail_field(canvas_item.get("thumbnail"))

        if not canvas_thumb_url:
            if isinstance(canvas_item.get("items"), list) and canvas_item["items"]:
                anno_page_item = canvas_item["items"][0]
                if isinstance(anno_page_item, dict) and isinstance(anno_page_item.get("items"), list) and anno_page_item["items"]:
                    anno_item = anno_page_item["items"][0]
                    if isinstance(anno_item, dict):
                        body_item = anno_item.get("body", {})
                        if isinstance(body_item, dict):
                            canvas_thumb_url = thumb_from_service(body_item.get("service"))
                            if not canvas_thumb_url:
                                body_id = body_item.get("id") or body_item.get("@id") or ""
                                if isinstance(body_id, str) and body_id.strip():
                                    canvas_thumb_url = normalize_url(body_id)

        if not canvas_thumb_url:
            if isinstance(canvas_item.get("images"), list) and canvas_item["images"]:
                image_item = canvas_item["images"][0]
                if isinstance(image_item, dict):
                    resource_item = image_item.get("resource", {})
                    if isinstance(resource_item, dict):
                        canvas_thumb_url = thumb_from_service(resource_item.get("service"))

        canvas_info_url = info_url_from_canvas(canvas_item)

        if canvas_thumb_url:
            output.append(
                {
                    "label": canvas_label,
                    "thumb_url": canvas_thumb_url,
                    "info_url": canvas_info_url,
                }
            )

    return output


class IIIFThumbnailGallery(anywidget.AnyWidget):
    _esm = Path(__file__).parent / "static" / "thumbnail_gallery.js"
    info_urls = traitlets.List(trait=traitlets.Unicode(), default_value=[]).tag(sync=True)
    items_json = traitlets.Unicode("[]").tag(sync=True)
    selected_info_url = traitlets.Unicode("").tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sync_items_from_info_urls()

    @classmethod
    def from_manifest(cls, manifest_url):
        """Constructs a gallery from a IIIF manifest URL."""
        info_urls = info_urls_from_manifest(manifest_url)
        return cls(info_urls=info_urls)

    @traitlets.observe("info_urls")
    def _on_info_urls_change(self, _change):
        self._sync_items_from_info_urls()

    def _sync_items_from_info_urls(self):
        clean_info_urls = []
        for info_url in self.info_urls:
            normalized = normalize_url(info_url)
            if normalized and normalized not in clean_info_urls:
                clean_info_urls.append(normalized)

        if clean_info_urls != self.info_urls:
            self.info_urls = clean_info_urls
            return

        items = []
        for idx, info_url in enumerate(clean_info_urls, start=1):
            thumb_url = thumb_from_info_url(info_url)
            if not thumb_url:
                continue

            items.append(
                {
                    "label": f"Image {idx}",
                    "thumb_url": thumb_url,
                    "info_url": info_url,
                }
            )

        self.items_json = json.dumps(items)

        current_selection = normalize_url(self.selected_info_url)
        if current_selection and current_selection in clean_info_urls:
            self.selected_info_url = current_selection
        elif clean_info_urls:
            self.selected_info_url = clean_info_urls[0]
        else:
            self.selected_info_url = ""
