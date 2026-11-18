# UI/UX Design — Intelligent Traffic Monitoring System

| Field | Value |
|---|---|
| Version | 1.0 |
| Status | P3 design proposal |
| Baseline | Approved SRS v1.0 and ARCHITECTURE.md v1.0 |

## 1. Purpose and constraints

This is a design artifact only. It specifies the React + TypeScript experience for image, video and browser-webcam analysis of urban roads and the four required classes: cars, motorcycles, buses and trucks.

Inherited constraints:
- Responsive web interface; no mandatory account/login initially.
- A job UUID is an identifier, not authorization. Access must be session-scoped or protected by an opaque, high-entropy, short-lived credential.
- Raw uploaded footage and webcam frames are not retained by default.
- Video inference is asynchronous and must not block ordinary FastAPI request handling.
- Webcam support depends on browser permissions and hosting capability.
- Do not claim unmeasured accuracy, FPS or real-time performance.
- This is an educational/portfolio prototype, not a safety-critical traffic-control system.

## 2. UX goals

1. Make the next action obvious: choose input, submit, monitor, inspect.
2. Distinguish queued, processing, completed, failed and expired states.
3. Keep processed media prominent and summarize analytics clearly.
4. Explain density as an image-space/ROI estimate, not calibrated physical road density.
5. Make limitations and privacy behavior visible.
6. Support keyboard navigation, visible focus, accessible labels and status announcements.

## 3. Navigation and information architecture

Primary navigation: Dashboard, Analyze, History, Model Evaluation, About/Limitations. Analyze branches into Image, Video and Live Camera. A completed job opens a result detail view.

History is proposed as browser-session scoped; it does not imply permanent, cross-device or account-backed storage.

~~~mermaid
flowchart TD
 A[Dashboard] --> B[Analyze]
 A --> H[History]
 A --> E[Model Evaluation]
 A --> L[About and Limitations]
 B --> I[Image Analysis]
 B --> V[Video Analysis]
 B --> C[Live Camera]
 I --> J[Job Status / Result]
 V --> J
 C --> J
 H --> J
 J --> R[Result Detail]
 R --> X[Export Summary]
 R --> B
~~~

## 4. User journeys

### Image
1. Select Image Analysis.
2. Choose a supported image; show preview, filename and size.
3. Allow remove/replace; display configured limits and privacy note.
4. Submit; show pending state.
5. Display annotated image, counts, density method and congestion level.
6. Allow summary export and job deletion.

### Video
1. Choose a video and display metadata/limits.
2. Submit asynchronously.
3. Show queued/processing state and progress only when meaningful progress is available.
4. Poll status at a bounded interval and stop polling at terminal state.
5. Display processed video (if generated and retained), summary and time-bucket metrics.
6. Export or delete.

### Webcam
1. Show privacy notice and explicit Start action.
2. Request browser permission and display local preview.
3. Submit bounded frames only while the user-started session is active.
4. Show latest available detections/metrics and a clear active indicator.
5. Stop camera tracks and server session on explicit Stop or teardown.
6. If unsupported/denied, explain why and offer image/video workflows.

Bounded HTTP frame submission is a candidate transport, not a real-time guarantee. It must be benchmarked before implementation.

~~~mermaid
flowchart TD
 S([Start]) --> D[Dashboard]
 D --> M{Input mode}
 M --> I[Select image]
 M --> V[Select video]
 M --> C[Start camera with permission]
 I --> VAL[Validate]
 V --> VAL
 C --> P{Permission and host support?}
 P -->|No| ERR[Explain and offer upload]
 P -->|Yes| LIVE[Bounded frame session]
 LIVE --> STOP[User stops session]
 STOP --> RES[Show session summary]
 VAL --> OK{Valid?}
 OK -->|No| ERR
 OK -->|Yes| SUB[Submit job]
 SUB --> Q[Queued]
 Q --> PR[Processing]
 PR --> T{Terminal state?}
 T -->|No| PR
 T -->|Failed| ERR
 T -->|Completed| RES
 RES --> EXP[Optional export]
~~~

## 5. Screen specifications

### Dashboard
Header/navigation; short product explanation and educational disclaimer; three input cards; recent session jobs; supported classes and privacy link. States: first-visit empty, populated history, API unavailable, session storage unavailable.

