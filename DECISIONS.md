# Architecture Decision Records (ADRs)

| Field | Value |
|---|---|
| Project | Intelligent Traffic Monitoring System |
| ADR set version | 1.0 |
| Status | Approved architecture baseline |
| Approval date | 2026-11-18 |
| Requirements baseline | SRS v1.0 |

This file records architectural decisions approved by the project owner. A decision marked **provisional** is an approved direction for planning, but a technical choice remains conditional on benchmarking, feasibility or licensing review.

## ADR-001 — Primary language: Python

- **Status:** Approved
- **Decision:** Use Python for backend and computer-vision components.
- **Rationale:** Strong ecosystem for PyTorch, OpenCV, detection, tracking and evaluation.
- **Consequences:** Python dependencies must be pinned and reviewed; training and inference environments must be reproducible.

## ADR-002 — Deep-learning framework: PyTorch

- **Status:** Approved
- **Decision:** Use PyTorch as the primary deep-learning framework.
- **Rationale:** Suitable pretrained-model and fine-tuning ecosystem.
- **Consequences:** Record framework/CUDA versions and training configuration.

## ADR-003 — Detector: benchmark a YOLO-family candidate

- **Status:** Provisional pending benchmark and license review
- **Decision:** Start research with a suitable pretrained YOLO-family detector.
- **Alternatives:** RT-DETR and Faster R-CNN.
- **Rationale:** Candidate balance of speed, detection quality and available tooling.
- **Conditions:** Exact model, package, version, weight license and deployment terms must be reviewed before adoption. If licensing is incompatible, evaluate an alternative.
- **Consequences:** Do not treat a YOLO-family choice or its license as finally selected until the gate is passed.

## ADR-004 — Tracking: ByteTrack initial candidate

- **Status:** Provisional pending comparative evaluation
- **Decision:** Use ByteTrack as the initial tracking candidate and compare with BoT-SORT.
- **Alternatives:** BoT-SORT, DeepSORT.
- **Rationale:** ByteTrack offers a comparatively straightforward tracking pipeline.
- **Consequences:** Validate ID consistency, IDF1/HOTA/MOTA where supported, and failure cases before locking configuration.

## ADR-005 — Image and video processing: OpenCV

- **Status:** Approved
- **Decision:** Use OpenCV for media decoding, frame extraction, preprocessing and video output.
- **Consequences:** Enforce format, dimension, duration and resource limits.

## ADR-006 — Backend: FastAPI

- **Status:** Approved
- **Decision:** Use FastAPI for REST endpoints and API validation.
- **Rationale:** Typed request/response validation, asynchronous support and generated OpenAPI documentation.
- **Consequences:** Keep long-running inference out of API request handlers.

## ADR-007 — Frontend: React + TypeScript

- **Status:** Approved by project owner
- **Decision:** Use React with TypeScript.
- **Alternatives:** Streamlit and Gradio.
- **Rationale:** More flexible interactive dashboard, video overlays, charts and responsive UI.
- **Consequences:** Maintain frontend/backend API contracts and typed client models.

## ADR-008 — Database: PostgreSQL

- **Status:** Approved by project owner
- **Decision:** Use PostgreSQL for job metadata, aggregated metrics and model-version metadata.
- **Alternative:** SQLite for lightweight local-only development.
- **Rationale:** Relational integrity and deployed persistence.
- **Consequences:** No raw video/image payloads in the relational database. Use temporary private storage for media.

## ADR-009 — Asynchronous processing: Redis queue and separate worker

- **Status:** Approved architectural direction; deployment details subject to feasibility
- **Decision:** Separate API request handling from video inference using a Redis-backed queue and Python worker.
- **Rationale:** Avoid blocking API requests and allow independent worker scaling.
- **Consequences:** Requires job lifecycle, retries, failure handling, concurrency limits and cleanup policy. Start with one worker.

## ADR-010 — Training environment: Google Colab

- **Status:** Approved
- **Decision:** Use Google Colab for GPU-dependent fine-tuning.
- **Rationale:** No local GPU is available; Codespaces is not assumed to provide GPU resources.
- **Consequences:** Preserve reproducible training scripts/configuration and document hardware/runtime.

