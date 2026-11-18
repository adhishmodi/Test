# API Specification — Intelligent Traffic Monitoring System

| Field | Value |
|---|---|
| Version | 1.0 |
| Status | P3 API contract proposal |
| Style | REST/JSON; multipart media submission |
| Backend | Python + FastAPI |
| Baseline | Approved SRS v1.0 and ARCHITECTURE.md v1.0 |

## 1. Conventions

Base path: /api/v1. JSON property names use snake_case; timestamps are ISO 8601 UTC; IDs are UUIDs. Image/video submission uses multipart/form-data. Job processing is asynchronous. Examples are proposed contracts, not evidence that routes exist.

## 2. Authentication and authorization

No mandatory user account is required initially. Every job resource must be scoped to the submitting browser session or protected by an opaque, high-entropy, short-lived job-access credential. A job UUID is an identifier, never sufficient authorization.

Prefer a secure scoped cookie or Authorization header; never put credentials in URLs, logs, analytics or referrers. If cookies are used, select secure attributes and CSRF protections for deployment. Protect operational/admin endpoints separately. Worker services remain private and use internal credentials.

## 3. Common response and errors

Endpoint-specific JSON objects are used for success. Error envelope:

~~~json
{
  "error": {
    "code": "INVALID_MEDIA",
    "message": "The selected file is not a supported image or video.",
    "details": { "field": "file" },
    "request_id": "req_example"
  }
}
~~~

Never expose stack traces, storage keys, filesystem paths, credentials or raw exception messages.

| HTTP | Meaning |
|---:|---|
| 200 | Successful read/action |
| 201 | Resource created |
| 202 | Accepted for asynchronous processing |
| 204 | Successful deletion, no body |
| 400 | Malformed request/invalid transition |
| 401 | Missing or invalid access context |
| 403 | Not authorized |
| 404 | Not found or intentionally concealed |
| 409 | Resource not in required state |
| 410 | Expired resource |
| 413 | Upload too large |
| 415 | Unsupported media type |
| 422 | Validation failure |
| 429 | Rate/quota exceeded |
| 500 | Unexpected server error |
| 503 | Dependency/service unavailable |

## 4. Endpoint catalog

| Method | Path | Purpose | Access |
|---|---|---|---|
| GET | /health | Liveness | Public, minimal |
| GET | /health/ready | Readiness | Operational protection as needed |
| GET | /models | Available model metadata | Public read |
| GET | /evaluation | Evaluation report metadata | Public read |
| POST | /analyze/image | Submit image | Session/job |
| POST | /analyze/video | Submit video | Session/job |
| POST | /live/sessions | Create webcam session | Session |
| POST | /live/sessions/{session_id}/frames | Submit bounded frame | Session |
| DELETE | /live/sessions/{session_id} | Stop webcam session | Session |
| GET | /jobs | List session jobs | Session |
| GET | /jobs/{job_id} | Read job status | Job/session |
| GET | /jobs/{job_id}/results | Read result summary | Job/session |
| GET | /jobs/{job_id}/media | Read authorized media metadata | Job/session |
| GET | /statistics/{job_id} | Read time-bucket metrics | Job/session |
| GET | /jobs/{job_id}/export | Export summary | Job/session |
| DELETE | /jobs/{job_id} | Delete job and artifacts | Job/session |

All routes are relative to /api/v1.

## 5. Health and model metadata

### GET /health
200: { "status": "ok" }. Liveness only; do not disclose infrastructure.

### GET /health/ready
200 example:
~~~json
{
  "status": "ready",
  "dependencies": { "database": "ready", "queue": "ready" }
}
~~~
Return 503 if a critical dependency prevents service. Avoid hostnames, credentials and internal topology.

### GET /models
200 example:
~~~json
{
  "items": [{
    "id": "model-uuid",
    "name": "vehicle-detector",
    "version": "1.0",
    "detector_family": "candidate-family",
    "tracking_algorithm": "ByteTrack",
    "evaluation_status": "evaluated"
  }]
}
~~~
Only list models approved for use.

