from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from pathlib import Path
import re
import tempfile

import requests

S2_API_BASE = "https://api.semanticscholar.org/graph/v1/paper"
S2_FIELDS = "title,authors,abstract,year,venue,publicationDate,externalIds"
S2_TIMEOUT = 5
DOI_PATTERN = re.compile(r"10\.\d{4,9}/[^\s?#]+")


def detect_doi(url: str) -> str | None:
    match = DOI_PATTERN.search(url)
    if match:
        return match.group(0).rstrip(".,;:)")
    return None


def source_id_from_doi(doi: str) -> str:
    return "doi-" + doi.replace("/", "-")


def source_id_from_path(path: Path) -> str:
    path_hash = hashlib.sha256(str(path.resolve()).encode()).hexdigest()[:12]
    return f"file-{path_hash}"


def source_id_from_url(url: str) -> str:
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:12]
    return f"web-{url_hash}"


def detect_source_type(url: str | None, path: Path | None, doi: str | None) -> str:
    if doi:
        return "paper"
    if path and str(path).lower().endswith(".pdf"):
        return "paper"
    if url and url.lower().split("?")[0].endswith(".pdf"):
        return "paper"
    return "article"


def fetch_semantic_scholar(doi: str) -> dict | None:
    try:
        response = requests.get(
            f"{S2_API_BASE}/DOI:{doi}",
            params={"fields": S2_FIELDS},
            timeout=S2_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def extract_pdf(path: Path) -> dict:
    import pymupdf4llm

    pages = pymupdf4llm.to_markdown(
        str(path),
        page_chunks=True,
        force_text=True,
        table_strategy="lines",
    )
    if isinstance(pages, list):
        content = "\n\n".join(
            page["text"] if isinstance(page, dict) else str(page) for page in pages
        )
    else:
        content = str(pages)
    return {"content": content, "word_count": len(content.split())}


def extract_web(url: str) -> dict:
    import trafilatura

    html = trafilatura.fetch_url(url)
    if not html:
        raise ValueError(f"Failed to fetch URL: {url}")

    content = trafilatura.extract(
        html,
        output_format="markdown",
        with_metadata=True,
        favor_recall=True,
        include_tables=True,
    )
    if not content:
        raise ValueError(f"Failed to extract content from: {url}")

    metadata = trafilatura.extract_metadata(html)
    result = {"content": content, "word_count": len(content.split())}
    if metadata:
        result["title"] = metadata.title or ""
        result["authors"] = (
            [author.strip() for author in metadata.author.split(";") if author.strip()]
            if metadata.author
            else []
        )
        result["description"] = metadata.description or ""
        result["published"] = metadata.date or ""
        result["sitename"] = metadata.sitename or ""
    return result


def fetch_article(
    url: str | None = None,
    path: Path | None = None,
    doi: str | None = None,
) -> dict:
    if not url and not path:
        raise ValueError("Either url or path is required")
    if not doi and url:
        doi = detect_doi(url)

    source_type = detect_source_type(url, path, doi)
    result = {
        "source_type": source_type,
        "url": url or "",
        "doi": doi or "",
        "title": "",
        "authors": [],
        "description": "",
        "venue": "",
        "published": "",
        "content": "",
        "word_count": 0,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }

    if doi:
        s2_data = fetch_semantic_scholar(doi)
        if s2_data:
            result["title"] = s2_data.get("title", "")
            result["authors"] = [
                author.get("name", "") for author in s2_data.get("authors", [])
            ]
            result["description"] = s2_data.get("abstract", "") or ""
            result["venue"] = s2_data.get("venue", "") or ""
            result["published"] = s2_data.get("publicationDate", "") or ""

    if source_type == "paper":
        pdf_path = path
        temp_dir: str | None = None

        if pdf_path and not pdf_path.exists():
            raise ValueError(f"File not found: {pdf_path}")
        if not pdf_path and url:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            temp_dir = tempfile.mkdtemp()
            pdf_path = Path(temp_dir) / "download.pdf"
            pdf_path.write_bytes(response.content)
        if not pdf_path:
            raise ValueError("No PDF path available")

        try:
            extracted = extract_pdf(pdf_path)
        finally:
            if temp_dir:
                import shutil

                shutil.rmtree(temp_dir, ignore_errors=True)

        result["content"] = extracted["content"]
        result["word_count"] = extracted["word_count"]
    else:
        if not url:
            raise ValueError("URL is required for web article extraction")
        extracted = extract_web(url)
        result["content"] = extracted["content"]
        result["word_count"] = extracted["word_count"]
        if not result["title"]:
            result["title"] = extracted.get("title", "")
        if not result["authors"]:
            result["authors"] = extracted.get("authors", [])
        if not result["description"]:
            result["description"] = extracted.get("description", "")
        if not result["published"]:
            result["published"] = extracted.get("published", "")

    if doi:
        result["source_id"] = source_id_from_doi(doi)
    elif path:
        result["source_id"] = source_id_from_path(path)
    else:
        result["source_id"] = source_id_from_url(url)

    return result
