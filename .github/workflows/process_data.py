import json
import logging
import os
import re
import unicodedata
from typing import Any, TypeAlias, cast
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import httpx2
import pandas as pd

JsonObject: TypeAlias = dict[str, Any]
Record: TypeAlias = dict[str, Any]
RequestParamValue: TypeAlias = str | bytes | int | float | None
RequestParams: TypeAlias = dict[str, RequestParamValue]


def require_env(name: str) -> str:
    """Return a required environment variable or fail before processing starts."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} environment variable must be set")
    return value


# Configuration
OMEKA_API_URL = f"{require_env('OMEKA_API_URL').rstrip('/')}/"
KEY_IDENTITY = require_env("KEY_IDENTITY")
KEY_CREDENTIAL = require_env("KEY_CREDENTIAL")
ITEM_SET_ID_RAW = require_env("ITEM_SET_ID")
try:
    ITEM_SET_ID = int(ITEM_SET_ID_RAW)
except ValueError:
    raise ValueError("ITEM_SET_ID must be a valid integer") from None
CSV_PATH = os.getenv("CSV_PATH", "_data/sgb-metadata-csv.csv")
JSON_PATH = os.getenv("JSON_PATH", "_data/sgb-metadata-json.json")
VALIDATION_REPORT_PATH = os.getenv("VALIDATION_REPORT_PATH")
FAIL_ON_LITERAL_URLS = os.getenv("FAIL_ON_LITERAL_URLS", "").lower() in {
    "1",
    "true",
    "yes",
}
PLACEHOLDER_IMAGE_PATHS = {
    "assets/img/no-image.svg",
    "assets/img/placeholder.svg",
}
PLACEHOLDER_SOURCE_MARKER = "platzhalter"
URL_IN_LITERAL_PATTERN = re.compile(r"\b(?:https?://|www\.)\S+", re.IGNORECASE)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# --- Helper Functions for Data Extraction ---
def is_valid_url(url: str) -> bool:
    """Checks if a URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def redact_url(url: str) -> str:
    """Redacts Omeka API credentials from URLs before logging or raising errors."""
    parsed_url = urlparse(url)
    query = urlencode(
        [
            (
                key,
                "[redacted]" if key in {"key_identity", "key_credential"} else value,
            )
            for key, value in parse_qsl(parsed_url.query, keep_blank_values=True)
        ]
    )
    return urlunparse(parsed_url._replace(query=query))


