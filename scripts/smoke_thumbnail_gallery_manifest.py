import json
import tempfile
from pathlib import Path

from iiif_anywidget.iiifutils import Manifest, canvaslabel_for_imageid
from iiif_anywidget.thumbnail_gallery import IIIFThumbnailGallery


def main():
    manifest_payload = {
        "@context": "http://iiif.io/api/presentation/3/context.json",
        "id": "https://example.org/manifest/1",
        "type": "Manifest",
        "items": [
            {
                "id": "https://example.org/canvas/1",
                "type": "Canvas",
                "label": {"en": ["Page 1"]},
                "items": [
                    {
                        "id": "https://example.org/page/1",
                        "type": "AnnotationPage",
                        "items": [
                            {
                                "id": "https://example.org/annotation/1",
                                "type": "Annotation",
                                "motivation": "painting",
                                "body": {
                                    "id": "https://example.org/iiif/image-1/full/1200,/0/default.jpg",
                                    "type": "Image",
                                    "format": "image/jpeg",
                                },
                                "target": "https://example.org/canvas/1",
                            }
                        ],
                    }
                ],
            }
        ],
    }

    manifest_payload_v2 = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": "https://example.org/manifest/v2",
        "@type": "sc:Manifest",
        "sequences": [
            {
                "@type": "sc:Sequence",
                "canvases": [
                    {
                        "@id": "https://example.org/canvas/v2/1",
                        "@type": "sc:Canvas",
                        "label": "V2 Page 1",
                        "images": [
                            {
                                "@type": "oa:Annotation",
                                "resource": {
                                    "@id": "https://example.org/iiif/v2-image-1/full/full/0/default.jpg",
                                    "@type": "dctypes:Image",
                                    "service": {
                                        "@id": "https://example.org/iiif/v2-image-1",
                                        "profile": "http://iiif.io/api/image/2/level2.json",
                                    },
                                },
                            }
                        ],
                    }
                ],
            }
        ],
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        manifest_path = Path(temp_dir) / "manifest.json"
        manifest_path.write_text(json.dumps(manifest_payload), encoding="utf-8")
        manifest_url = manifest_path.as_uri()

        gallery = IIIFThumbnailGallery(manifest_url=manifest_url)
        items = json.loads(gallery.items_json)

        assert isinstance(gallery.manifest, Manifest)
        assert gallery.manifest.source_url == manifest_url
        assert isinstance(gallery.manifest.manifest_json, dict)
        assert len(gallery.manifest.manifest_json.get("items", [])) == 1
        assert len(items) == 1
        assert items[0].get("info_url") == "https://example.org/iiif/image-1/info.json"
        assert gallery.selected_info_url == "https://example.org/iiif/image-1/info.json"
        assert gallery.manifest_error == ""

        label_from_raw_manifest = canvaslabel_for_imageid(
            manifest_payload,
            "https://example.org/iiif/image-1/full/1200,/0/default.jpg",
        )
        label_from_synced_payload = canvaslabel_for_imageid(
            gallery.manifest.to_dict(),
            "https://example.org/iiif/image-1/info.json",
        )
        label_from_manifest_obj = canvaslabel_for_imageid(
            gallery.manifest,
            "https://example.org/iiif/image-1",
        )

        assert label_from_raw_manifest == "Page 1"
        assert label_from_synced_payload == "Page 1"
        assert label_from_manifest_obj == "Page 1"

        label_from_v2_manifest = canvaslabel_for_imageid(
            manifest_payload_v2,
            "https://example.org/iiif/v2-image-1/info.json",
        )
        assert label_from_v2_manifest == "V2 Page 1"

    print("Smoke test passed: manifest sync, thumbnail extraction, and canvas label lookup are working for IIIF v2 and v3.")


if __name__ == "__main__":
    main()
