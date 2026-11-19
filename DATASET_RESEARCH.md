# P5 — Dataset Research

| Field | Value |
|---|---|
| Project | Intelligent Traffic Monitoring System |
| Phase | P5 — Dataset Research and Model Baseline |
| Status | Owner-selected primary dataset; readiness review documented; acquisition and data validation pending |
| Research date | 2026-11-19 |

## 1. Requirements

The dataset must support urban-road vehicle detection for **car, motorcycle, bus and truck**. It should provide varied road scenes, reliable bounding boxes, a defensible training, validation and held-out evaluation strategy and clear usage terms. Video tracking annotations are desirable for the later tracking evaluation.

## 2. Candidate comparison

| Dataset | Strengths | Limitations for this project | Recommendation |
|---|---|---|---|
| **BDD100K** | Dashcam driving scenes; 100K 1280×720 images; varied weather, time of day and road scenes; detection labels include car, truck, bus and motorcycle; separate box-tracking task | Large download; US driving domain may differ from Indian roads; dataset terms limit commercial use to BDD/BAIR Commons members and affiliates unless separately licensed; class imbalance must be measured | **Primary dataset** |
| **MS COCO 2017** | Widely used pretrained-detection benchmark; contains car, motorcycle, bus and truck; convenient for checking transfer-learning compatibility | General everyday imagery rather than a traffic-monitoring dataset; not sufficient alone to represent fixed urban-road cameras or traffic sequences | Use only as pretrained-weight provenance / optional secondary comparison, not as the project dataset |
| **KITTI** | Real-world driving imagery with object-detection and tracking research resources | Its common 2D detection classes do not directly provide the complete four-class mapping required here; smaller scope and different sensor/camera setup | Not selected as primary |

## 3. Selected primary dataset — BDD100K

**Owner decision (2026-11-19): BDD100K is approved as the primary dataset for the initial detector baseline.** MIO-TCD is optional for a later, separately reviewed experiment and is excluded from the initial baseline. This decision approves the dataset choice for planning; it does not authorize downloading or processing the data.

Official resources:
- Dataset and download documentation: https://github.com/bdd100k/bdd100k/blob/master/doc/source/download.rst
- Official toolkit and task descriptions: https://github.com/bdd100k/bdd100k
- Label format and class definitions: https://github.com/bdd100k/bdd100k/blob/master/doc/source/format.rst
- Dataset license: https://github.com/bdd100k/bdd100k/blob/master/doc/source/license.rst
- Dataset paper: https://openaccess.thecvf.com/content_CVPR_2020/html/Yu_BDD100K_A_Diverse_Driving_Dataset_for_Heterogeneous_Multitask_Learning_CVPR_2020_paper.html

BDD100K is the selected initial fit because it is a driving dataset, includes the four required vehicle categories in its object-detection labels, and provides a separate multi-object box-tracking task. Its images are 1280×720 and the dataset includes scene, weather and time-of-day diversity. The official download documentation describes the 100K Images package as frames sampled at the 10th second of the videos; image train/validation/test splits follow the corresponding video splits.

### 3.1 Required packages and acquisition boundary

The official download documentation currently lists these packages for the initial image-detection baseline:

| Package | Documented size | Published MD5 | Purpose |
|---|---:|---|---|
| 100K Images | 5.3 GB | `5a0359c86a0b8713adab1eee9a3041cb` | Detection images |
| Detection 2020 Labels | 53 MB | `b86a3e1b7edbcad421b7dad2b3987c94` | Revised detection annotations |

The documentation recommends Detection 2020 Labels over the legacy 2018 detection labels. It lists `det_train.json` and `det_val.json` in the `labels/det_20` package. The full 100K video archive is approximately 1.8 TB and is not required for the first image-detection baseline.

The official documentation publishes MD5 values for these archives. It does not list SHA-256 values in the package table. After a separately approved acquisition, verify the published MD5 and calculate SHA-256 locally for the project manifest.

**Availability status:** The official documentation lists the required packages and their checksums. Actual download endpoint availability, account/access requirements, and successful retrieval have not been tested. Confirm those in P5.2 before acquisition. Do not treat a documentation listing as proof that the download endpoint is currently reachable.

Acquisition scope for a future, separately approved task:
1. Obtain only **100K Images** and **Detection 2020 Labels** for the initial detector dataset.
2. Do not obtain the full video archive for the first detector experiment.
3. Do not obtain MIO-TCD as part of the initial baseline.
4. For later tracking work, separately review and approve the **MOT 2020 Images** and **MOT 2020 Labels** packages. The official documentation describes MOT 2020 as a video subset resampled to 5 Hz; its labels are a separate task-specific package.
5. Record exact package names, source URLs, acquisition date, archive sizes, checksums and license notice in the experiment manifest.

### 3.2 Class mapping

The official BDD100K object-detection category IDs start at **1**, not 0. The four project classes map as follows:

| Project class | BDD100K category | Official BDD100K category ID | Project class ID |
|---|---|---:|---:|
| car | car | 3 | 0 |
| motorcycle | motorcycle | 7 | 1 |
| bus | bus | 5 | 2 |
| truck | truck | 4 | 3 |

Map only these four categories for the initial project detector. Ignore other categories for training unless a later requirement explicitly adds them. Preserve the original category names and IDs in the conversion manifest. The mapping is based on the official detection category list; actual annotation counts and presence in each downloaded split remain to be verified after acquisition.

### 3.3 Annotation representation

