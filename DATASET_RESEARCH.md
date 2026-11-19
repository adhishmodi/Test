# P5 — Dataset Research

| Field | Value |
|---|---|
| Project | Intelligent Traffic Monitoring System |
| Phase | P5 — Dataset Research and Model Baseline |
| Status | Owner-selected primary dataset; data validation pending |
| Research date | 2026-11-18 |

## 1. Requirements

The dataset must support urban-road vehicle detection for **car, motorcycle, bus and truck**. It should provide varied road scenes, reliable bounding boxes, a defensible training, validation and held-out evaluation strategy and clear usage terms. Video tracking annotations are desirable for the later tracking evaluation.

## 2. Candidate comparison

| Dataset | Strengths | Limitations for this project | Recommendation |
|---|---|---|---|
| **BDD100K** | Dashcam driving scenes; 100K 1280×720 images; varied weather, time of day and road scenes; detection labels include car, truck, bus and motorcycle; separate box-tracking task | Large download; US driving domain may differ from Indian roads; data terms restrict use to educational/research/not-for-profit purposes unless separately licensed; class imbalance must be measured | **Primary dataset** |
| **MS COCO 2017** | Widely used pretrained-detection benchmark; contains car, motorcycle, bus and truck; convenient for checking transfer-learning compatibility | General everyday imagery rather than a traffic-monitoring dataset; not sufficient alone to represent fixed urban-road cameras or traffic sequences | Use only as pretrained-weight provenance / optional secondary comparison, not as the project dataset |
| **KITTI** | Real-world driving imagery with object-detection and tracking research resources | Its common 2D detection classes do not directly provide the complete four-class mapping required here; smaller scope and different sensor/camera setup | Not selected as primary |

## 3. Selected primary dataset — BDD100K

**Owner decision (2026-11-19): BDD100K is approved as the primary dataset for the initial detector baseline.** MIO-TCD is optional for a later, separately reviewed experiment and is excluded from the initial baseline. This decision approves the dataset choice for planning; it does not authorize downloading or processing the data.

Official resources:
- Dataset and download documentation: https://doc.bdd100k.com/download.html
- Official toolkit and task descriptions: https://github.com/bdd100k/bdd100k
- Label format and class definitions: https://doc.bdd100k.com/format.html
- Dataset paper: https://openaccess.thecvf.com/content_CVPR_2020/html/Yu_BDD100K_A_Diverse_Driving_Dataset_for_Heterogeneous_Multitask_Learning_CVPR_2020_paper.html
- Dataset license: https://doc.bdd100k.com/license.html

BDD100K is the best initial fit because it is a driving dataset, includes the four required vehicle categories in its object-detection labels, and provides a separate multi-object box-tracking task. Its images are 1280×720 and the dataset includes scene, weather and time-of-day diversity. The official download documentation lists the 100K image package at approximately 5.3 GB; the full video package is approximately 1.8 TB and is unnecessary for the first detector baseline.

### 3.1 Use only the required subsets

1. Download the **100K Images** and the recommended **Detection 2020 Labels** for object detection.
2. Do not download the full 1.8 TB video archive for the first detector experiment.
3. MIO-TCD is not part of the initial dataset. Reconsider it only if BDD100K validation exposes a specific coverage gap and its separate license and class mapping are reviewed.
4. Do not download the optional supplementary dataset as part of the initial baseline.
5. For later tracking work, separately obtain the **MOT 2020 Images** and **MOT 2020 Labels** subset. The official documentation describes this as a subset of the videos resampled to 5 Hz, with training and validation labels.
6. Record the exact official download package, date, checksum and license notice in the experiment manifest.

### 3.2 Class mapping

| Project class | BDD100K detection category |
|---|---|
| car | car |
| motorcycle | motorcycle |
| bus | bus |
| truck | truck |

Map only these four categories for the initial project detector. Ignore other categories for training unless a later requirement explicitly adds them. Preserve the original category names and IDs in the conversion manifest.

