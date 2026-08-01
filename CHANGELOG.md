# Changelog

All notable changes per release. Versions follow [semver](https://semver.org)
pre-1.0 conventions: minor bumps may include breaking changes (called out
explicitly), patch bumps are docs / build / fixes only.

## v0.2.0 — 2026-08-01

Dependency security release. This clears all 43 open Dependabot advisories
against `requirements.txt` — 1 critical, 12 high, 24 medium, 6 low. It is a
minor rather than a patch bump because clearing them requires transformers 4 →
5, and that major bump changes observable startup behaviour (see below).

`requirements.txt` was a `pip freeze` dump. It pinned torch's entire CUDA
transitive closure (`nvidia-*-cu12`, `triton`) to the versions that shipped
alongside torch 2.3.1, which made moving torch impossible without hand-editing
a dozen unrelated lines. Those transitive pins are gone; the file is now direct
dependencies plus explicit lower bounds on the transitive packages that carried
advisories, so a resolver cannot quietly pick a vulnerable one.

Packages raised:

| Package | Was | Now at least | Severity cleared |
|---|---|---|---|
| torch | 2.3.1 | 2.13.0 | critical, high, medium, low |
| transformers | 4.42.4 | 5.5.0 | high, medium, low |
| urllib3 | 2.2.2 | 2.7.0 | high, medium |
| protobuf | 5.27.2 | 5.29.6 | high |
| sentencepiece | 0.2.0 | 0.2.1 | high |
| Jinja2 | 3.1.4 | 3.1.6 | medium |
| requests | 2.32.3 | 2.33.0 | medium |
| filelock | 3.15.4 | 3.20.3 | medium |
| idna | 3.7 | 3.15 | medium |

The critical one is the torch advisory covering everything below 2.6.0.

Two behaviour changes fall out of the transformers 4 → 5 bump, both of which
broke the app as written:

- `tokenizer.default_chat_template` no longer exists — transformers dropped the
  per-tokenizer-class fallback in 4.44, and reading the attribute now raises.
  A model whose tokenizer ships no chat template used to silently pick up that
  fallback; it now fails at startup with a message naming `CHAT_TEMPLATE` and
  listing the templates on offer. Models that ship their own template are
  unaffected.
- An unset `HF_TOKEN` used to be passed through as an empty string. The current
  Hugging Face client sends it verbatim, producing an illegal `Bearer ` header
  that the HTTP client rejects, so every model load failed without a token set.
  Unset now means unset.

## v0.1.3 — 2026-08-01

Infrastructure only. Nothing in this repository's own code changed — every
commit in this release touches `.github/workflows/`.

- The pipeline was split: building and publishing stay in `pipeline.yml`, and
  everything that leaves the host now lives beside it in
  `mirror-and-archive.yml`.
- The repository is mirrored to Codeberg as well as GitLab.
- It is archived to the Wayback Machine, Software Heritage, and archive.org.
- Issues opened on either mirror are copied back to GitHub every six hours, and
  the GitHub copy is closed when the original closes.
- Pull requests are switched off on both mirrors. They are force-pushed from
  GitHub, so anything merged on a mirror would be destroyed by the next sync.
  Issues and forking stay enabled.

## v0.1.2 — 2026-07-27

- Added a GitHub Actions CI status badge to the README.

## v0.1.1 — 2026-07-27

- Added self-hosted version and license badges; added a pipeline.yml running the badges job.

## v0.1.0 — 2026-07-26

First tagged release.

- Added `THIRD_PARTY.md` + `LICENSES/` documenting third-party dependencies: `python-telegram-bot` (LGPL-3.0) and the NVIDIA proprietary wheels. The project's own code is WTFPL.