### Upload selection
Drop zone/file picker, supported formats and server-configured limits, preview, filename/size, replace/remove and submit. Client checks are advisory; backend signature/content validation is authoritative.

### Processing
Job reference, status, progress only if reliable, safe stage description, elapsed time, failure guidance and delete action. Do not expose Cancel until worker cancellation is designed and tested.

### Results
Desktop: media viewer beside summary cards; charts below. Mobile: single-column media, summary, category breakdown, charts and actions. Show bounding boxes, class labels, confidence and track IDs where available. Distinguish unique vehicle counts from per-frame detections. Explain ROI/density method and congestion thresholds.

### Live Camera
Explicit Start/Stop, local preview, active indicator, permission/device errors, latest frame/metrics and privacy explanation. No silent capture. Stop tracks on stop, route exit and teardown.

### History
Session-scoped jobs with input type, submission time, status, summary and open/delete actions. Show expired/missing artifacts explicitly.

### Model Evaluation
Model/version/provenance, dataset version/split, class mapping, detection metrics, supported tracking metrics, count error, congestion metrics, runtime hardware/FPS and limitations. Missing measurements must be shown as not evaluated, never invented.

### About / Limitations
Explain educational purpose, supported classes, out-of-scope features, privacy defaults, density assumptions and environmental/model limitations.

## 6. Functional wireframes

### Dashboard
~~~text
+--------------------------------------------------------------+
| Traffic Monitor | Dashboard | Analyze | History | Evaluation |
+--------------------------------------------------------------+
| Intelligent Traffic Monitoring                               |
| Educational prototype — not for safety-critical decisions    |
|                                                              |
| +----------------+ +----------------+ +--------------------+ |
| | Image Analysis | | Video Analysis | | Live Camera        | |
| | [Open]         | | [Open]         | | [Open]             | |
| +----------------+ +----------------+ +--------------------+ |
| Recent analyses: type / submitted / status / summary / open  |
+--------------------------------------------------------------+
~~~

### Video processing
~~~text
Video Analysis
[Drop video / Choose file]
Selected file, size, duration and configured limits
[Start analysis]
Job reference     Status: Processing
[Progress only when available]
Current stage
[Delete job]
~~~

### Result detail
~~~text
+--------------------------------+-----------------------------+
| Processed image/video          | Total vehicles              |
| Bounding boxes / labels / IDs   | Cars / motorcycles          |
|                                | Buses / trucks              |
|                                | ROI density estimate        |
|                                | Congestion level            |
+--------------------------------+-----------------------------+
| Traffic metrics and charts                                  |
| Method, assumptions and limitations                         |
| [Export summary] [Delete]                                    |
+--------------------------------------------------------------+
~~~

## 7. Responsive behavior

| Area | Desktop >=1024 | Tablet 768–1023 | Mobile <768 |
|---|---|---|---|
| Navigation | Full | Compact | Collapsible |
| Dashboard cards | Three columns | Two columns | One column |
| Results | Media + metrics | Stacked/two-column | Single column |
| Charts | Multi-column | Full width | Simplified/scrollable |
| Media | Large viewer | Fluid | Width constrained |
| History | Table | Condensed | Cards |

Prevent horizontal page overflow; use touch-sized controls; do not rely on hover-only interactions.

## 8. UI states and feedback

| Area | Loading | Empty | Success | Error/recovery |
|---|---|---|---|---|
| Dashboard | Recent-job skeleton | Welcome/actions | Recent jobs | Non-blocking retry banner |
| Upload | Inspect/submit | No file | Preview | Explain invalid/unsupported/oversize |
| Job | Queued/processing | No job | Result link | Safe error and supported retry |
| Results | Load media/summary | Not ready | Metrics/media | Partial availability and retry |
| History | Loading list | No session jobs | Job list | Expired/session unavailable |
| Webcam | Permission/connecting | Not started | Active indicator | Denied/no device/unsupported |
| Evaluation | Loading | Not evaluated | Versioned metrics | Report unavailable |
| Export | Preparing | N/A | Download | Safe retry guidance |

