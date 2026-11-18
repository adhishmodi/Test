# Database Design — Intelligent Traffic Monitoring System

| Field | Value |
|---|---|
| Version | 1.0 |
| Status | P3 logical design proposal |
| Database | PostgreSQL (approved) |
| Baseline | Approved SRS v1.0 and ARCHITECTURE.md v1.0 |

## 1. Principles and scope

This is a logical schema proposal only; no database or migration is created.

- PostgreSQL stores job metadata, model provenance and structured analytics.
- Raw media bytes are not stored in PostgreSQL.
- Private temporary object storage holds media artifacts when required.
- Raw uploaded footage and webcam frames are not retained by default.
- A job UUID is not authorization.
- Store aggregates by default, not every frame-level detection.
- Retention values are proposals pending confirmation before implementation.

## 2. Entities

### 2.1 analysis_jobs

One row per image/video job or webcam analysis session.

| Column | Type | Constraints / meaning |
|---|---|---|
| id | UUID | PK, server generated |
| input_type | VARCHAR(16) | NOT NULL: image, video, webcam |
| status | VARCHAR(20) | NOT NULL: queued, validating, processing, finalizing, completed, failed, expired |
| original_filename | VARCHAR(255) | Nullable, sanitized display metadata |
| mime_type | VARCHAR(100) | Nullable, verified server-side |
| input_size_bytes | BIGINT | Nullable, >= 0 |
| duration_ms | BIGINT | Nullable, >= 0 |
| width_px / height_px | INTEGER | Nullable, > 0 when set |
| submitted_at | TIMESTAMPTZ | NOT NULL |
| started_at / completed_at | TIMESTAMPTZ | Nullable |
| expires_at | TIMESTAMPTZ | NOT NULL |
| deleted_at | TIMESTAMPTZ | Nullable logical deletion marker |
| progress_percent | SMALLINT | Nullable, 0–100 |
| progress_stage | VARCHAR(50) | Nullable, safe user-facing stage |
| error_code | VARCHAR(64) | Nullable, stable safe code |
| error_message | TEXT | Nullable, sanitized message |
| model_version_id | UUID | FK model_versions, nullable until selected |
| access_scope_id | UUID | Optional FK job_access_grants |
| created_at / updated_at | TIMESTAMPTZ | NOT NULL |

Checks: non-negative size/duration; positive dimensions; progress null or 0–100; completed_at >= submitted_at. Indexes: PK, (status, submitted_at DESC), expires_at, (access_scope_id, submitted_at DESC), model_version_id.

### 2.2 job_access_grants (optional persisted authorization)

| Column | Type | Constraints / meaning |
|---|---|---|
| id | UUID | PK |
| token_hash | BYTEA | NOT NULL; hash only, never plaintext token |
| scope_type | VARCHAR(16) | NOT NULL: session or job |
| created_at / expires_at | TIMESTAMPTZ | NOT NULL |
| revoked_at / last_used_at | TIMESTAMPTZ | Nullable |

Generate tokens cryptographically; store only a one-way hash; compare safely; expire/revoke; never place tokens in URLs, logs or analytics. A session grant may scope multiple jobs; a job grant scopes one job. A secure session store may replace this table if approved.

### 2.3 model_versions

| Column | Type | Constraints / meaning |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(120) | NOT NULL |
| version | VARCHAR(80) | NOT NULL |
| detector_family | VARCHAR(80) | NOT NULL |
| weights_reference | TEXT | Nullable artifact identifier, not binary weights |
| framework / framework_version | VARCHAR(80) / VARCHAR(40) | Framework provenance |
| tracking_algorithm | VARCHAR(80) | Nullable |
| class_mapping | JSONB | NOT NULL; four SRS classes |
| dataset_name / dataset_version | VARCHAR(160) / VARCHAR(80) | Nullable |
| license_name | VARCHAR(120) | Nullable |
| provenance_uri | TEXT | Nullable |
| evaluation_status | VARCHAR(20) | NOT NULL: planned, evaluated, deprecated |
| metrics | JSONB | Nullable, versioned evaluation metadata |
| created_at / updated_at | TIMESTAMPTZ | NOT NULL |

Unique (name, version). Model/package and weights licensing review must pass before the model is selected for use.

### 2.4 job_results

One summary row per completed job.

| Column | Type | Constraints / meaning |
|---|---|---|
| id | UUID | PK |
| job_id | UUID | UNIQUE NOT NULL FK analysis_jobs ON DELETE CASCADE |
| model_version_id | UUID | NOT NULL FK model_versions |
| total_vehicles | INTEGER | NOT NULL DEFAULT 0, >= 0 |
| density_value | NUMERIC(10,4) | Nullable, image-space/ROI indicator |
| density_method | VARCHAR(80) | Nullable |
| congestion_level | VARCHAR(16) | Nullable: low, moderate, high |
| congestion_thresholds | JSONB | Nullable, thresholds used |
| processed_fps | NUMERIC(10,3) | Nullable, measured only |
| processing_duration_ms | BIGINT | Nullable, >= 0 |
| result_summary | JSONB | NOT NULL DEFAULT empty object |
| created_at | TIMESTAMPTZ | NOT NULL |

