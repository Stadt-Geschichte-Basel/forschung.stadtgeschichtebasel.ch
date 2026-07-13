"""Tests for the pure helpers in process_data.py.

The module reads required Omeka env vars at import time (require_env), so we set
dummy values before importing it.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("OMEKA_API_URL", "https://example.org/api")
os.environ.setdefault("KEY_IDENTITY", "dummy")
os.environ.setdefault("KEY_CREDENTIAL", "dummy")
os.environ.setdefault("ITEM_SET_ID", "1")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "workflows"))

import process_data as p  # noqa: E402


def test_is_valid_url():
    assert p.is_valid_url("https://omeka.unibe.ch/files/x.jpg")
    assert not p.is_valid_url("not-a-url")
    assert not p.is_valid_url("")


def test_redact_url_hides_credentials():
    url = "https://x/api/items?key_identity=abc&key_credential=def&page=2"
    redacted = p.redact_url(url)
    assert "abc" not in redacted
    assert "def" not in redacted
    assert "page=2" in redacted


def test_normalize_objectid_falls_back():
    assert p.normalize_objectid("abb123", "sgb", 7) == "abb123"
    assert p.normalize_objectid("  ", "sgb", 7) == "sgb7"
    assert p.normalize_objectid(None, "sgb", 7) == "sgb7"


def test_ensure_unique_objectid_dedupes():
    used: set[str] = set()
    assert p.ensure_unique_objectid("a", used, "m") == "a"
    assert p.ensure_unique_objectid("a", used, "m") == "a_m"
    assert p.ensure_unique_objectid("a", used, "m") == "a_m_2"


def test_extract_property_by_id_and_label():
    props = [{"property_id": 1, "@value": "v", "o:label": "L"}]
    assert p.extract_property(props, 1) == "v"
    assert p.extract_property(props, 1, as_label=True) == "L"
    assert p.extract_property(props, 99) == ""


def test_has_meaningful_preview():
    assert p.has_meaningful_preview("objects/real.jpg")
    assert not p.has_meaningful_preview("assets/img/no-image.svg")
    assert not p.has_meaningful_preview("")
    assert not p.has_meaningful_preview(None)


def test_get_media_passes_item_id_as_param(monkeypatch):
    """item_id must go in params, not the URL query (httpx2 drops query on params)."""
    captured = {}

    def fake_get_paginated_items(url, params):
        captured["url"] = url
        captured["params"] = params
        return []

    monkeypatch.setattr(p, "get_paginated_items", fake_get_paginated_items)
    p.get_media(99)
    assert captured["params"]["item_id"] == 99
    assert "?" not in captured["url"]  # no query string for httpx2 to replace


def test_apply_media_preview():
    placeholder = {"image_thumb": "assets/img/no-image.svg"}
    real_child = {
        "image_thumb": "objects/real.jpg",
        "image_small": "objects/real.jpg",
        "format": "image/jpeg",
        "image_alt_text": "a photo",
    }

    # Keeps an already-meaningful parent preview untouched.
    parent = {"image_thumb": "objects/parent.jpg", "image_small": "objects/parent.jpg"}
    assert p.apply_media_preview(dict(parent), [real_child])["image_thumb"] == (
        "objects/parent.jpg"
    )

    # Picks the first meaningful image-media child over a placeholder parent.
    result = p.apply_media_preview(dict(placeholder), [placeholder, real_child])
    assert result["image_thumb"] == "objects/real.jpg"
    assert result["image_alt_text"] == "a photo"

    # Unchanged when no child has a valid preview.
    result = p.apply_media_preview(dict(placeholder), [dict(placeholder)])
    assert result["image_thumb"] == "assets/img/no-image.svg"


def test_download_thumbnail_skips_on_error(monkeypatch):
    """A failed download must return "" instead of raising (mtwente's crash)."""
    import httpx2

    def boom(*_args, **_kwargs):
        raise httpx2.ConnectError("connection refused")

    monkeypatch.setattr(p, "download_file", boom)
    # use a URL whose basename file does not already exist locally
    assert (
        p.download_thumbnail("https://dead.invalid/files/large/zzz-nonexistent.jpg")
        == ""
    )