Use accessible live regions; avoid announcing every polling update. Never expose stack traces, storage paths, tokens or secrets.

## 9. Frontend architecture

Approved framework: React + TypeScript. Candidate libraries, not yet locked:
- React Router for routing.
- TanStack Query for server state and bounded polling.
- React state/context for transient UI/session state.
- Zod for client validation where useful.
- Recharts as a chart candidate.
- HTML video with Canvas/SVG overlay.
- Choose either CSS Modules or Tailwind during setup; do not introduce both without need.

### Routes

| Route | View |
|---|---|
| / | Dashboard |
| /analyze/image | Image selection |
| /analyze/video | Video selection |
| /analyze/live | Webcam |
| /jobs/:jobId | Job/result |
| /history | Session history |
| /evaluation | Evaluation |
| /about | Scope/privacy |

A UUID-only route must not authorize job data.

### Component hierarchy

~~~mermaid
flowchart TD
 APP[App] --> ROUTER[Router]
 ROUTER --> SHELL[AppShell]
 SHELL --> NAV[Header and Navigation]
 SHELL --> PAGES[Pages]
 PAGES --> DASH[Dashboard]
 PAGES --> INPUT[Image / Video Upload]
 PAGES --> LIVE[Live Camera]
 PAGES --> JOB[Job Detail]
 PAGES --> HIST[History]
 PAGES --> EVAL[Evaluation]
 JOB --> STATUS[Job Status]
 JOB --> VIEW[Media Result Viewer]
 VIEW --> OVERLAY[Detection Overlay]
 JOB --> SUMMARY[Traffic Summary]
 SUMMARY --> COUNTS[Vehicle Counts]
 SUMMARY --> DENSITY[Density and Congestion]
 JOB --> CHARTS[Traffic Charts]
 JOB --> ACTIONS[Export and Delete]
 PAGES --> STATES[Loading / Empty / Error]
~~~

State ownership:
- Server state: jobs, results, history, model/evaluation metadata.
- Local state: selected file, active tab, overlay visibility, chart range, modal.
- Session context: opaque access credential; never log or expose.
- Poll only while a job is non-terminal and view active; stop on terminal state/unmount.
- Webcam lifecycle must clean up tracks and resources.

API calls belong in a typed service layer. Validate response shapes, normalize errors, never put credentials in URLs, and do not automatically retry uploads unless idempotency is supported.

## 10. Accessibility acceptance

- All controls have accessible names and keyboard support.
- Logical focus order and visible focus.
- Color is not the sole status/congestion indicator.
- Contrast and text resizing are checked.
- Status changes are announced without excessive repetition.
- Charts have text or tabular alternatives.
- Camera activation and stopping are explicit.
- Reduced-motion preferences are respected.
- Validation errors are associated with controls.

## 11. SRS traceability

| Requirement | UI behavior |
|---|---|
| FR-01 | Image picker, validation and result |
| FR-02 | Video picker, async status and result |
| FR-03 | Explicit webcam permission/start/stop, conditional on host |
| FR-04–06 | Detection overlays, class labels, confidence |
| FR-07 | Track IDs and unique-count semantics |
| FR-08 | Total/category count cards |
| FR-09 | ROI density with method explanation |
| FR-10 | Low/moderate/high congestion and thresholds |
| FR-11 | Dashboard and result analytics |
| FR-12 | Annotated image/video viewer |
| FR-13 | Summary export action |
| FR-14 | Validation feedback |
| FR-15 | Progress/status feedback where available |
| FR-16 | Evaluation view/report |

## 12. Open decisions and approval boundary

| Topic | Proposal | Gate |
|---|---|---|
| Styling | CSS Modules or Tailwind | Choose during setup |
| Routing/query | React Router / TanStack Query | Confirm minimal dependencies |
| Charts | Recharts candidate | Accessibility/responsive check |
| Webcam | Bounded HTTP frames | Benchmark host/network/browser |
| Progress | Polling | Set interval and granularity |
| History | Session-scoped | Confirm retention/session semantics |
| Export | CSV + JSON | Freeze fields |
| Cancellation | Excluded initially | Define worker cancellation first |

This document authorizes design only. It does not authorize source changes, dependencies, database migrations, deployment configuration, merge or deployment.
