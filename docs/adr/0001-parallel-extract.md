# 0001 — Parallel extract, not replacement

**Context.** The generic YouTube/OCR/repo-correlation engine lives inside `knowledge-vault`, the author's private notes project. Three relationship shapes were considered: parallel extract (new greenfield public repo), rebase-on-top (knowledge-vault depends on video-buddy), or full replacement (rename + rewrite in place).

**Decision.** Parallel extract. video-buddy starts as a clean greenfield repo with no LFS objects, no personal data, and no migration burden. knowledge-vault keeps running unchanged.

**Why.** Lowest-risk path. Replacement front-loads the risk of bricking the daily knowledge workflow before the public thing has shipped. Rebase-on-top is the right long-term shape but the wrong first move. A later rebase remains possible once video-buddy is stable.