### 3.3 Split strategy and leakage prevention

- Use the official labelled training images as the source training pool.
- Create a validation subset from the official training pool using a fixed, recorded random seed.
- Keep the official labelled validation split untouched as the project's held-out detector evaluation split. Do not describe it as BDD100K's official test set.
- The official test images are unlabelled; do not use them for metric calculation.
- Keep images from the same source video in only one split wherever source-video identifiers are available. This prevents near-duplicate frames leaking between training and evaluation.
- For tracking, preserve the official video/sequence split; never split individual frames from one sequence across train and validation.

The exact split sizes will be recorded after inspecting the downloaded annotations and sequence metadata. Do not invent labelled test ground truth.

## 4. Preprocessing plan

1. Verify downloaded archives against published checksums where available.
2. Validate image decoding, dimensions and annotation references; report missing/corrupt files.
3. Convert official Scalabel/JSON bounding boxes into the detector's required format with a deterministic script.
4. Clip boxes to image boundaries and reject invalid/zero-area boxes; log every rejected annotation.
5. Convert coordinates carefully and test the conversion by rendering sample overlays.
6. Resize/letterbox to 640×640 for the first baseline while preserving aspect ratio.
7. Apply training-only augmentation: horizontal flip where appropriate, modest scale/translation, brightness/contrast and HSV changes. Avoid transformations that make road scenes unrealistic.
8. Do not augment validation or held-out evaluation data.
9. Calculate per-class object counts and box-size distributions before training. Address rare motorcycle/bus/truck examples through sampling or loss configuration only after measuring the imbalance.
10. Keep raw data outside Git. Commit only scripts, manifests, documentation and small non-sensitive examples permitted by the dataset terms.

## 5. License and usage gate

The BDD100K repository code has a BSD 3-Clause license, but that is **not the dataset license**. The dataset's own license grants educational, research and not-for-profit use under stated notice/redistribution conditions; commercial use is separately restricted to BDD/BAIR Commons members and affiliates unless separately licensed.

Project action:
- Retain the dataset license and required copyright notice with experiment records.
- Do not redistribute the original images, videos or annotations in this repository or public deployment.
- Publicly demonstrating model predictions does not itself grant rights to redistribute the source dataset.
- Before any commercial use, redistribution, or use outside the stated educational/research/not-for-profit scope, obtain and review written permission from the rights holder.
- Verify the current terms on the official page at download time. This document is not legal advice.

## 6. Risks and mitigations

| Risk | Mitigation |
|---|---|
| US dashcam scenes differ from Indian urban roads | Evaluate on a small separately collected, properly licensed Indian-road sample before claiming local generalization |
| Class imbalance | Measure per-class counts; report per-class precision/recall and mAP; use balanced sampling only if justified |
| Small/distant vehicles | Inspect box-size distribution; compare 640 and a larger input size only if GPU budget permits |
| Similar frames leak across splits | Split by source video/sequence where possible |
| Large download consumes storage/time | Start with labelled images; defer full videos; download MOT subset only for tracking |
| Dataset license limits downstream use | Keep dataset private, retain notices and obtain permission before broader/commercial use |

## 7. P5 dataset acceptance criteria

- [x] Primary dataset decision recorded: BDD100K.
- [x] Supplementary MIO-TCD explicitly deferred as optional, not part of the initial baseline.
- [x] Official dataset and license sources recorded.
- [ ] Four project classes mapped and verified against annotations.
- [ ] Detection and tracking subsets identified separately.
- [ ] Split strategy prevents sequence leakage.
- [ ] Annotation conversion and visual spot-check procedure defined.
- [ ] Dataset size, class counts and corrupt/missing-file report captured after download.
- [ ] Dataset is not committed to Git.

**Status:** BDD100K is the owner-approved primary dataset. It has not been downloaded or validated. Actual annotation counts, class mapping in the selected label package, split integrity and conversion correctness remain to be verified during the data-preparation task. Actual annotation counts and conversion correctness remain to be verified during the first data-preparation task.
