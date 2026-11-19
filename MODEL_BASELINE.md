# P5 — Model Baseline

| Field | Value |
|---|---|
| Project | Intelligent Traffic Monitoring System |
| Phase | P5 — Dataset Research and Model Baseline |
| Status | Owner-selected detector baseline; pilot and license checks pending |
| Research date | 2026-11-18 |

## 1. Recommendation

**Owner decision (2026-11-19): select YOLOX-S (PyTorch implementation) as the initial detector baseline, initialized from a verified COCO-pretrained checkpoint and fine-tuned on the four BDD100K vehicle classes.**

Why:
- The official repository provides a PyTorch implementation and custom-dataset training instructions.
- The repository is Apache-2.0 licensed.
- YOLOX provides smaller Nano/Tiny/Small variants, custom training examples and export paths.
- YOLOX-S is a practical starting point for a student project using a Google Colab GPU, without beginning with a large detector.

This is the selected starting baseline for the project, not a claim that YOLOX-S is the most accurate model or the final production model. The pilot must verify code/runtime compatibility, dataset conversion, checkpoint provenance and applicable terms before a full training run or any weight distribution.

## 2. Detector comparison

| Candidate | Advantages | Trade-offs | Role |
|---|---|---|---|
| **YOLOX-S** | PyTorch implementation; Apache-2.0 repository; custom data guide; pretrained COCO checkpoints; smaller model variants | Older codebase than some newer detectors; custom experiment configuration is required; benchmark performance on BDD100K is unknown | **Primary baseline** |
| **RT-DETRv2-R18** | Transformer-based real-time detector; official PyTorch implementation; Apache-2.0 repository; COCO model zoo | More involved configuration/training path; should be measured for Colab memory and inference latency | Secondary comparison |
| **Ultralytics YOLO family** | Very simple training/inference workflow; strong documentation and ecosystem | Ultralytics states the framework and trained models are AGPL-3.0 by default; an Enterprise license is needed for use cases that cannot comply with AGPL obligations | Convenience reference only; do not adopt until license implications are accepted |

Official sources:
- YOLOX repository and license: https://github.com/Megvii-BaseDetection/YOLOX
- YOLOX custom-dataset training: https://github.com/Megvii-BaseDetection/YOLOX/blob/main/docs/train_custom_data.md
- RT-DETR / RT-DETRv2 repository: https://github.com/lyuwenyu/RT-DETR
- Ultralytics licensing: https://www.ultralytics.com/license

### 2.1 Licensing rules

A repository license does not automatically settle the license of every pretrained checkpoint, dataset or dependency. Before using or redistributing a checkpoint:
1. Record its exact file name, source URL, release/version and checksum.
2. Review the checkpoint/model license and the training dataset's terms.
3. Preserve required notices.
4. Do not upload weights to Git unless redistribution rights are confirmed.

YOLOX's repository is Apache-2.0; BDD100K data has separate terms. Ultralytics' current licensing page describes AGPL-3.0 and Enterprise options and states that trained models are covered by AGPL-3.0 by default. If the project later becomes proprietary or commercial, re-evaluate all licenses before deployment.

## 3. Tracking recommendation

**Initial tracker: ByteTrack**, used after detector inference.

Conceptual pipeline:
1. Detector predicts boxes, class IDs and confidence scores for a frame.
2. Tracker associates detections with existing tracks across frames.
3. Matched objects keep their track IDs; new objects receive IDs; lost tracks are retained/removed according to tracker settings.
4. Analytics count unique track IDs crossing a configured counting line or region, rather than adding every frame detection.

ByteTrack is a lightweight association approach that uses both high- and lower-confidence detections to recover objects that may otherwise be dropped. It is suitable as an understandable first tracker for traffic footage.

Alternatives:
- **BoT-SORT:** compare if ByteTrack has frequent identity switches or loses vehicles during occlusion/camera motion.
- **DeepSORT:** consider only if appearance/ReID features are justified; extra complexity is not required for the first version.

Sources:
- ByteTrack paper: https://arxiv.org/abs/2110.06864
- ByteTrack implementation: https://github.com/FoundationVision/ByteTrack
- HOTA paper: https://doi.org/10.1007/s11263-020-01375-2

The ByteTrack repository is MIT-licensed; preserve its license notice. Confirm the actual implementation/dependency versions before adding them. Detector and tracker licenses must be reviewed independently.

## 4. Benchmark methodology

### 4.1 Detection

Evaluate the selected YOLOX-S baseline on the fixed BDD100K four-class split. RT-DETRv2-R18 remains an optional comparison if the pilot results, available compute and project schedule justify it.

Report:
- Precision and recall.
- mAP@0.5.
- mAP@0.5:0.95.
- Per-class precision, recall and AP for car, motorcycle, bus and truck.
- Confusion matrix and representative false-positive/false-negative examples.

Use the same image split, image size, class mapping and evaluation code. Do not compare scores produced on different datasets or different splits as if they were equivalent.

### 4.2 Runtime

Record:
- GPU model and memory.
- Framework/runtime versions.
- Image size, batch size and precision mode.
- Model load time separately from inference.
- Warm-up procedure.
- Average and percentile inference latency.
- Throughput in frames per second (FPS).

Measure detector-only FPS and end-to-end pipeline FPS separately. Include preprocessing, tracking and video decoding in the end-to-end figure. Do not describe the system as real-time until measured on the actual deployment hardware.

### 4.3 Tracking (later P7 evaluation)

Use the labelled BDD100K MOT subset and a supported MOT evaluation tool. Report:
- HOTA (balances detection and association quality).
- IDF1 (identity consistency).
- MOTA (CLEAR MOT summary metric).
- Identity switches and track fragmentation where supported.

Use the same detector outputs when comparing trackers so the tracker comparison is fair. Tracking metrics are not part of the first detector-only baseline unless the MOT subset and evaluation pipeline are ready.

### 4.4 Counting and congestion (later P7 evaluation)

- Counting: compare predicted unique vehicle counts with manually verified ground truth per clip/line; report MAE and count error by class.
- Congestion: define a reproducible ROI and threshold profile, create manually labelled low/moderate/high reference clips, then report confusion matrix, per-class precision/recall and macro-F1.
- Density: report the actual ROI occupancy/density formula and units. Do not label image-space occupancy as vehicles/km without camera calibration.

## 5. Baseline decision gates

YOLOX-S is selected as the initial baseline. A trained model can be accepted for application integration only after:
- Custom-data training completes without data/label errors.
- Per-class validation metrics are available.
- The model runs on a representative image and video.
- Runtime is measured on the available Colab GPU and on the intended inference environment.
- Exact package, checkpoint and dataset license terms are recorded.
- The pilot and measured results are reviewed. A second-detector comparison is optional, not a prerequisite for beginning the YOLOX-S baseline.

**No accuracy target is pre-declared.** Establish a project target after the first reproducible baseline results are available.

## 6. P5 acceptance criteria

- [x] Owner-selected primary detector baseline (YOLOX-S) and alternative documented.
- [ ] Repository, model checkpoint and dataset licenses distinguished.
- [ ] Tracking candidate and alternatives documented.
- [ ] Detection, tracking, counting and congestion metrics defined.
- [ ] Fair benchmark conditions specified.
- [x] YOLOX-S baseline decision recorded; final trained-model acceptance remains conditional on pilot results and measurements.
- [ ] No model package or dependency has been installed as part of this research document.

**Status:** YOLOX-S is the owner-selected initial detector baseline; ByteTrack remains the initial tracker candidate. Pilot validation, runtime compatibility and exact checkpoint/package license checks remain outstanding. No training or dependency installation has been performed.
