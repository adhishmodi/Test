# Software Requirements Specification (SRS)
## Intelligent Traffic Monitoring System

| Document field | Value |
|---|---|
| Version | 1.0 |
| Status | Draft — pending owner approval |
| Domain | Deep Learning / Computer Vision |
| Project type | Portfolio-grade academic application |
| Target environment | Urban roads |

---

## 1. Project Overview

The Intelligent Traffic Monitoring System is a computer vision application that analyzes urban-road images, uploaded videos, and live webcam footage. It uses a fine-tuned pretrained object-detection model and multi-object tracking to identify vehicles, count traffic, estimate traffic density, detect congestion, and present traffic statistics through a dashboard.

The application will support two usage modes:
- A demonstration launched from GitHub Codespaces.
- A publicly accessible web application.

The project is intended for academic learning, demonstration, and portfolio use. It is not a certified traffic-control, enforcement, or public-safety system.

## 2. Problem Statement

Urban traffic monitoring can require continuous human observation or specialized infrastructure. Manual observation is time-consuming and makes it difficult to obtain consistent vehicle counts and traffic-condition summaries across video footage.

This project will provide an automated prototype that extracts vehicle-level and traffic-level information from road imagery and video. It will help users inspect vehicle movement, traffic volume, density, and congestion through a visual interface.

## 3. Objectives

1. Detect vehicles in supported road images and video frames.
2. Classify four vehicle categories: cars, motorcycles, buses, and trucks.
3. Track detected vehicles across video frames with persistent tracking identifiers.
4. Count vehicles, including category-wise counts.
5. Estimate traffic density using a documented and reproducible method.
6. Classify traffic conditions into defined congestion levels.
7. Present processed footage and traffic statistics in an interactive dashboard.
8. Evaluate detection, tracking, counting, congestion classification, and runtime performance.
9. Provide reproducible training, setup, testing, and deployment documentation.

## 4. Target Users

- Computer science, AI, and machine-learning students.
- Academic project evaluators and instructors.
- Researchers and learners exploring computer vision.
- Developers interested in intelligent transportation prototypes.
- Users demonstrating or exploring traffic analytics.

## 5. Scope

### 5.1 In scope for the initial release

- Urban-road traffic scenes.
- Cars, motorcycles, buses, and trucks.
- Image upload and analysis.
- Video upload and analysis.
- Live webcam capture and analysis, subject to browser and hosting capabilities.
- Vehicle detection and classification.
- Multi-object tracking.
- Vehicle counting and category-wise statistics.
- Traffic density estimation.
- Congestion detection.
- Traffic statistics dashboard.
- Model evaluation and documented test results.
- Codespaces demonstration and public web deployment.

### 5.2 Out of scope for the initial release

- Automatic traffic-signal control.
- Automatic fines, enforcement, or law-enforcement decisions.
- Face recognition or driver identification.
- Number-plate recognition.
- City-wide camera-network integration.
- Guaranteed vehicle-speed estimation.
- Lane-wise traffic analytics.
- Commercial-scale or safety-critical deployment.

These items may be considered as separately scoped future enhancements.

## 6. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | The system shall accept supported road images for analysis. | Must |
| FR-02 | The system shall accept supported video files for analysis. | Must |
| FR-03 | The system shall provide a live webcam input workflow where browser permissions and hosting resources permit. | Must |
| FR-04 | The system shall detect vehicles in input images and video frames. | Must |
| FR-05 | The system shall classify detected vehicles as car, motorcycle, bus, or truck. | Must |
| FR-06 | The system shall display detection bounding boxes, class labels, and confidence scores. | Must |
| FR-07 | The system shall track vehicles across consecutive video frames and assign tracking IDs. | Must |
| FR-08 | The system shall calculate total vehicle counts and counts by vehicle category. | Must |
| FR-09 | The system shall estimate traffic density using a documented measurement method and defined analysis region. | Must |
| FR-10 | The system shall classify congestion into documented levels, initially low, moderate, and high. | Must |
| FR-11 | The system shall display vehicle counts, category distribution, density, and congestion results in a dashboard. | Must |
| FR-12 | The system shall display processed images or video with detection and tracking overlays. | Must |
| FR-13 | The system should allow users to export or download analysis summaries. | Should |
| FR-14 | The system shall validate input formats and report unsupported, invalid, or corrupted files clearly. | Must |
| FR-15 | The system should provide progress or status feedback during longer video-processing jobs. | Should |
| FR-16 | The system shall provide a model-evaluation view or documented evaluation report. | Must |

