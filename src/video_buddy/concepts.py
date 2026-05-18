from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path
import re

FUZZY_THRESHOLD = 0.8


@dataclass(frozen=True, slots=True)
class ConceptSummary:
    created: tuple[str, ...]
    updated: tuple[str, ...]
    tags: tuple[str, ...]


def slugify(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def scan_existing_concepts(concepts_dir: Path) -> dict[str, Path]:
    if not concepts_dir.exists():
        return {}
    concept_pattern = re.compile(r'^concept:\s*"([^"]+)"\s*$', re.MULTILINE)
    existing = {}
    for md_file in concepts_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        match = concept_pattern.search(content)
        if match:
            existing[match.group(1)] = md_file
    return existing


def fuzzy_match(name: str, existing_names: list[str]) -> str | None:
    if not existing_names:
        return None
    name_lower = name.lower()
    for existing in existing_names:
        if existing.lower() == name_lower:
            return existing
    best_match = None
    best_ratio = 0.0
    for existing in existing_names:
        ratio = SequenceMatcher(None, name_lower, existing.lower()).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = existing
    return best_match if best_ratio >= FUZZY_THRESHOLD else None


def process_concepts_file(
    concepts_json_path: Path,
    *,
    concepts_dir: Path,
    source_title: str,
    source_slug: str | None = None,
) -> ConceptSummary:
    extraction = json.loads(concepts_json_path.read_text(encoding="utf-8"))
    concepts = extraction.get("concepts")
    if not isinstance(concepts, list):
        raise RuntimeError("Concept extraction JSON must contain a concepts list")

    concepts_dir.mkdir(parents=True, exist_ok=True)
    existing = scan_existing_concepts(concepts_dir)
    existing_names = list(existing.keys())
    created: list[str] = []
    updated: list[str] = []
    created_date = date.today().isoformat()
    source_ref = (
        f"[{source_title}](../{source_slug}.md)" if source_slug else source_title
    )

    for concept in concepts:
        if not isinstance(concept, dict):
            raise RuntimeError("Each concept entry must be an object")
        name = str(concept.get("name") or "").strip()
        definition = str(concept.get("definition") or "").strip()
        if not name or not definition:
            raise RuntimeError("Each concept requires non-empty name and definition")
        matched_name = fuzzy_match(name, existing_names)
        if matched_name:
            changed = update_concept_note(
                existing[matched_name],
                source_ref=source_ref,
                relevance=str(concept.get("relevance") or "Referenced in source"),
                related_concepts=[
                    str(item) for item in concept.get("related_concepts") or []
                ],
            )
            if changed:
                updated.append(matched_name)
        else:
            note_path = create_concept_note(
                concepts_dir,
                name=name,
                definition=definition,
                related_concepts=[
                    str(item) for item in concept.get("related_concepts") or []
                ],
                source_ref=source_ref,
                relevance=str(concept.get("relevance") or "Referenced in source"),
                created_date=created_date,
            )
            created.append(name)
            existing[name] = note_path
            existing_names.append(name)

    return ConceptSummary(
        tuple(created),
        tuple(updated),
        tuple(str(tag) for tag in extraction.get("tags") or []),
    )


def create_concept_note(
    concepts_dir: Path,
    *,
    name: str,
    definition: str,
    related_concepts: list[str],
    source_ref: str,
    relevance: str,
    created_date: str,
) -> Path:
    slug = slugify(name)
    note_path = concepts_dir / f"{slug}.md"
    related_lines = (
        "".join(
            f"- [{related}]({slugify(related)}.md)\n" for related in related_concepts
        )
        or "<!-- No related concepts yet -->\n"
    )
    content = f'''---
concept: "{name}"
created: "{created_date}"
aliases: []
tags:
  - concept
---

# {name}

## Definition

{definition}

## Related Concepts

{related_lines}## Sources

- {source_ref} - {relevance}
'''
    note_path.write_text(content, encoding="utf-8")
    return note_path


def update_concept_note(
    note_path: Path, *, source_ref: str, relevance: str, related_concepts: list[str]
) -> bool:
    content = note_path.read_text(encoding="utf-8")
    original = content
    if source_ref not in content:
        source_line = f"- {source_ref} - {relevance}\n"
        sources_match = re.search(r"^## Sources\s*\n", content, re.MULTILINE)
        if sources_match:
            insert_pos = _skip_section_comments(content, sources_match.end())
            content = content[:insert_pos] + source_line + content[insert_pos:]
        else:
            content = content.rstrip() + "\n\n## Sources\n\n" + source_line
    if related_concepts:
        related_match = re.search(r"^## Related Concepts\s*\n", content, re.MULTILINE)
        if related_match:
            new_links = [
                f"- [{related}]({slugify(related)}.md)\n"
                for related in related_concepts
                if f"[{related}]({slugify(related)}.md)" not in content
            ]
            if new_links:
                insert_pos = _skip_section_comments(content, related_match.end())
                content = (
                    content[:insert_pos] + "".join(new_links) + content[insert_pos:]
                )
    if content == original:
        return False
    note_path.write_text(content, encoding="utf-8")
    return True


def _skip_section_comments(content: str, start_pos: int) -> int:
    rest = content[start_pos:]
    match = re.match(r"(?:\s|<!--.*?-->)*", rest, re.DOTALL)
    return start_pos + (len(match.group(0)) if match else 0)