### GET /evaluation
200 example:
~~~json
{
  "status": "available",
  "model_version": { "name": "vehicle-detector", "version": "1.0" },
  "dataset": { "name": "documented-dataset", "version": "v1" },
  "metrics": {
    "precision": null, "recall": null, "map_50": null,
    "map_50_95": null, "idf1": null, "count_mae": null
  },
  "runtime": { "hardware": null, "average_fps": null },
  "limitations": []
}
~~~
Null means not measured/not available. Never substitute illustrative values for missing metrics.

## 6. Image and video submission

### POST /analyze/image
Content type: multipart/form-data.
- file (required): one supported image.
- model_version_id (optional): available approved model.

Validate file signature/content, size, decoded dimensions and decode safety. Do not trust client MIME/extension. Generate storage names server-side; apply quotas.

### POST /analyze/video
Content type: multipart/form-data.
- file (required): one supported video.
- model_version_id (optional): available approved model.
- sampling_profile (optional): server-defined profile only.

Validate signature, codec/decode support, size, duration, dimensions, frame rate and compute budget.

Both return 202:
~~~json
{
  "job_id": "7b2d2c30-8c52-4b72-91a1-7e8c1f8d31a1",
  "status": "queued",
  "status_url": "/api/v1/jobs/7b2d2c30-8c52-4b72-91a1-7e8c1f8d31a1",
  "access": { "scope": "job", "expires_at": "2026-11-19T12:00:00Z" }
}
~~~
The credential is conveyed only through the selected secure cookie/header mechanism, never echoed in the body.

Uploads are not automatically retried. An Idempotency-Key header with bounded retention and request fingerprint is an optional proposal; implement only if approved.

## 7. Job endpoints

### GET /jobs
Lists jobs authorized for current session. Query: limit (default 20, bounded), cursor, status, input_type.

200:
~~~json
{
  "items": [{
    "job_id": "job-uuid",
    "input_type": "video",
    "status": "completed",
    "submitted_at": "2026-11-18T08:30:00Z",
    "completed_at": "2026-11-18T08:31:12Z",
    "expires_at": "2026-11-19T08:31:12Z"
  }],
  "next_cursor": null
}
~~~

### GET /jobs/{job_id}
200:
~~~json
{
  "job_id": "job-uuid",
  "input_type": "video",
  "status": "processing",
  "progress_percent": 65,
  "progress_stage": "Analyzing frames",
  "submitted_at": "2026-11-18T08:30:00Z",
  "started_at": "2026-11-18T08:30:04Z",
  "completed_at": null,
  "error": null
}
~~~
Progress may be null when meaningful progress is unavailable.

### GET /jobs/{job_id}/results
Return only when completed; otherwise return a consistent not-ready status (proposed 409).

~~~json
{
  "job_id": "job-uuid",
  "model_version": { "name": "vehicle-detector", "version": "1.0" },
  "total_vehicles": 120,
  "vehicle_counts": {
    "car": 75, "motorcycle": 25, "bus": 8, "truck": 12
  },
  "density": {
    "value": null,
    "unit": "roi_method_specific",
    "method": "documented_roi_occupancy",
    "region": "configured_roi"
  },
  "congestion": { "level": "moderate", "threshold_profile": "profile-version" },
  "runtime": {
    "processing_duration_ms": null,
    "average_fps": null,
    "hardware": null
  }
}
~~~
All numbers above are illustrative only. Return measured values and actual method/context. Density is not inherently vehicles/km.

### GET /jobs/{job_id}/media
Return authorized artifact metadata and, if selected, a short-lived download URL. Never expose storage_key or permanent public URLs. If API streaming is selected, define range support and limits.

### GET /statistics/{job_id}
Query: from_ms, to_ms, bucket_limit (bounded).