## 7. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Performance | Video processing shall use manageable frame or batch processing. Latency and FPS shall be measured and reported on the target deployment environment. |
| Accuracy | Model and analytics quality shall be evaluated on held-out test data using suitable metrics. |
| Usability | The interface shall be clear, responsive, and usable on common desktop and mobile browsers. |
| Reliability | Invalid inputs and inference failures shall be handled without crashing the entire application. |
| Maintainability | Detection, tracking, analytics, API, and interface components shall be modular. |
| Scalability | The design shall allow model and processing components to be upgraded independently. |
| Security | Uploads shall be validated, file types restricted, and file-size limits enforced. |
| Privacy | Raw uploaded footage and webcam frames shall not be retained by default after processing. |
| Reproducibility | Dataset versions, model weights, training configuration, dependencies, and evaluation procedures shall be documented. |
| Portability | Development shall be supported in GitHub Codespaces; GPU-dependent training shall be performed in Google Colab. |
| Accessibility | Controls, labels, and status messages should be usable with standard keyboard and assistive-technology workflows. |

## 8. High-Level System Architecture

The system shall be organized into the following logical layers:

1. **Input layer**
   - Image upload.
   - Video upload.
   - Browser webcam capture.

2. **Preprocessing layer**
   - Input validation.
   - Video frame extraction.
   - Image resizing and normalization as required by the selected model.

3. **Computer-vision layer**
   - Fine-tuned pretrained vehicle detector.
   - Vehicle-class filtering.
   - Multi-object tracking.
   - Bounding-box and tracking-overlay generation.

4. **Traffic analytics layer**
   - Total and category-wise counting.
   - Traffic-density calculation.
   - Congestion-level classification.
   - Summary-statistics generation.

5. **Presentation layer**
   - Image and processed-video viewer.
   - Webcam monitoring view.
   - Traffic analytics dashboard.
   - Results export.

6. **Deployment and operations layer**
   - GitHub source repository.
   - Codespaces demonstration.
   - Public web application.
   - Configuration, logging, and documented deployment process.

## 9. Machine-Learning Requirements

### 9.1 Training strategy

The project shall fine-tune a suitable pretrained object-detection model. Training a complete detector from random initialization is not part of the selected initial approach.

### 9.2 Model selection

A suitable YOLO-family detector may be evaluated as a candidate. The exact model, model size, framework version, and tracking algorithm shall be selected during architecture and technology design after considering accuracy, inference speed, licensing, hardware, and deployment constraints.

### 9.3 Dataset requirements

The selected dataset or combination of datasets shall:
- Contain representative urban-road scenes.
- Include annotations for the four target vehicle categories.
- Have documented provenance and usage/licensing terms.
- Be divided into training, validation, and held-out test subsets.
- Avoid leakage between related video sequences where practical.
- Be documented with preprocessing and class-mapping details.

### 9.4 Evaluation metrics

The evaluation plan shall consider:
- Detection precision and recall.
- mAP@0.5 and mAP@0.5:0.95.
- Tracking metrics such as IDF1, HOTA, or MOTA when supported by the evaluation dataset and tooling.
- Vehicle-count error, such as mean absolute error.
- Congestion-classification metrics, including confusion matrix and per-class precision/recall.
- Inference latency and processing FPS on documented hardware.

Targets shall be established after a baseline benchmark. The project shall report measured results rather than claim unverified accuracy or real-time performance.

## 10. Development Environment and Tools

