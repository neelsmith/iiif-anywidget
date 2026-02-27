import json
from urllib.request import urlopen


class Manifest:
    """A class representing a IIIF manifest."""

    def __init__(self, manifest_json=None, source_url=""):
        self.manifest_json = manifest_json if isinstance(manifest_json, dict) else {}
        self.source_url = source_url.strip() if isinstance(source_url, str) else ""

    @classmethod
    def from_url(cls, source_url):
        clean_url = source_url.strip() if isinstance(source_url, str) else ""
        if not clean_url:
            raise ValueError("manifest_url is required")

        with urlopen(clean_url) as response:
            parsed_json = json.load(response)

        if not isinstance(parsed_json, dict):
            raise ValueError("IIIF manifest JSON must be an object")

        return cls(manifest_json=parsed_json, source_url=clean_url)

    @classmethod
    def from_dict(cls, payload):
        if not isinstance(payload, dict):
            return cls()
        return cls(
            manifest_json=payload.get("manifest_json"),
            source_url=payload.get("source_url", ""),
        )

    def to_dict(self):
        return {
            "source_url": self.source_url,
            "manifest_json": self.manifest_json,
        }


def _normalize_url(url_value):
    if not isinstance(url_value, str):
        return ""
    clean = url_value.strip()
    if clean.startswith("http://"):
        return "https://" + clean[len("http://") :]
    return clean


def _pick_label(label_value):
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


def _manifest_dict_from_input(manifest_input):
    if isinstance(manifest_input, Manifest):
        return manifest_input.manifest_json
    if not isinstance(manifest_input, dict):
        return {}
    if isinstance(manifest_input.get("manifest_json"), dict):
        return manifest_input["manifest_json"]
    return manifest_input


def _canonical_candidates(url_value):
    clean = _normalize_url(url_value)
    if not clean:
        return set()

    values = {clean}
    if clean.endswith("/info.json"):
        values.add(clean[: -len("/info.json")])
    if "/full/" in clean:
        values.add(clean.split("/full/", 1)[0].rstrip("/"))
    return {value for value in values if value}


def _canvas_matches_image_id(canvas_item, target_candidates):
    if not isinstance(canvas_item, dict):
        return False

    if isinstance(canvas_item.get("items"), list):
        for anno_page in canvas_item["items"]:
            if not isinstance(anno_page, dict) or not isinstance(anno_page.get("items"), list):
                continue
            for anno in anno_page["items"]:
                if not isinstance(anno, dict):
                    continue
                body = anno.get("body")
                body_items = body if isinstance(body, list) else [body]
                for body_item in body_items:
                    if not isinstance(body_item, dict):
                        continue
                    body_id = body_item.get("id") or body_item.get("@id")
                    if _canonical_candidates(body_id) & target_candidates:
                        return True
                    service = body_item.get("service")
                    service_items = service if isinstance(service, list) else [service]
                    for service_item in service_items:
                        if not isinstance(service_item, dict):
                            continue
                        service_id = service_item.get("id") or service_item.get("@id")
                        if _canonical_candidates(service_id) & target_candidates:
                            return True

    if isinstance(canvas_item.get("images"), list):
        for image in canvas_item["images"]:
            if not isinstance(image, dict):
                continue
            resource = image.get("resource")
            if not isinstance(resource, dict):
                continue
            resource_id = resource.get("id") or resource.get("@id")
            if _canonical_candidates(resource_id) & target_candidates:
                return True
            service = resource.get("service")
            service_items = service if isinstance(service, list) else [service]
            for service_item in service_items:
                if not isinstance(service_item, dict):
                    continue
                service_id = service_item.get("id") or service_item.get("@id")
                if _canonical_candidates(service_id) & target_candidates:
                    return True

    return False


def canvaslabel_for_imageid(manifest_json, image_id):
    """Return a canvas label for an image id."""
    target_candidates = _canonical_candidates(image_id)
    if not target_candidates:
        return ""

    manifest_dict = _manifest_dict_from_input(manifest_json)
    if not isinstance(manifest_dict, dict):
        return ""

    canvases = []
    if isinstance(manifest_dict.get("items"), list):
        canvases = manifest_dict["items"]
    elif isinstance(manifest_dict.get("sequences"), list):
        for sequence in manifest_dict["sequences"]:
            if isinstance(sequence, dict) and isinstance(sequence.get("canvases"), list):
                canvases.extend(sequence["canvases"])

    for canvas_item in canvases:
        if _canvas_matches_image_id(canvas_item, target_candidates):
            return _pick_label(canvas_item.get("label"))

    return ""