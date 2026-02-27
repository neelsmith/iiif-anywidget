import json
from pathlib import Path
from urllib.error import URLError

import anywidget
import traitlets

from .iiifutils import Manifest


def _manifest_to_json(manifest_obj, _widget):
    if isinstance(manifest_obj, Manifest):
        return manifest_obj.to_dict()
    return None


def _manifest_from_json(payload, _widget):
    if payload is None:
        return None
    return Manifest.from_dict(payload)


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


def extract_thumbnails(manifest_input):
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
    manifest_url = traitlets.Unicode("").tag(sync=True)
    manifest = traitlets.Instance(Manifest, allow_none=True, default_value=None).tag(
        sync=True,
        to_json=_manifest_to_json,
        from_json=_manifest_from_json,
    )
    items_json = traitlets.Unicode("[]").tag(sync=True)
    selected_info_url = traitlets.Unicode("").tag(sync=True)
    manifest_error = traitlets.Unicode("").tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_manifest()

    @traitlets.observe("manifest_url")
    def _on_manifest_url_change(self, _change):
        self._load_manifest()

    def _load_manifest(self):
        url_value = (self.manifest_url or "").strip()
        if not url_value:
            self.manifest = None
            self.items_json = "[]"
            self.selected_info_url = ""
            self.manifest_error = ""
            return

        try:
            manifest_obj = Manifest.from_url(url_value)
        except (URLError, ValueError, OSError) as err:
            self.manifest = None
            self.items_json = "[]"
            self.selected_info_url = ""
            self.manifest_error = str(err)
            return

        self.manifest = manifest_obj
        thumbnails = extract_thumbnails(manifest_obj.manifest_json)
        self.items_json = json.dumps(thumbnails)
        self.manifest_error = ""

        default_info_url = ""
        if thumbnails and isinstance(thumbnails[0], dict):
            default_info_url = (thumbnails[0].get("info_url") or "").strip()

        self.selected_info_url = default_info_url