| Tool / technology | Intended purpose |
|---|---|
| GitHub | Source control, issues, documentation, and collaboration |
| GitHub Codespaces | Main development environment and lightweight testing |
| Google Colab | GPU-assisted training and fine-tuning |
| Python | Primary programming language |
| PyTorch | Deep-learning framework, subject to final model choice |
| OpenCV | Image and video processing |
| Detection framework | Pretrained vehicle detection and fine-tuning |
| Tracking library | Multi-object tracking |
| Web framework | Application interface and backend/API |
| Automated tests | Unit, integration, and application workflow validation |

The exact web framework, tracking library, model package, and hosting provider remain architecture-phase decisions.

## 11. Deployment Requirements

### 11.1 Codespaces demonstration

- The repository shall include clear instructions to create and launch the development environment.
- The application shall support a documented demonstration workflow.
- CPU-based inference shall be supported where practical.
- GPU-dependent training shall not be assumed to run inside Codespaces.

### 11.2 Public web application

- The application shall be accessible through a public URL.
- Users shall be able to submit supported images and videos.
- The application shall display analysis outputs and dashboard statistics.
- Webcam access shall use browser permission controls and shall be enabled only where the deployment architecture supports it.
- Hosting compute, memory, execution-time, upload-size, and concurrency limits shall be documented.
- The application shall not promise real-time throughput until measured on the deployed infrastructure.

## 12. Acceptance Criteria

The initial release will be accepted when:

1. The application accepts supported image and video inputs and validates them.
2. The detector produces vehicle detections for all four target classes on representative test samples.
3. Detection overlays show bounding boxes and class labels; confidence scores are shown where available.
4. Tracking IDs persist across suitable consecutive video frames.
5. The system reports total and category-wise vehicle counts.
6. Traffic-density calculations use a documented method and defined region of interest.
7. Congestion levels are produced using documented thresholds or a validated classification method.
8. The dashboard displays the required traffic statistics.
9. The image, video, and webcam workflows are implemented, with any webcam hosting limitations explicitly documented.
10. A held-out evaluation report includes relevant model and analytics metrics.
11. The Codespaces setup and public deployment instructions are documented.
12. The public application is deployed and its supported workflows are smoke-tested.
13. Known limitations, dataset licenses, model provenance, and reproducibility instructions are documented.

## 13. Constraints, Assumptions, and Risks

- No local GPU is available; Google Colab is the planned environment for GPU-dependent training.
- Codespaces is intended for development and lightweight tests, not assumed GPU training.
- Public hosting may provide CPU-only or resource-limited compute.
- Webcam inference throughput depends on browser capture, network conditions, and server resources.
- Large video uploads may require file-size limits, asynchronous processing, or chunked processing.
- Dataset licensing and suitability must be checked before training or redistribution.
- Traffic density is an estimate tied to the chosen camera view, region of interest, and measurement method; it is not automatically a calibrated physical road-occupancy measurement.
- Congestion thresholds must be defined, justified, and evaluated.
- Camera angle, occlusion, lighting, weather, and dataset domain shift may reduce model performance.
- The application is a prototype for education and analysis, not safety-critical operation.

## 14. Future Enhancements

Potential future features, subject to separate requirements and feasibility review:
- Vehicle-speed estimation using camera calibration and scene geometry.
- Lane-wise traffic analysis.
- Multiple-camera processing.
- Historical traffic trends and reports.
- Geographic traffic visualization.
- Traffic-signal optimization recommendations.
- Number-plate recognition, only after a separate privacy, legal, and security assessment.

## 15. Requirements Traceability and Change Control

- Functional requirements use stable identifiers (FR-01, FR-02, etc.).
- Architecture decisions shall map back to these requirements.
- Tests shall reference the requirement IDs they verify.
- Scope changes shall be recorded in DECISIONS.md and reflected in this document.
- Changes to requirements after approval shall increment the document version and be summarized in CHANGELOG.md.

---

**Approval state:** Draft finalized for review. The project owner must approve this SRS before architecture decisions are treated as a committed implementation baseline.
