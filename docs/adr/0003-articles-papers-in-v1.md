# 0003 — Articles and papers ship in v1 with one shared template

**Context.** The current `knowledge-vault` supports YouTube videos, web articles (via trafilatura), PDFs (via pymupdf4llm), and academic papers (via Semantic Scholar DOI lookup). The v1 scope question: include all of this, or ship YouTube-only and add the rest in v2.

**Decision.** Include in v1. Articles and papers share one note template (`article_note.md`), one extraction prompt (`article_concept_extraction.md`), and one polymorphic `fetch` verb that branches on URL/path shape internally.

**Why.**
- Marginal Python cost is low: 2 deps (trafilatura, pymupdf4llm), one fetch-branching path, one template, one prompt fragment.
- Persona #1 (your peer) does meaningful non-video knowledge work; shipping YouTube-only is a guaranteed v1.1 regret.
- Article/paper code in `knowledge-vault` is already clean and generic (365 LoC, no personal coupling).
- The shared-template choice over the current `article_note.md` + `paper_note.md` split removes ~50% of template surface area at near-zero loss — DOI/venue fields are already optional in the article template.
