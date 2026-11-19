# P5.1 — Dataset Readiness and Licensing Record

| Field | Value |
|---|---|
| Project | Intelligent Traffic Monitoring System |
| Phase / batch | P5 — Dataset Research and Model Baseline / P5.1 |
| Status | Documentation review prepared; awaiting PR review |
| Primary dataset | BDD100K |
| Research date | 2026-11-19 |
| Acquisition status | Not downloaded; no data access attempted |

## 1. Purpose and scope

This record defines the readiness checks required before acquiring BDD100K for the initial four-class vehicle detector baseline.

**Approved project choices:**
- Primary dataset: BDD100K.
- Project classes: car, motorcycle, bus and truck.
- Project class IDs: car=0, motorcycle=1, bus=2, truck=3.
- Initial detector baseline: YOLOX-S (documented separately).
- MIO-TCD: optional future dataset; excluded from the initial baseline.

This P5.1 batch is documentation-only. It does not authorize dataset downloads, dependency installation, annotation conversion, model benchmarking, training or application implementation.

## 2. Official package acquisition checklist

The official BDD100K download documentation currently lists the following required packages:

| Package | Documented size | Published MD5 | Required now? |
|---|---:|---|---|
| 100K Images | 5.3 GB | `5a0359c86a0b8713adab1eee9a3041cb` | Yes |
| Detection 2020 Labels | 53 MB | `b86a3e1b7edbcad421b7dad2b3987c94` | Yes |
| 100K video clips | 1.8 TB | `253d9a2f9d89d2b09d8d93f397aecdd7` | No |
| MOT 2020 Labels | 115 MB | `6be40e0ca56a83ddeba2ed6bff50f9e6` | No; later tracking review |
| MOT 2020 Images | Not specified in the cited package table | Not specified | No; later tracking review |

Official download documentation:
https://github.com/bdd100k/bdd100k/blob/master/doc/source/download.rst

### Package selection notes

- Use **Detection 2020 Labels**, not the legacy 2018 detection label archive. The official documentation recommends the 2020 labels and marks the original detection set as deprecated.
- The documented label package contains `det_train.json` and `det_val.json`.
- The 100K Images package consists of frames sampled at the 10th second in the videos. The image split follows the corresponding video split.
- The full video archive is unnecessary for the initial image-based detector baseline.
- MOT 2020 is a separate tracking task, sampled at 5 Hz. It is not part of the initial detector acquisition.

### Availability and integrity status

| Check | Current status | Evidence / next action |
|---|---|---|
| Official package listing | Documented | Official download documentation lists both required packages |
| Package sizes | Documented | 5.3 GB images; 53 MB Detection 2020 labels |
| Published archive checksums | Documented | MD5 values recorded above |
| Live download endpoint | Not verified | Check access only after P5.2 approval |
| Actual downloaded file sizes | Not applicable | No files downloaded |
| MD5 verification | Not executed | Run after separately approved acquisition |
| SHA-256 calculation | Not executed | Calculate after acquisition; official package table lists MD5, not SHA-256 |
| Extracted storage requirement | Unknown | Measure after acquisition; compressed size is not extracted size |

**P5.2 gate:** Before acquisition, confirm the official endpoint is reachable and the approved packages can be retrieved. If the endpoint is unavailable or requires unexpected access, stop and report the blocker rather than switching to an unofficial mirror without review.

## 3. License record

### 3.1 Separate code and data terms

The official BDD100K repository states:
- Repository code and other repository resources: BSD 3-Clause.
- Dataset images and labels downloaded from the BDD data host: separate UC Regents / BAIR Open Research Commons license.

Official license:
https://github.com/bdd100k/bdd100k/blob/master/doc/source/license.rst

### 3.2 Dataset permissions and restrictions

The official dataset license grants permission to use, copy, modify and distribute the data and documentation for **educational, research and not-for-profit purposes**, without a fee or signed licensing agreement, provided the required copyright notice and license paragraphs appear in all copies, modifications and distributions.

The license separately grants commercial-use rights to BDD and BAIR Commons members and their affiliates, with those rights stated as non-transferable. It refers other commercial licensing inquiries to UC Berkeley's Office of Technology Licensing.

### 3.3 Project handling requirements

1. Retain the full dataset license and required copyright notice with experiment records and any permitted copies or distributions.
2. Do not treat the BSD 3-Clause repository license as the dataset license.
3. Do not commit original images or annotations to this GitHub repository.
4. Before publicly hosting or distributing dataset-derived artifacts, including model weights, review the intended use against the dataset terms. Obtain written clarification from the rights holder if public hosting or downstream distribution is not clearly covered.
5. Do not use the dataset commercially unless the project qualifies under the stated commercial-use provision or separate written permission is obtained.
6. Recheck the license at acquisition time because the terms in force at that time govern the project.

**Unresolved legal/product question:** The license text permits distribution for educational, research and not-for-profit purposes subject to notice conditions, but it does not explicitly resolve every scenario involving a publicly accessible application, hosted inference, or redistribution of fine-tuned model weights. The public-demo plan must be reviewed against the precise deployment and artifact-sharing behavior before release. This record is not legal advice.

## 4. Official annotation schema and class mapping

### 4.1 Detection categories

The official BDD100K detection schema defines these category IDs (starting at 1):

| Official category ID | BDD100K category |
|---:|---|
| 1 | pedestrian |
| 2 | rider |
| 3 | car |
| 4 | truck |
| 5 | bus |
| 6 | train |
| 7 | motorcycle |
| 8 | bicycle |
| 9 | traffic light |
| 10 | traffic sign |

