# Changelog

All notable project changes are documented here.

## 2026-11-18

### P4 Batch 2 — Application scaffold
- Added the Python 3.12 backend dependency manifest and initial FastAPI application.
- Added liveness and PostgreSQL/Redis readiness endpoints under `/api/v1`.
- Added a backend liveness test and Ruff/pytest configuration.
- Added the React 19 + TypeScript + Vite frontend scaffold and development API proxy.
- Updated Codespaces setup instructions and installed the uv project manager in the devcontainer.
- Dependency lock files are generated during the first install in Codespaces; they could not be generated in the isolated execution environment.

### P4 Batch 1 — Development foundation
- Added the Codespaces devcontainer, Docker Compose PostgreSQL/Redis services, environment template and setup guide.
- Added ignore rules for local secrets, datasets, media and model artifacts.


## 2026-11-18

### P5 — Dataset research and model baseline
- Added BDD100K dataset suitability, class mapping, license notes and split/preprocessing recommendations.
- Documented YOLOX-S as the recommended detector baseline, RT-DETRv2 as an alternative and ByteTrack as the initial tracking candidate.
- Added benchmark methodology and a Google Colab training plan.
- Recommendations remain subject to project-owner review; no dataset was downloaded and no model was trained.
