"""Tests for the pure helpers in process_data.py.

The module reads required Omeka env vars at import time (require_env), so we set
dummy values before importing it.
"""

import os
import sys
from pathlib import Path

import pytest

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


def test_legacy_subject_is_not_exported(monkeypatch):
    """Legacy Omeka dcterms:subject values must not reach the exported records."""
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "")
    subject = [{"property_id": 3, "@value": "Legacy subject", "type": "literal"}]
    item = {"o:id": 1, "o:is_public": True, "dcterms:subject": subject}
    media = {"o:id": 2, "o:is_public": True, "dcterms:subject": subject}

    for record in (p.extract_item_data(item), p.extract_media_data(media, "abb1")):
        assert "subject" not in record
        assert "Legacy subject" not in str(record)


def test_private_media_has_no_file_location(monkeypatch):
    """Private media keep a thumbnail but export no original file URL."""
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "objects/thumb.jpg")
    media = {
        "o:id": 2,
        "o:is_public": False,
        "dcterms:format": [
            {"property_id": 9, "@value": "image/png", "type": "literal"}
        ],
        "o:original_url": "https://omeka.unibe.ch/files/original/abc.png",
    }
    record = p.extract_media_data(media, "abb1")
    assert record["object_location"] == ""
    assert record["image_thumb"] == "objects/thumb.jpg"


def test_original_url_preview_skips_tiff(monkeypatch):
    """Omeka made no thumbnail: a TIFF file must not become the preview.

    The published data has TIFF files labeled image/jpeg, so the file name decides.
    """
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "")

    def record(filename: str, mime: str) -> dict:
        media = {
            "o:id": 2,
            "o:is_public": True,
            "dcterms:format": [{"property_id": 9, "@value": mime, "type": "literal"}],
            "o:original_url": f"https://omeka.unibe.ch/files/original/{filename}",
        }
        return p.extract_media_data(media, "abb1")

    assert record("abc.tif", "image/tiff")["image_thumb"] == "assets/img/no-image.svg"
    assert record("abc.TIFF", "image/jpeg")["image_thumb"] == "assets/img/no-image.svg"
    assert record("abc.jpg", "image/jpeg")["image_thumb"].endswith("/abc.jpg")


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


PLACEHOLDER_SHA = next(iter(p.PLACEHOLDER_SHA256))


def media_record(**fields: object) -> dict:
    media = {
        "o:id": 2,
        "o:is_public": True,
        "dcterms:format": [
            {"property_id": 9, "@value": "image/png", "type": "literal"}
        ],
        "o:original_url": "https://omeka.unibe.ch/files/original/abc.png",
        "o:source": "abc.png",
        "o:filename": "abc.png",
        "o:sha256": "0" * 64,
    }
    media.update(fields)
    return media


@pytest.mark.parametrize(
    "fields",
    [
        {"o:source": "sgb-fdp-platzhalter[1].png"},
        {"o:filename": "sgb-fdp-Platzhalter.png"},
        {"o:sha256": PLACEHOLDER_SHA},
    ],
    ids=["source", "filename", "checksum"],
)
def test_public_placeholder_has_no_file_location(monkeypatch, fields):
    """A public placeholder keeps its preview but exports no file location."""
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "objects/thumb.jpg")
    record = p.extract_media_data(media_record(**fields), "abb1")
    assert p.is_placeholder(media_record(**fields))
    assert record["object_location"] == ""
    assert record["image_thumb"] == "objects/thumb.jpg"


def test_placeholder_without_thumbnail_uses_placeholder_icon(monkeypatch):
    """No thumbnail: the placeholder original must not become the preview."""
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "")
    record = p.extract_media_data(media_record(**{"o:sha256": PLACEHOLDER_SHA}), "x")
    assert record["image_thumb"] == "assets/img/placeholder.svg"
    assert record["object_location"] == ""


def test_private_media_without_thumbnail_does_not_use_original(monkeypatch):
    """No thumbnail: the private original must not become the preview."""
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "")
    record = p.extract_media_data(media_record(**{"o:is_public": False}), "abb1")
    assert record["image_thumb"] == "assets/img/no-image.svg"
    assert "files/original" not in str(record)


def test_public_media_with_real_file_has_file_location(monkeypatch):
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "objects/thumb.jpg")
    record = p.extract_media_data(media_record(), "abb1")
    assert record["object_location"] == "https://omeka.unibe.ch/files/original/abc.png"


def test_media_without_visibility_flag_has_no_file_location(monkeypatch):
    """A missing o:is_public counts as private."""
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "objects/thumb.jpg")
    media = media_record()
    del media["o:is_public"]
    assert p.extract_media_data(media, "abb1")["object_location"] == ""


def test_private_values_are_not_exported(monkeypatch):
    """The export reads with an API key. Private values must not reach the site."""
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "objects/thumb.jpg")
    secret = [
        {"property_id": 4, "@value": "Interne Notiz", "is_public": False},
        {"property_id": 4, "@value": "Öffentlich", "is_public": True},
    ]
    item = {"o:id": 1, "o:is_public": True, "dcterms:description": secret}
    media = media_record(**{"dcterms:description": secret})
    for record in (p.extract_item_data(item), p.extract_media_data(media, "abb1")):
        assert "Interne Notiz" not in str(record)
        assert record["description"] == "Öffentlich"
    issues = p.find_literal_url_issues(
        {
            "o:id": 1,
            "dcterms:rights": [
                {"@value": "https://x", "is_public": False},
                {"@value": "https://y"},
            ],
        },
        "Item",
    )
    assert len(issues) == 1
    assert "dcterms:rights[1]" in issues[0] and "https://x" not in issues[0]


def test_public_item_with_private_and_public_children(monkeypatch, tmp_path):
    """A mixed compound item exports a file location only for public originals."""
    monkeypatch.setattr(p, "download_thumbnail", lambda _url: "objects/thumb.jpg")
    item = {"o:id": 1, "o:is_public": True}
    children = [
        media_record(
            **{"o:id": 2, "o:original_url": "https://o/files/original/pub.png"}
        ),
        media_record(
            **{
                "o:id": 3,
                "o:is_public": False,
                "o:original_url": "https://o/files/original/priv.png",
            }
        ),
        media_record(
            **{
                "o:id": 4,
                "o:sha256": PLACEHOLDER_SHA,
                "o:original_url": "https://o/files/original/ph.png",
            }
        ),
    ]
    records = [p.extract_item_data(item)]
    records += [p.extract_media_data(m, "abb1") for m in children]
    locations = [r["object_location"] for r in records]
    assert locations == ["", "https://o/files/original/pub.png", "", ""]

    json_path, csv_path = tmp_path / "m.json", tmp_path / "m.csv"
    p.save_to_files(records, str(csv_path), str(json_path))
    exported = json_path.read_text() + csv_path.read_text()
    assert "priv.png" not in exported
    assert "ph.png" not in exported
    assert "pub.png" in exported