~~~json
{
  "job_id": "job-uuid",
  "time_unit": "milliseconds_from_media_start",
  "items": [{
    "timestamp_ms": 5000,
    "vehicles_visible": 14,
    "roi_occupancy": 0.32,
    "density_value": null,
    "congestion_level": "moderate"
  }]
}
~~~

### GET /jobs/{job_id}/export
Proposed format query: json or csv. Include job metadata, model provenance, total/category counts, density method, congestion thresholds and available bucket metrics. Exclude raw media, credentials and private storage references. Freeze exact CSV columns before implementation.

### DELETE /jobs/{job_id}
Proposed success: 204. Verify access, revoke grants, delete temporary media and dependent result/metric data, make cleanup idempotent and retry failed object deletion. Alternative async deletion would return 202 and needs a deletion-status resource; choose one contract before implementation. Do not reveal whether an unauthorized job exists.

## 8. Webcam API (conditional)

SRS requires webcam analysis where browser/hosting resources permit. Initial proposal is bounded HTTP frame submission, not a persistent WebSocket stream.

### POST /live/sessions
JSON request:
~~~json
{
  "model_version_id": "model-uuid",
  "frame_width": 640,
  "frame_height": 360
}
~~~
Server enforces dimensions, session duration, frame rate and payload size.

201:
~~~json
{
  "session_id": "session-uuid",
  "status": "active",
  "max_frames_per_batch": 1,
  "expires_at": "2026-11-18T09:00:00Z"
}
~~~

### POST /live/sessions/{session_id}/frames
One bounded encoded image frame per request is the initial proposal. Choose octet-stream or multipart encoding during implementation.

200:
~~~json
{
  "session_id": "session-uuid",
  "sequence": 12,
  "processed": true,
  "detections": [],
  "vehicle_counts": { "car": 0, "motorcycle": 0, "bus": 0, "truck": 0 },
  "congestion_level": null
}
~~~
Define sequencing, dropped-frame/backpressure behavior, request limits and response bounds before implementation.

### DELETE /live/sessions/{session_id}
204 after stopping processing, closing resources and invalidating session access. Cleanup must cover explicit stop and timeout/disconnect where detectable.

Live support is conditional on measured latency, bandwidth, browser and hosting capacity. If not feasible, show the limitation and preserve image/video workflows.

## 9. Worker contract

Queue messages carry metadata only; media bytes do not travel through Redis.

~~~json
{
  "job_id": "job-uuid",
  "input_type": "video",
  "input_artifact_id": "artifact-uuid",
  "model_version_id": "model-uuid",
  "submitted_at": "2026-11-18T08:30:00Z",
  "attempt": 1
}
~~~

Worker responsibilities:
1. Load and validate job state.
2. Fetch private input with internal credentials.
3. Transition to processing and update progress at bounded intervals.
4. Run OpenCV preprocessing, detection and tracking.
5. Calculate unique counts, ROI density and congestion.
6. Persist aggregate results/time-bucket metrics transactionally.
7. Write temporary output artifacts if required.
8. Mark completed only after required outputs persist.
9. On failure, save safe error code and clean partial artifacts.
10. Make retries idempotent.

Worker is not public; queue payloads contain no tokens or raw media.

~~~mermaid
sequenceDiagram
 actor User
 participant UI as React Client
 participant API as FastAPI
 participant DB as PostgreSQL
 participant Store as Private Media Store
 participant Q as Redis Queue
 participant W as Python Worker
 User->>UI: Select and submit video
 UI->>API: POST /analyze/video
 API->>API: Validate file and session
 API->>Store: Write temporary input
 API->>DB: Create job and artifact metadata
 API->>Q: Enqueue job envelope
 API-->>UI: 202 Accepted with job ID
 Q->>W: Deliver job
 W->>Store: Read private input
 W->>W: Decode, detect, track and aggregate
 W->>DB: Persist result and metrics
 W->>Store: Write temporary output if needed
 W->>DB: Mark completed
 loop Until terminal state
  UI->>API: GET /jobs/{job_id}
  API->>DB: Read authorized status
  API-->>UI: Status and progress
 end
 UI->>API: GET /jobs/{job_id}/results
 API-->>UI: Authorized summary