Official format:
https://github.com/bdd100k/bdd100k/blob/master/doc/source/format.rst

### 4.2 Approved project mapping

| Project class ID | Project class | Official BDD100K category | Official category ID |
|---:|---|---|---:|
| 0 | car | car | 3 |
| 1 | motorcycle | motorcycle | 7 |
| 2 | bus | bus | 5 |
| 3 | truck | truck | 4 |

Do not confuse the official one-based category IDs with the project zero-based IDs. Keep both in the conversion manifest.

### 4.3 Relevant annotation fields

The official format is compatible with Scalabel JSON. Relevant fields include:

| Field | Meaning | Handling note |
|---|---|---|
| `name` | Frame/image name | Use to resolve image references |
| `videoName` | Optional source-video name | Use for grouping/leakage checks when present |
| `frameIndex` | Optional frame index | Preserve when present |
| `labels` | List of object annotations | Iterate per object |
| `labels[].category` | Source category name | Map only the four approved classes |
| `labels[].box2d` | 2D bounding box | Convert x1/y1/x2/y2 carefully |
| `labels[].attributes.occluded` | Occlusion flag | Preserve for analysis if present |
| `labels[].attributes.truncated` | Truncation flag | Preserve for analysis if present |

The official schema describes `box2d` as pixel coordinates `x1`, `y1`, `x2`, `y2`. Optional fields may be absent. The exact downloaded Detection 2020 JSON must be inspected before implementation; this document does not claim that the package has already been parsed.

## 5. Split and leakage policy

The planned split design is:

```text
Official labelled BDD100K training pool
    ├── Project training subset
    └── Internal validation subset
         (fixed seed; grouped by source video where metadata permits)

Official labelled BDD100K validation split
    └── Held-out project detector evaluation
        (kept untouched during training/configuration selection)

Official BDD100K test images
    └── Not used for metrics unless valid ground truth is separately available
```

Rules:
- The official Detection 2020 package documents `det_train.json` and `det_val.json`; it does not list a labelled `det_test.json`.
- Do not call the project's held-out BDD validation split the official BDD test set.
- Do not report metrics on images without ground-truth annotations.
- Where `videoName` or equivalent source identifiers exist, assign all images from a source video to one project split.
- If source-video identifiers are unavailable in the selected labels, record that limitation and do not claim sequence-level leakage checks passed.
- Preserve official video/sequence boundaries for later tracking evaluation.

## 6. Storage and manifest specification

### 6.1 Proposed storage layout

Keep data in Google Drive for the Colab workflow, outside Git:

```text
Google Drive/
└── ML_Project_2/
    └── datasets/
        └── bdd100k/
            ├── archives/
            ├── raw/
            │   ├── images/
            │   └── labels/
            ├── processed/
            ├── manifests/
            └── reports/
```

This is a proposed layout only. It has not been created.

### 6.2 Manifest fields

The dataset manifest should record:

| Field | Required | Description |
|---|---|---|
| dataset_name | Yes | BDD100K |
| dataset_release_or_package | Yes | Exact official package name |
| source_url | Yes | Official source URL |
| download_date_utc | Yes | Date acquired |
| license_url | Yes | Official license reference |
| license_notice_retained | Yes | Whether required notice was retained |
| archive_filename | Yes | Exact downloaded filename |
| archive_size_bytes | Yes | Actual size |
| published_md5 | Yes | Official MD5, where published |
| calculated_md5 | Yes | Locally calculated MD5 |
| calculated_sha256 | Yes | Locally calculated SHA-256 |
| extracted_size_bytes | After extraction | Actual extracted size |
| image_count | After validation | Number of images found |
| annotation_file | Yes | JSON file name |
| source_split | Yes | Official train/validation/test identity |
| project_split | After split creation | Project train/internal-val/held-out evaluation |
| source_video_id | If available | Source sequence/video identifier |
| class_mapping_version | Yes | Version of project class mapping |
| validation_status | After validation | Pending/pass/fail with report reference |

Do not put original image bytes, annotations, credentials or private download links into the Git manifest. A sanitized manifest template may be committed later.

## 7. P5.1 readiness checklist

| Readiness item | Result |
|---|---|
| Owner-approved primary dataset recorded | Complete |
| Required detection packages identified | Complete |
| Official package sizes and MD5 values recorded | Complete |
| Legacy versus Detection 2020 labels distinguished | Complete |
| Four required categories mapped with official IDs | Complete |
| Scalabel JSON fields and box representation documented | Complete |
| Dataset license separated from repository code license | Complete |
| Educational/research/not-for-profit permissions and commercial restrictions recorded | Complete |
| Public hosting/model-weight distribution ambiguity flagged | Complete |
| Storage layout and manifest fields specified | Complete |
| Live download endpoint tested | Not executed |
| Dataset downloaded | Not executed |
| Archive hashes verified | Not executed |
| Image/annotation integrity inspected | Not executed |
| Class counts and split manifests produced | Not executed |

## 8. Handoff to P5.2

P5.2 is a separate acquisition batch and requires explicit approval. Before any download:
1. Reconfirm the official package listing and license.
2. Check endpoint availability and access requirements.
3. Confirm available Google Drive storage.
4. Confirm exact packages and expected compressed sizes.
5. Obtain approval to download only 100K Images and Detection 2020 Labels.
6. After acquisition, verify MD5 and calculate SHA-256; record actual sizes and integrity results.

**Current result:** P5.1 documentation readiness is prepared. No data was downloaded, no dependency was installed, no code or training was executed, and no dataset files were added to Git.