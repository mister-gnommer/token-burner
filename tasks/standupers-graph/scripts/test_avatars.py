import hashlib
import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from avatars import prepare_avatar
from graph_pipeline import d2_source

PERFORMER = {"id": "lorem", "name": "Lorem", "profile_url": "https://example.invalid/people/lorem", "image_url": "/avatars/lorem.webp"}
IMAGE_URL = "https://example.invalid/avatars/lorem.webp"
CACHE_NAME = "avatar-" + hashlib.sha256(IMAGE_URL.encode()).hexdigest()[:20] + ".png"


class AvatarTests(unittest.TestCase):
    def test_download_decodes_webp_and_cache_survives_offline_rendering(self):
        content = BytesIO()
        Image.new("RGB", (220, 180), "#225588").save(content, "WEBP")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch("avatars.urlopen", return_value=BytesIO(content.getvalue())):
                avatar = prepare_avatar(PERFORMER, root)
            assert (avatar["status"], avatar["source_url"], avatar["path"]) == ("photo", IMAGE_URL, f"assets/{CACHE_NAME}")
            with Image.open(root / avatar["path"]) as image:
                assert (image.format, image.size) == ("PNG", (160, 160))
            assert prepare_avatar(PERFORMER, root, fetch=False)["status"] == "photo"

    def test_missing_unreachable_and_invalid_images_use_local_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing = prepare_avatar({"id": "lorem"}, root)
            with patch("avatars.urlopen", side_effect=OSError("Lorem network unavailable")):
                unavailable = prepare_avatar(PERFORMER, root)
            with patch("avatars.urlopen", return_value=BytesIO(b"Lorem ipsum, not an image")):
                invalid = prepare_avatar(PERFORMER, root)
            assert [r["status"] for r in [missing, unavailable, invalid]] == ["placeholder"] * 3
            assert all((root / r["path"]).is_file() for r in [missing, unavailable, invalid])
            assert "Lorem network unavailable" in unavailable["reason"]

    def test_corrupt_cache_and_non_https_urls_do_not_break_rendering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            prepare_avatar({}, root)
            (root / "assets" / CACHE_NAME).write_bytes(b"Lorem damaged cache")
            assert prepare_avatar(PERFORMER, root, fetch=False)["status"] == "placeholder"
            assert prepare_avatar({**PERFORMER, "image_url": "file:///etc/passwd"}, root)["status"] == "placeholder"

    def test_d2_photo_node_keeps_label_outside_image(self):
        graph = {"synthetic": True, "nodes": [{"id": "lorem", "name": "Lorem", "observed_fans": 0, "avatar": {"path": "assets/laughing-person.svg"}}], "relations": [], "evidence_sources": {}}
        source = d2_source(graph)
        assert 'icon: "./assets/laughing-person.svg"' in source
        assert "shape: image" in source and "label.near: outside-bottom-center" in source


if __name__ == "__main__":
    unittest.main()