~~~

~~~mermaid
sequenceDiagram
 actor User
 participant Browser
 participant API as FastAPI
 participant CV as CV Service
 User->>Browser: Explicitly start camera
 Browser->>Browser: Request permission
 Browser->>API: POST /live/sessions
 API-->>Browser: Session ID and limits
 loop While session active
  Browser->>API: POST /live/sessions/{id}/frames
  API->>CV: Process bounded frame
  CV-->>API: Latest detections and metrics
  API-->>Browser: Frame result
 end
 User->>Browser: Stop camera
 Browser->>Browser: Stop media tracks
 Browser->>API: DELETE /live/sessions/{id}
 API-->>Browser: 204 No Content
~~~

## 10. Validation, limits and rate control

Numeric limits are not hard-coded because hosting is deferred. Before implementation, define:
- maximum upload size, video duration and decoded dimensions/pixels;
- supported formats/codecs;
- frame sampling rate and maximum processed frames;
- webcam frame size/rate/payload/session duration;
- per-session concurrent jobs and quotas;
- worker timeout/retry policy;
- polling interval and pagination bounds.

Apply reverse-proxy and application limits. Validate signatures and decode safely. Reject decompression bombs/malformed media. Use server-generated filenames and private storage.

## 11. Error catalog

| Code | HTTP | Meaning |
|---|---:|---|
| INVALID_MEDIA | 422 | Cannot decode/invalid input |
| UNSUPPORTED_MEDIA | 415 | Unsupported format/codec |
| FILE_TOO_LARGE | 413 | Configured upload limit exceeded |
| MEDIA_LIMIT_EXCEEDED | 422 | Duration/dimensions/frame budget exceeded |
| JOB_NOT_READY | 409 | Continue bounded polling |
| JOB_EXPIRED | 410 | Submit again |
| ACCESS_REQUIRED | 401 | Missing/invalid access context |
| ACCESS_DENIED | 403 | Not authorized |
| RATE_LIMITED | 429 | Respect Retry-After |
| MODEL_UNAVAILABLE | 503 | No approved model available |
| PROCESSING_FAILED | 500 | Safe message and request ID |
| SERVICE_UNAVAILABLE | 503 | Dependency unavailable |
| LIVE_UNSUPPORTED | 503 | Live workflow unavailable in deployment |

## 12. SRS traceability

| Requirement | API support |
|---|---|
| FR-01 | POST /analyze/image |
| FR-02 | POST /analyze/video |
| FR-03 | /live/sessions and /frames, conditional |
| FR-04–06 | Results and media artifacts |
| FR-07 | Worker tracking and unique-count semantics |
| FR-08 | GET /jobs/{id}/results |
| FR-09–10 | Results and /statistics |
| FR-11 | Results/statistics for dashboard |
| FR-12 | GET /jobs/{id}/media |
| FR-13 | GET /jobs/{id}/export |
| FR-14 | Submission validation/error catalog |
| FR-15 | GET /jobs/{id} |
| FR-16 | GET /models and /evaluation |

## 13. Open contract decisions

| Topic | Proposal | Must finalize |
|---|---|---|
| Access mechanism | Secure cookie or Authorization header | Session model, CSRF and token lifecycle |
| Numeric limits | Deployment-configured | Benchmark and publish values |
| Idempotency | Optional Idempotency-Key | Decide need |
| Deletion | 204 or async 202 | Select and test cleanup semantics |
| Media delivery | Short-lived URL or API stream | Decide after storage/hosting |
| Progress | Bounded polling | Interval and granularity |
| Export | CSV and JSON | Freeze fields |
| Webcam payload | Bounded HTTP | Encoding, limits and backpressure |
| Cancellation | Not specified | Design worker cancellation before exposing |

## 14. Approval boundary

This contract is documentation only. It does not authorize route/worker implementation, dependencies, database migrations, secrets/configuration changes, deployment or production API exposure.
