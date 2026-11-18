# Changelog

All notable project documentation and implementation changes are recorded here.

## 2026-11-18

### Architecture
- Recorded owner-approved P2 technical architecture in `ARCHITECTURE.md`.
- Recorded architecture decisions and approval conditions in `DECISIONS.md`.
- Confirmed React + TypeScript, PostgreSQL and no mandatory initial login.
- Deferred public hosting selection until benchmarking.
- Kept detector/package selection conditional on performance and licensing review.
- No application code, dependencies, database schema or deployment configuration changed.

### P3 — UI/UX, database and API design
- Added `UI_UX_DESIGN.md` with navigation, user journeys, responsive layouts, UI states, frontend structure, accessibility and SRS traceability.
- Added `DATABASE_DESIGN.md` with the proposed PostgreSQL logical schema, relationships, lifecycle, retention/deletion design and SRS traceability.
- Added `API_SPECIFICATION.md` with proposed REST contracts for image/video jobs, status/results, analytics, export, webcam sessions, health and worker integration.
- Recorded provisional P3 decisions and implementation gates in `DECISIONS.md`.
- Explicitly aligned raw-input deletion with the SRS privacy requirement; 24-hour processed-output and 30-day metadata targets remain provisional.
- Kept `ARCHITECTURE.md` unchanged because the P3 detail is appropriately captured in the dedicated design specifications.
- Documentation only: no source code, dependencies, migrations, secrets, deployment settings or production services changed. No merge or deployment performed.
