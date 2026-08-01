# Changelog

All notable changes per release. Versions follow [semver](https://semver.org)
pre-1.0 conventions: minor bumps may include breaking changes (called out
explicitly), patch bumps are docs / build / fixes only.

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