## ADR-011 — Development environment: GitHub Codespaces

- **Status:** Approved
- **Decision:** Support development and lightweight CPU-based demonstrations in GitHub Codespaces.
- **Consequences:** Provide a documented development container and setup instructions during the setup phase.

## ADR-012 — Public hosting: defer selection

- **Status:** Approved by project owner
- **Decision:** Choose the public hosting provider only after benchmarking.
- **Candidates:** General application hosting with a separate worker/database, and ML-focused hosting.
- **Rationale:** Video inference performance, resource limits and cost are not yet known.
- **Consequences:** Keep configuration provider-neutral where practical. Compare CPU/GPU, memory, storage, upload limits, worker duration, concurrency, webcam latency and total cost before recommending a provider.

## ADR-013 — Authentication: no mandatory login initially

- **Status:** Approved by project owner
- **Decision:** Do not require user registration/login in the initial release.
- **Rationale:** User accounts are not required by the approved SRS.
- **Consequences:** Use job-scoped access controls, opaque high-entropy short-lived tokens/session binding, rate limits and protected administrative operations. A job UUID alone is not authorization.

## ADR-014 — Media storage and privacy

- **Status:** Approved
- **Decision:** Do not retain raw uploaded footage or webcam frames by default. Use private temporary storage with expiry and deletion.
- **Rationale:** Align with SRS privacy requirements and reduce exposure.
- **Consequences:** Define retention windows, cleanup of failed/abandoned jobs and deletion behavior before implementation.

## ADR-015 — Density and congestion semantics

- **Status:** Approved methodology direction; thresholds require validation
- **Decision:** Distinguish cumulative unique vehicle counts from current ROI occupancy. Use an image-space ROI density indicator and configurable low/moderate/high congestion thresholds.
- **Rationale:** Prevent frame detections from being mistaken for unique vehicles and avoid claiming physical density without calibration.
- **Consequences:** Document ROI, camera assumptions, threshold calibration and evaluation limitations.

## ADR-016 — Scope and implementation approval boundary

- **Status:** Approved
- **Decision:** This architecture approval authorizes architecture documentation and planning only.
- **Not authorized:** Source-code implementation, dependency installation, database/schema changes, production configuration changes, PR merges or deployment.
- **Consequence:** Each implementation batch and every high-impact action must receive the separate approval required by the project workflow.

## Approval record

The project owner confirmed the following on 2026-11-18:
- Frontend: React + TypeScript.
- Hosting: choose after benchmarking.
- Database: PostgreSQL.
- Authentication: no mandatory login initially.
- Comments: approve the proposed architecture, subject to documented risks and licensing review.

**Overall status: Architecture approved. Implementation not authorized.**


---

## P3 design records — 2026-11-18

The following records capture design proposals documented in P3. Items explicitly marked **Provisional** are not implementation authorization and must be confirmed at the relevant implementation gate.

### ADR-017 — Session-scoped history

- **Status:** Provisional design proposal
- **Decision:** Start with browser-session-scoped job history; do not imply account-backed or cross-device persistence.
- **Rationale:** Consistent with no mandatory login in the initial release.
- **Gate:** Confirm session lifecycle, recovery behavior and retention before implementation.

### ADR-018 — Initial job progress delivery

- **Status:** Provisional design proposal
- **Decision:** Use bounded HTTP polling for job status initially.
- **Rationale:** Simple to operate and sufficient for an initial asynchronous job workflow.
- **Gate:** Set polling interval, progress granularity and rate limits based on API/worker behavior. Server-sent events may be reconsidered if measured need justifies them.

### ADR-019 — Initial webcam transport

- **Status:** Provisional, conditional on benchmark
- **Decision:** Evaluate bounded HTTP frame submissions before adopting a persistent streaming transport.
- **Rationale:** Keeps the first design understandable and avoids assuming WebSocket/streaming infrastructure.
- **Gate:** Validate latency, bandwidth, browser behavior, frame limits and hosting capacity. This is not a real-time performance commitment.

### ADR-020 — Export formats