Store the model actually used. Density is not calibrated physical density unless a separate validated calibration is adopted.

### 2.5 vehicle_counts

| Column | Type | Constraints / meaning |
|---|---|---|
| id | UUID | PK |
| job_result_id | UUID | NOT NULL FK job_results ON DELETE CASCADE |
| vehicle_class | VARCHAR(20) | NOT NULL: car, motorcycle, bus, truck |
| vehicle_count | INTEGER | NOT NULL DEFAULT 0, >= 0 |
| created_at | TIMESTAMPTZ | NOT NULL |

Unique (job_result_id, vehicle_class). Counts represent unique vehicles under tracker/counting logic, not detections summed over frames. A completed result should have one row per class.

### 2.6 traffic_metrics

Time-bucketed video/live metrics; image jobs may have none.

| Column | Type | Constraints / meaning |
|---|---|---|
| id | UUID | PK |
| job_id | UUID | NOT NULL FK analysis_jobs ON DELETE CASCADE |
| bucket_index | INTEGER | NOT NULL, >= 0 |
| timestamp_ms | BIGINT | NOT NULL, >= 0 from media/session start |
| roi_occupancy | NUMERIC(10,4) | Nullable image-space occupancy |
| density_value | NUMERIC(10,4) | Nullable method-defined |
| congestion_level | VARCHAR(16) | Nullable low/moderate/high |
| vehicles_visible | INTEGER | Nullable, >= 0; per bucket |
| created_at | TIMESTAMPTZ | NOT NULL |

Unique (job_id, bucket_index); index (job_id, timestamp_ms). Do not store every raw detection here.

### 2.7 media_artifacts

Metadata only; binary content stays in private temporary storage.

| Column | Type | Constraints / meaning |
|---|---|---|
| id | UUID | PK |
| job_id | UUID | NOT NULL FK analysis_jobs ON DELETE CASCADE |
| artifact_type | VARCHAR(20) | NOT NULL: input, processed_video, annotated_image, preview |
| storage_key | TEXT | NOT NULL opaque private key |
| content_type | VARCHAR(100) | NOT NULL |
| size_bytes | BIGINT | NOT NULL, >= 0 |
| checksum_sha256 | CHAR(64) | Nullable |
| created_at / expires_at | TIMESTAMPTZ | NOT NULL |
| deleted_at | TIMESTAMPTZ | Nullable |

Private bucket only; never expose storage_key or permanent public URLs. Issue short-lived downloads after authorization. Webcam frames remain ephemeral and bounded.

## 3. Relationships and ER diagram

- job_access_grants 1-to-many analysis_jobs for session scope; job-scoped grant links one job.
- model_versions 1-to-many analysis_jobs.
- analysis_jobs 1-to-zero/one job_results.
- job_results 1-to-four vehicle_counts.
- analysis_jobs 1-to-many traffic_metrics.
- analysis_jobs 1-to-many media_artifacts.