BDD100K detection annotations use a Scalabel-compatible JSON structure. The official format describes a JSON list of frame records. Relevant fields include:
- `name`: image/frame name.
- `videoName`: optional source-video identifier.
- `frameIndex`: optional frame index.
- `labels`: object annotations.
- `labels[].category`: source category name.
- `labels[].box2d`: bounding-box coordinates `x1`, `y1`, `x2`, `y2`.
- `labels[].attributes`: may include `occluded` and `truncated`.

The official format allows optional fields, so the conversion must not assume that every record contains a video identifier, frame index or every attribute. Confirm the exact schema of the downloaded Detection 2020 JSON before implementing the converter. Do not assume that the field names or coordinate conventions match the target detector format without an explicit conversion test.

### 3.4 Split strategy and leakage prevention

- Use the official labelled training images as the source training pool.
- Create an internal validation subset from the official training pool using a fixed, recorded seed.
- Keep the official labelled validation split untouched as the project's held-out detector evaluation split. Do not call it BDD100K's official test set.
- The selected Detection 2020 package documents `det_train.json` and `det_val.json`. It does not list a labelled `det_test.json`; do not invent test ground truth or report metrics on images without annotations.
- Where source-video identifiers are available, keep all images from one source video in only one project split. This reduces leakage from correlated frames.
- For later tracking work, preserve the official video/sequence split; never split frames from one sequence across train and validation.

The exact split sizes will be recorded after inspecting the downloaded annotations and sequence metadata. If source-video identifiers are missing from the detection labels, document that limitation and use the official image split as supplied rather than claiming sequence-level leakage prevention has been verified.

## 4. Preprocessing plan

1. Verify downloaded archives against the published MD5 values and calculate SHA-256.
2. Validate image decoding, dimensions and annotation references; report missing/corrupt files.
3. Inspect the downloaded JSON schema and convert the Scalabel-compatible bounding boxes into the detector's required format with a deterministic script.
4. Clip boxes to image boundaries and reject invalid/zero-area boxes; log every rejected annotation.
5. Convert coordinates carefully and test the conversion by rendering sample overlays.
6. Resize/letterbox to 640×640 for the first baseline while preserving aspect ratio.
7. Apply training-only augmentation: horizontal flip where appropriate, modest scale/translation, brightness/contrast and HSV changes. Avoid transformations that make road scenes unrealistic.
8. Do not augment validation or held-out evaluation data.
9. Calculate per-class object counts and box-size distributions before training. Address rare motorcycle/bus/truck examples through sampling or loss configuration only after measuring the imbalance.
10. Keep raw data outside Git. Commit only scripts, manifests without restricted data, documentation and small examples only where the applicable terms permit them.

## 5. License and usage gate

The official BDD100K repository states that its code and other repository resources are under the BSD 3-Clause license. It separately states that data and labels downloaded from the BDD data host are under the UC Regents / BAIR Open Research Commons license reproduced in the official license document.

The dataset terms grant permission to use, copy, modify and distribute the data and documentation for **educational, research and not-for-profit purposes**, without a fee or signed licensing agreement, provided the specified copyright notice and license paragraphs are included in copies, modifications and distributions. Commercial-use rights are granted to BDD and BAIR Commons members and their affiliates, with those rights stated as non-transferable. The license directs other commercial licensing inquiries to UC Berkeley's Office of Technology Licensing.

Project actions:
- Keep the dataset license and required copyright notice with experiment records and any permitted copies or distributions.
- Do not assume the toolkit's BSD 3-Clause license applies to the images or labels.
- Do not publish original images or annotations in this GitHub repository.
- Before publicly hosting or distributing dataset-derived artifacts, including model weights, review the exact intended use against the dataset terms and obtain written clarification from the rights holder if the scope is uncertain. The dataset license text alone does not answer every question about public hosting or downstream model-weight distribution.
- Do not use the dataset commercially unless the project qualifies under the stated commercial-use provision or separate written permission is obtained.
- Recheck the official license at acquisition time. This document is a project research record, not legal advice.

## 6. Risks and mitigations

| Risk | Mitigation |
|---|---|
| US dashcam scenes differ from Indian urban roads and fixed CCTV | Evaluate on a small separately collected, properly licensed Indian-road sample before claiming local generalization |
| Class imbalance | Measure per-class counts; report per-class precision/recall and mAP; use balanced sampling only if justified |
| Small/distant vehicles | Inspect box-size distribution; compare 640 and a larger input size only if GPU budget permits |
| Similar frames leak across splits | Group by source video where the annotation metadata supports it; otherwise record the limitation |
| Large download consumes storage/time | Start with labelled images; defer full videos; download MOT subset only for separately approved tracking work |
| Download mirror or endpoint unavailable | Confirm access and retrieval in P5.2 before attempting acquisition |
| Dataset terms constrain downstream use | Preserve notices; review intended public hosting and model distribution; obtain permission where required |

## 7. P5 dataset acceptance criteria

- [x] Primary dataset decision recorded: BDD100K.
- [x] Supplementary MIO-TCD explicitly deferred as optional, not part of the initial baseline.
- [x] Official dataset and license sources recorded.
- [x] Official detection category names and IDs mapped to the four project class IDs.
- [x] Required detection packages, documented sizes and published MD5 values recorded.
- [x] Annotation format and relevant fields documented from the official schema.
- [x] Split strategy and source-video leakage limitation documented.
- [ ] Download endpoint availability and actual archive integrity verified after separate approval.
- [ ] Actual annotation counts, class distribution, image integrity and split manifests captured after acquisition.
- [ ] Annotation conversion and visual spot-check completed.
- [ ] Dataset remains outside Git.

**Status:** BDD100K is the owner-approved primary dataset and its official package documentation, detection categories, annotation format and license terms have been reviewed. It has not been downloaded or processed. Download endpoint availability, actual annotation counts, archive integrity, split integrity and conversion correctness remain unverified.