- **Status:** Provisional design proposal
- **Decision:** Plan for CSV statistics and a JSON summary export.
- **Rationale:** Both are straightforward formats for tabular and structured analysis results.
- **Gate:** Freeze exact fields, privacy filtering and download behavior before implementation.

### ADR-021 — Retention targets

- **Status:** Provisional; requires explicit implementation-time confirmation
- **Decision:** Delete raw uploaded input footage after processing by default, as required by the SRS. Webcam frames remain ephemeral. If processed output media must be retained for result viewing, evaluate a maximum 24-hour temporary-retention target; evaluate 30 days for job metadata and aggregate results.
- **Rationale:** Preserves the approved privacy requirement while giving the UI a bounded way to offer processed outputs.
- **Gate:** Confirm exact output retention, metadata retention, cleanup guarantees and user-facing disclosure before implementation. The 24-hour and 30-day targets are provisional and are not current enforced policy.

### ADR-022 — No cancellation endpoint in initial contract

- **Status:** Provisional design constraint
- **Decision:** Do not expose job cancellation until queue/worker cancellation, partial-artifact cleanup and retry semantics are designed and tested.
- **Rationale:** A UI/API cancellation control without reliable worker cancellation would misrepresent behavior.
- **Gate:** Revisit only with a tested worker lifecycle design.

**P3 status:** UI, database and API designs are documented. The above provisional items remain subject to implementation-time confirmation. No source code, dependencies, database schema, production settings, merge or deployment is authorized by these records.


---

## P5 research recommendations — 2026-11-18

### ADR-023 — Primary dataset: BDD100K

- **Status:** Owner-approved primary dataset; data validation pending
- **Decision:** Use BDD100K labelled images as the initial detector fine-tuning dataset. Use its separate MOT 2020 subset for later tracking evaluation.
- **Rationale:** Urban driving scenes, all four required vehicle categories, weather/time-of-day diversity, and dedicated tracking annotations.
- **Alternatives:** MS COCO 2017 (general scenes, not traffic-specific) and KITTI (does not directly cover the complete four-class requirement).
- **Conditions:** Dataset terms are separate from toolkit-code licensing. Educational/research/not-for-profit use is permitted subject to stated terms; obtain permission before commercial use or redistribution. Validate actual annotation counts, splits and class mapping after download.
- **Consequences:** Do not commit dataset media/labels to Git. Keep the official license notice and record source/checksums. MIO-TCD is optional for a later, separately reviewed experiment and is excluded from the initial baseline.

### ADR-024 — Detector and tracker baseline

- **Status:** Owner-approved initial detector baseline; pilot and exact checkpoint/license verification pending
- **Decision:** Select YOLOX-S (PyTorch) as the initial detector baseline, initialized from a verified COCO-pretrained checkpoint; use ByteTrack as the initial tracker candidate. RT-DETRv2-R18 remains an optional detector comparison.
- **Rationale:** YOLOX has a PyTorch implementation, custom-dataset training guidance and an Apache-2.0 repository license; ByteTrack provides a comparatively simple tracking baseline.
- **Alternatives:** RT-DETRv2-R18; Ultralytics YOLO family.
- **Conditions:** Verify exact checkpoint, pretrained-data, package and dependency terms independently. Ultralytics licensing is not assumed acceptable; its current default AGPL-3.0 obligations must be reviewed.
- **Consequences:** The YOLOX-S baseline choice is approved for planning. Do not install dependencies, train, export or distribute weights until a separate implementation batch is approved and the required compatibility and license checks are complete.

### P5 owner decision record — 2026-11-19

The project owner confirmed:
- Primary dataset: BDD100K.
- Primary detector baseline: YOLOX-S.
- Supplementary dataset: optional; MIO-TCD is excluded from the initial baseline and may be reconsidered only through a separate review.
- Initial tracker candidate remains ByteTrack.

These decisions approve the research direction and documentation only. Dataset validation, checkpoint/package license verification, Colab compatibility testing and pilot benchmarking remain outstanding.

**P5 status:** Dataset and initial detector baseline decisions approved. No dataset download, dependency installation, model training, application implementation, PR merge or deployment is authorized by this record.