~~~mermaid
erDiagram
 JOB_ACCESS_GRANTS ||--o{ ANALYSIS_JOBS : scopes
 MODEL_VERSIONS ||--o{ ANALYSIS_JOBS : processes
 ANALYSIS_JOBS ||--o| JOB_RESULTS : produces
 JOB_RESULTS ||--|{ VEHICLE_COUNTS : summarizes
 ANALYSIS_JOBS ||--o{ TRAFFIC_METRICS : records
 ANALYSIS_JOBS ||--o{ MEDIA_ARTIFACTS : references
 JOB_ACCESS_GRANTS {
  uuid id PK
  bytea token_hash
  varchar scope_type
  timestamptz expires_at
 }
 MODEL_VERSIONS {
  uuid id PK
  varchar name
  varchar version
  varchar evaluation_status
 }
 ANALYSIS_JOBS {
  uuid id PK
  varchar input_type
  varchar status
  uuid model_version_id FK
  uuid access_scope_id FK
  timestamptz submitted_at
  timestamptz expires_at
 }
 JOB_RESULTS {
  uuid id PK
  uuid job_id FK
  uuid model_version_id FK
  integer total_vehicles
  numeric density_value
  varchar congestion_level
 }
 VEHICLE_COUNTS {
  uuid id PK
  uuid job_result_id FK
  varchar vehicle_class
  integer vehicle_count
 }
 TRAFFIC_METRICS {
  uuid id PK
  uuid job_id FK
  integer bucket_index
  bigint timestamp_ms
  numeric roi_occupancy
 }
 MEDIA_ARTIFACTS {
  uuid id PK
  uuid job_id FK
  varchar artifact_type
  text storage_key
  timestamptz expires_at
 }
~~~

## 4. Job lifecycle

~~~mermaid
stateDiagram-v2
 [*] --> queued
 queued --> validating
 validating --> processing: valid
 validating --> failed: invalid
 processing --> finalizing: inference complete
 processing --> failed: processing error
 finalizing --> completed: outputs persisted
 finalizing --> failed: persistence error
 completed --> expired: retention elapsed
 failed --> expired: retention elapsed
~~~

Transitions are controlled by API/job manager/worker. Update timestamps consistently. Progress is optional and must be meaningful. Retries must be idempotent and avoid duplicate summaries/counts. Persist safe error codes, not stack traces. Cancelled is excluded until worker cancellation and cleanup semantics are designed.

## 5. Illustrative records

Synthetic example only:

| job | input_type | status | filename |
|---|---|---|---|
| 7b2d… | video | completed | junction.mp4 |
| 8c3e… | image | completed | road.jpg |
| 9d4f… | webcam | failed | NULL |

| class | count |
|---|---:|
| car | 75 |
| motorcycle | 25 |
| bus | 8 |
| truck | 12 |

## 6. Retention and deletion

SRS requires raw uploaded footage and webcam frames not be retained by default after processing. Exact durations are not specified in the approved baseline.

Provisional proposal for later implementation approval:
- Raw uploaded input footage: delete after processing by default, consistent with the SRS; do not retain it for a general 24-hour window.
- Webcam frames: ephemeral processing buffers only; discard after frame processing.
- Processed output media/annotated artifacts: if retained to support result viewing, use private temporary storage with a proposed maximum 24-hour expiry after completion.
- Job metadata and aggregate results: proposed 30-day target.
- Failed/abandoned uploads: bounded expiry and cleanup.
- Access grants: expire no later than the associated resource and be revoked on deletion.

The 24-hour and 30-day values are provisional targets, not current enforced policy. Confirm exact behavior before implementation. The SRS default for raw input footage takes precedence over convenience retention. Confirm before implementation.

Deletion sequence:
1. Authorize using session/job grant.
2. Mark job/artifacts for deletion/expiry.
3. Revoke access grants.
4. Delete private storage objects idempotently.
5. Delete dependent results/metrics and job metadata per retention policy.
6. Record minimal non-sensitive cleanup outcome.
7. Retry failed object deletion and detect orphaned artifacts.

~~~mermaid
flowchart TD
 UP[Input received] --> VAL[Validate and create job]
 VAL --> TMP[Private temporary artifact]
 TMP --> PROC[Worker processes]
 PROC --> AGG[Persist aggregate result]
 AGG --> OUT[Temporary output if needed]
 OUT --> READY[Authorized result]
 READY -->|Delete or expiry| DEL[Revoke grants and delete objects]
 DEL --> DBDEL[Delete dependent data]
 DBDEL --> END([Cleanup complete])
~~~

## 7. Indexes, constraints and operations

- UUID primary keys; UTC TIMESTAMPTZ timestamps.
- Foreign keys with explicit deletion behavior.
- CHECK constraints for non-negative values and bounded progress.
- Unique constraints for one result per job and one count per class.
- Index status/submission, expiry, job/time-series and access scope.
- Paginate history/metrics; avoid unbounded responses.
- Partition only if measured data volume justifies it.
- Use migrations for schema evolution; no migration is part of P3.
- Keep secrets, raw media, plaintext tokens and model weight binaries out of PostgreSQL.

## 8. API-facing semantics

| Field | Meaning |
|---|---|
| total_vehicles | Unique vehicles under selected tracking/counting logic |
| vehicle_counts | Unique counts by four vehicle classes |
| vehicles_visible | Visible in a time bucket, not cumulative unique count |
| roi_occupancy | Image-space ROI occupancy indicator |
| density_value | Method-specific estimate; not inherently vehicles/km |
| congestion_level | low/moderate/high using recorded thresholds |
| processed_fps | Measured throughput with hardware context |
| model_version | Exact model/tracker/config provenance |

## 9. SRS traceability

| Requirement | Database support |
|---|---|
| FR-01–03 | analysis_jobs.input_type and media_artifacts |
| FR-04–06 | job_results model provenance/summary and annotated artifacts |
| FR-07 | Tracker provenance; track-level records not persisted by default |
| FR-08 | total_vehicles and vehicle_counts |
| FR-09 | density_value, density_method, roi_occupancy |
| FR-10 | congestion_level and congestion_thresholds |
| FR-11 | job_results and traffic_metrics |
| FR-12 | media_artifacts |
| FR-13 | Export generated from results/counts/metrics; no export table initially |
| FR-14 | status/error fields and input metadata |
| FR-15 | status, progress and timestamps |
| FR-16 | model_versions evaluation_status and metrics |

## 10. Open decisions and implementation gates

| Topic | Proposal | Gate |
|---|---|---|
| Access grant | Table or secure session store | Choose after threat-model review |
| Media store | Private temporary object storage | Select after hosting benchmark |
| Media retention | 24-hour target | Confirm before implementation |
| Job/result retention | 30-day target | Confirm before implementation |
| Raw detections | Not stored by default | Add only with justified need |
| Webcam buffers | Ephemeral and bounded | Confirm memory/network budget |
| Cancelled status | Excluded | Define worker cancellation first |
| Metric bucket size | Configurable | Select based on output size/value |

This is logical design only. It does not authorize SQL migrations, database provisioning, storage configuration, dependencies or source-code changes.