def download_file(url: str, dest_path: str, retries: int = 3) -> None:
    """Downloads a file from a URL to dest_path, retrying transient errors."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    for attempt in range(1, retries + 1):
        try:
            with httpx2.stream("GET", url, timeout=30, follow_redirects=True) as r:
                r.raise_for_status()
                with open(dest_path, "wb") as f:
                    for chunk in r.iter_bytes(8192):
                        f.write(chunk)
            return
        except httpx2.HTTPError as err:
            # ponytail: small fixed retry loop for transient errors, no backoff lib
            logging.error(
                "File download error (attempt %d/%d): %s", attempt, retries, err
            )
            if os.path.exists(dest_path):
                os.remove(dest_path)  # drop any partial write before retry/skip
            if attempt == retries:
                raise


def get_paginated_items(
    url: str | None, params: RequestParams | None
) -> list[JsonObject]:
    """Fetches all items from a paginated API endpoint."""
    items = []
    while url:
        try:
            # Add timeout to prevent hanging on slow/unresponsive servers
            response = httpx2.get(url, params=params, timeout=30, follow_redirects=True)
            response.raise_for_status()
            items.extend(cast(list[JsonObject], response.json()))
        except (httpx2.HTTPError, json.JSONDecodeError):
            safe_url = redact_url(url)
            logging.exception("Error fetching items from %s", safe_url)
            raise RuntimeError(f"Error fetching items from {safe_url}") from None
        next_url = response.links.get("next", {}).get("url")
        url = next_url if isinstance(next_url, str) else None
        params = None

    return items


def get_items_from_collection(collection_id: int) -> list[JsonObject]:
    """Fetches all items from a specified collection."""
    params = {
        "item_set_id": collection_id,
        "key_identity": KEY_IDENTITY,
        "key_credential": KEY_CREDENTIAL,
        "per_page": 100,
    }
    return get_paginated_items(urljoin(OMEKA_API_URL, "items"), params)


def get_media(item_id: int | str) -> list[JsonObject]:
    """Fetches media associated with a specific item ID."""
    # item_id must go in params, not the URL query: httpx2 replaces an existing
    # query string when params is passed (requests merged it), which would drop
    # the filter and fetch every media object on the server.
    params = {
        "item_id": item_id,
        "key_identity": KEY_IDENTITY,
        "key_credential": KEY_CREDENTIAL,
    }
    return get_paginated_items(urljoin(OMEKA_API_URL, "media"), params)


# --- Data Extraction and Transformation Functions ---
def extract_property(
    props: list[JsonObject], prop_id: int, as_label: bool = False
) -> str:
    """Extracts a property value or label from properties based on property ID."""
    for prop in props:
        if prop.get("property_id") == prop_id:
            if as_label:
                return prop.get("o:label", "")
            return prop.get("@value", "")
    return ""


def extract_property_by_term(
    props: list[JsonObject], term: str, as_uri: bool = False
) -> str:
    """Extracts a property value or URI from properties list."""
    # Since props is already a list of values for dcterms:abstract,
    # we just need to extract the first available value
    for prop in props:
        if as_uri:
            return f"[{prop.get('o:label', '')}]({prop.get('@id', '')})"
        return prop.get("@value", "")
    return ""


def extract_combined_values(props: list[JsonObject]) -> list[str]:
    """Combines text values and URIs from properties into a single list."""
    values = [
        prop.get("@value", "").replace(";", "&#59")
        for prop in props
        if "@value" in prop
    ]
    uris = [
        f"[{prop.get('o:label', '').replace(';', '&#59')}]({prop.get('@id', '').replace(';', '&#59')})"
        for prop in props
        if "@id" in prop
    ]
    return values + uris


def extract_alt_text(item_or_media: JsonObject) -> str:
    """Extracts alt text from dcterms:abstract field, with fallback to o:alt_text."""
    # First try to get dcterms:abstract (the new alt attribute field)
    abstract_props = item_or_media.get("dcterms:abstract", [])
    if abstract_props:
        alt_text = extract_property_by_term(abstract_props, "abstract")
        if alt_text:
            return alt_text

    # Fallback to the old o:alt_text field for backward compatibility
    return item_or_media.get("o:alt_text", "")


def extract_combined_values_csv(props: list[JsonObject]) -> str:
    """Combines text values and URIs into a semicolon-separated string."""
    combined = extract_combined_values(props)
    return ";".join(combined)


def truncate_for_report(value: str, max_length: int = 90) -> str:
    """Normalizes and truncates a value for concise validation logs."""
    value = " ".join(value.split())
    if len(value) <= max_length:
        return value
    return f"{value[: max_length - 3]}..."


def find_literal_url_issues(resource: JsonObject, resource_type: str) -> list[str]:
    """Finds Omeka literal values that contain URLs and should be URI values."""
    issues = []
    resource_id = resource.get("o:id", "unknown")
    for term, props in resource.items():
        if not isinstance(props, list):
            continue
        for index, prop in enumerate(props):
            if not isinstance(prop, dict):
                continue
            value = prop.get("@value")
            if isinstance(value, str) and URL_IN_LITERAL_PATTERN.search(value):
                issues.append(
                    f"[{resource_type} {resource_id}] {term}[{index}]: "
                    f"Literal field contains URL: {truncate_for_report(value)}"
                )
    return issues


def report_literal_url_issues(issues: list[str]) -> None:
    """Logs literal URL validation issues and optionally writes a report file."""
    if not issues:
        # Clear a stale report from a previous run so downstream cleanup doesn't
        # act on outdated data.
        if VALIDATION_REPORT_PATH and os.path.exists(VALIDATION_REPORT_PATH):
            os.remove(VALIDATION_REPORT_PATH)
        return

    logging.warning(
        "%s literal metadata value(s) contain URLs. "
        "Move URLs into Omeka URI values with labels to avoid broken rendering.",
        len(issues),
    )
    for issue in issues:
        logging.warning(issue)

    if VALIDATION_REPORT_PATH:
        report_dir = os.path.dirname(VALIDATION_REPORT_PATH)
        if report_dir:
            os.makedirs(report_dir, exist_ok=True)
        with open(VALIDATION_REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(issues))
            f.write("\n")
        logging.warning("Validation report saved to %s", VALIDATION_REPORT_PATH)

    if FAIL_ON_LITERAL_URLS:
        raise ValueError(
            f"Found {len(issues)} literal metadata value(s) containing URLs"
        )


def download_thumbnail(image_url: str) -> str:
    """Downloads the thumbnail image if the URL is valid."""
    if image_url and is_valid_url(image_url):
        filename = os.path.basename(image_url)
        local_image_path = f"objects/{filename}"
        if not os.path.exists(local_image_path):
            try:
                download_file(image_url, local_image_path)
            except httpx2.HTTPError as err:
                # A single unreachable file must not abort the whole export.
                logging.warning("Skipping thumbnail %s: %s", redact_url(image_url), err)
                return ""
        return local_image_path
    return ""


def has_meaningful_preview(image_path: object) -> bool:
    """Returns whether an image path points to a non-placeholder preview."""
    return (
        isinstance(image_path, str)
        and bool(image_path)
        and image_path not in PLACEHOLDER_IMAGE_PATHS
    )


def normalize_objectid(objectid: object, prefix: str, source_id: object) -> str:
    """Returns a stable object identifier with a fallback for missing values."""
    normalized_objectid = str(objectid or "").strip()
    return normalized_objectid or f"{prefix}{source_id}"


def ensure_unique_objectid(
    objectid: str, used_objectids: set[str], suffix: object
) -> str:
    """Ensures that each exported record has a unique object identifier."""
    if objectid not in used_objectids:
        used_objectids.add(objectid)
        return objectid

    candidate = f"{objectid}_{suffix}"
    counter = 2
    while candidate in used_objectids:
        candidate = f"{objectid}_{suffix}_{counter}"
        counter += 1

    logging.warning(
        "Duplicate objectid '%s' detected. Exporting record as '%s'.",
        objectid,
        candidate,
    )
    used_objectids.add(candidate)
    return candidate


def apply_media_preview(item_record: Record, media_records: list[Record]) -> Record:
    """Uses the first meaningful child preview for a parent item when needed."""
    if has_meaningful_preview(item_record.get("image_thumb")) or has_meaningful_preview(
        item_record.get("image_small")
    ):
        return item_record

    def find_first_valid_preview_record(records: list[Record]) -> Record | None:
        for media_record in records:
            media_preview = media_record.get("image_thumb") or media_record.get(
                "image_small"
            )
            if has_meaningful_preview(media_preview):
                return media_record
        return None

    image_media_records = []
    for media_record in media_records:
        format_value = media_record.get("format", "")
        format_text = format_value if isinstance(format_value, str) else ""
        if media_record.get(
            "display_template"
        ) == "image" or format_text.lower().startswith("image/"):
            image_media_records.append(media_record)

    preview_record = find_first_valid_preview_record(
        image_media_records
    ) or find_first_valid_preview_record(media_records)
    if not preview_record:
        return item_record

    item_record["image_thumb"] = preview_record.get(
        "image_thumb"
    ) or preview_record.get("image_small")
    item_record["image_small"] = preview_record.get(
        "image_small"
    ) or preview_record.get("image_thumb")
    if preview_record.get("image_alt_text"):
        item_record["image_alt_text"] = preview_record["image_alt_text"]

    return item_record


def infer_display_template(format_value: str) -> str:
    """Infers the display template type based on the format value."""
    if "image" in format_value.lower():
        return "image"
    elif "pdf" in format_value.lower():
        return "pdf"
    elif "geo+json" in format_value.lower():
        return "geodata"
    else:
        return "record"


def extract_item_data(item: JsonObject) -> Record:
    """Extracts relevant data from an item and downloads its thumbnail if available."""
    local_image_path = (
        download_thumbnail(item.get("thumbnail_display_urls", {}).get("large", ""))
        if item.get("o:is_public", False)
        else "assets/img/placeholder.svg"
    )

    return {
        "objectid": extract_property(item.get("dcterms:identifier", []), 10),
        "parentid": "",
        "title": extract_property(item.get("dcterms:title", []), 1),
        "description": extract_property(item.get("dcterms:description", []), 4),
        # "subject": extract_combined_values(item.get("dcterms:subject", [])),
        "coverage": extract_property(item.get("dcterms:temporal", []), 41),
        "isPartOf": extract_combined_values(item.get("dcterms:isPartOf", [])),
        "creator": extract_combined_values(item.get("dcterms:creator", [])),
        "publisher": extract_combined_values(item.get("dcterms:publisher", [])),
        "source": extract_combined_values(item.get("dcterms:source", [])),
        "date": extract_property(item.get("dcterms:date", []), 7),
        "type": extract_property(item.get("dcterms:type", []), 8, as_label=True),
        "format": extract_property(item.get("dcterms:format", []), 9),
        "extent": extract_property(item.get("dcterms:extent", []), 25),
        "language": extract_property(item.get("dcterms:language", []), 12),
        "relation": extract_combined_values(item.get("dcterms:relation", [])),
        "rights": extract_property(item.get("dcterms:rights", []), 15),
        "license": extract_property(item.get("dcterms:license", []), 49),
        "display_template": "compound_object",
        "object_location": "",
        "image_small": local_image_path,
        "image_thumb": local_image_path,
        "image_alt_text": extract_alt_text(item),
    }


def extract_media_data(media: JsonObject, item_dc_identifier: str) -> Record:
    """Extracts relevant data from a media item associated with a specific item."""
    format_value = extract_property(media.get("dcterms:format", []), 9)
    display_template = infer_display_template(format_value)
    media_source = str(media.get("o:source", "")).lower()

    # Download the thumbnail image if available and valid
    if "application/geo+json" in format_value:
        local_image_path = "assets/lib/icons/sgb-globe.svg"
    elif "text/csv" in format_value:
        local_image_path = "assets/lib/icons/table.svg"
    else:
        local_image_path = download_thumbnail(
            media.get("thumbnail_display_urls", {}).get("large", "")
        )
        original_url = media.get("o:original_url", "")
        if (
            not local_image_path
            and media.get("o:is_public", False)
            and isinstance(original_url, str)
            and format_value.lower().startswith("image/")
            and is_valid_url(original_url)
        ):
            local_image_path = original_url
        if not local_image_path:
            local_image_path = (
                "assets/img/placeholder.svg"
                if PLACEHOLDER_SOURCE_MARKER in media_source
                else "assets/img/no-image.svg"
            )

    # Extract media data
    object_location = (
        media.get("o:original_url", "") if media.get("o:is_public", False) else ""
    )

    logging.info(f"Media ID: {media['o:id']}")
    logging.info(f"is_public: {media.get('o:is_public')}")

    return {
        "objectid": extract_property(media.get("dcterms:identifier", []), 10),
        "parentid": item_dc_identifier,
        "title": extract_property(media.get("dcterms:title", []), 1),
        "description": extract_property(media.get("dcterms:description", []), 4),
        # "subject": extract_combined_values(media.get("dcterms:subject", [])),
        "coverage": extract_property(media.get("dcterms:temporal", []), 41),
        "isPartOf": extract_combined_values(media.get("dcterms:isPartOf", [])),
        "creator": extract_combined_values(media.get("dcterms:creator", [])),
        "publisher": extract_combined_values(media.get("dcterms:publisher", [])),
        "source": extract_combined_values(media.get("dcterms:source", [])),
        "date": extract_property(media.get("dcterms:date", []), 7),
        "type": extract_property(media.get("dcterms:type", []), 8, as_label=True),
        "format": format_value,
        "extent": extract_property(media.get("dcterms:extent", []), 25),
        "language": extract_property(media.get("dcterms:language", []), 12),
        "relation": extract_combined_values(media.get("dcterms:relation", [])),
        "rights": extract_property(media.get("dcterms:rights", []), 15),
        "license": extract_property(media.get("dcterms:license", []), 49),
        "display_template": display_template,
        "object_location": object_location,
        "image_small": local_image_path,
        "image_thumb": local_image_path,
        "image_alt_text": extract_alt_text(media),
    }


def normalize_record(record: Record) -> Record:
    """Normalizes all string fields in a record to Unicode NFC form."""
    return {
        key: unicodedata.normalize("NFC", value) if isinstance(value, str) else value
        for key, value in record.items()
    }


# --- Main Processing Function ---
def main() -> None:
    # Fetch item data
    logging.info(f"Fetching items from collection {ITEM_SET_ID} at {OMEKA_API_URL}")
    items_data = get_items_from_collection(ITEM_SET_ID)

    # Validate that we received some data
    if not items_data:
        logging.error(
            "No items received from Omeka API. This could indicate a timeout or API unavailability."
        )
        logging.error("Canceling deployment to prevent deploying empty site.")
        raise ValueError("No items received from Omeka API")

    logging.info(f"Successfully retrieved {len(items_data)} items from collection")

    # Process each item and associated media
    items_processed = []
    literal_url_issues = []
    seen_parent_objectids: set[str] = set()
    used_objectids: set[str] = set()
    for item in items_data:
        item_record = extract_item_data(item)
        item_record["objectid"] = normalize_objectid(
            item_record.get("objectid"), "item-", item.get("o:id", "unknown")
        )
        item_objectid = item_record["objectid"]
        if item_objectid in seen_parent_objectids:
            logging.warning(
                "Skipping duplicate parent objectid '%s' from Omeka item %s.",
                item_objectid,
                item.get("o:id", "unknown"),
            )
            continue

        literal_url_issues.extend(find_literal_url_issues(item, "Item"))
        seen_parent_objectids.add(item_objectid)
        used_objectids.add(item_objectid)
        media_data = get_media(item.get("o:id", ""))
        media_records = []
        if media_data:
            for media in media_data:
                literal_url_issues.extend(find_literal_url_issues(media, "Media"))
                media_record = extract_media_data(media, item_objectid)
                media_record["objectid"] = ensure_unique_objectid(
                    normalize_objectid(
                        media_record.get("objectid"),
                        "media-",
                        media.get("o:id", "unknown"),
                    ),
                    used_objectids,
                    media.get("o:id", "unknown"),
                )
                media_records.append(media_record)

        item_record = apply_media_preview(item_record, media_records)
        items_processed.append(item_record)
        items_processed.extend(media_records)

    report_literal_url_issues(literal_url_issues)

    # Normalize all string fields in the records to avoid decomposed Unicode form Umlaute ¨ + o -> ö
    items_normalized = [normalize_record(record) for record in items_processed]

    # Final validation - ensure we have processed records
    if not items_normalized:
        logging.error("No records were processed successfully. Canceling deployment.")
        raise ValueError("No records were processed successfully")

    # Save data to CSV and JSON formats
    save_to_files(items_normalized, CSV_PATH, JSON_PATH)


def save_to_files(records: list[Record], csv_path: str, json_path: str) -> None:
    """Saves data to both CSV and JSON files."""
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False)
    logging.info(f"JSON file has been saved to {json_path}")

    # Convert list of records to a DataFrame and save as CSV
    records = [
        {
            key: ";".join(value) if isinstance(value, list) else value
            for key, value in record.items()
        }
        for record in records
    ]
    df = pd.DataFrame(records)
    df.to_csv(csv_path, index=False)
    logging.info(f"CSV file has been saved to {csv_path}")


if __name__ == "__main__":
    main()
