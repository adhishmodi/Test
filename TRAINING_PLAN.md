# P5 — Training Plan

| Field | Value |
|---|---|
| Project | Intelligent Traffic Monitoring System |
| Phase | P5 — Dataset Research and Model Baseline |
| Status | Proposed; no training has been run |
| Training environment | Google Colab GPU |
| Dataset | BDD100K labelled images (see DATASET_RESEARCH.md) |
| Initial detector | YOLOX-S (see MODEL_BASELINE.md) |

## 1. Training workflow

1. Start a fresh Colab notebook and record the assigned GPU type, available VRAM, RAM and runtime versions.
2. Mount Google Drive for dataset/checkpoint persistence. Do not store large datasets or model weights in Git.
3. Download only the approved BDD100K image and detection-label packages. Verify checksums and retain the dataset license.
4. Run annotation validation and conversion; render random samples with bounding boxes and class labels.
5. Create fixed train/validation/test manifests using the strategy in DATASET_RESEARCH.md.
6. Run a short smoke test to catch path, class-map, memory and loss issues.
7. Train YOLOX-S from the approved COCO-pretrained checkpoint.
8. Select the checkpoint using validation metrics only.
9. Evaluate once on the untouched held-out test split.
10. Save metrics, configuration, logs, environment information and checkpoint checksum to Drive.

## 2. Initial configuration

These are starting values for a pilot, not guaranteed optimal settings.

| Setting | Initial proposal | Adjustment rule |
|---|---|---|
| Model | YOLOX-S | Use Nano/Tiny only if memory or latency requires a smaller model |
| Input size | 640 × 640 | Preserve aspect ratio with letterboxing; test 800 only if small-object performance justifies the cost |
| Pilot epochs | 20 | Smoke test only; not a final performance result |
| Baseline epochs | Up to 100 | Stop earlier if validation stops improving; extend only if learning curves justify it |
| Batch size | Start at 8 | Increase to 16 if GPU memory permits; reduce if CUDA OOM occurs |
| Optimizer | SGD | Follow the selected YOLOX experiment configuration |
| Learning rate | Use the official YOLOX batch-size-scaled starting configuration | Record effective batch size and learning rate; adjust only from observed training behavior |
| Schedule | Warm-up followed by cosine schedule | Keep schedule consistent between candidate comparisons |
| Weight decay | Start from official YOLOX-S experiment defaults | Record any change |
| Precision | Mixed precision (FP16) when supported | Disable if numerical instability occurs |
| Checkpointing | Save latest and best validation checkpoint | Copy checkpoints to Drive during training |
| Randomness | Fixed Python/NumPy/PyTorch seeds where supported | Record seed and acknowledge nondeterministic GPU operations |

The YOLOX custom-training guide documents COCO-pretrained initialization, custom experiment configuration and its training options. Prefer the official experiment defaults as the first reproducible baseline instead of inventing a complex hyperparameter search.

Official guide: https://github.com/Megvii-BaseDetection/YOLOX/blob/main/docs/train_custom_data.md

## 3. Data augmentation

Apply augmentation only to training data:
- Horizontal flip.
- Moderate scale and translation.
- Mild HSV/brightness/contrast variation.
- YOLOX-supported Mosaic and MixUp where appropriate.

Do not use vertical flips or aggressive transformations that create implausible road scenes. Keep validation and test images unchanged. If augmentation causes poor small-object localization or unrealistic samples, reduce its strength and document the change.

## 4. Class imbalance

Before training, count objects per class and inspect bounding-box sizes. Cars may dominate; do not assume class balance.

If imbalance is substantial:
1. Report the distribution.
2. Inspect motorcycle, bus and truck examples manually.
3. Consider class-aware sampling or loss adjustments only after the baseline.
4. Report per-class AP/recall so overall mAP does not hide weak minority-class performance.

Do not duplicate validation/test examples or move samples between splits to improve reported metrics.

## 5. Validation and checkpoint selection

- Evaluate on the validation split at the configured interval.
- Save the checkpoint with the best validation metric (record which metric is used).
- Monitor per-class AP, precision/recall and validation loss.
- Check for overfitting by comparing training and validation curves.
- Do not tune hyperparameters on the held-out test set.
- Run the final test evaluation once the configuration is frozen.

If the training framework does not implement early stopping, use a fixed epoch budget and best-validation-checkpoint selection rather than claiming automatic early stopping.

## 6. Colab resource and recovery strategy

Colab GPU availability and session duration vary. At the start of every run:
- Record GPU model, VRAM and CUDA/PyTorch versions.
- Run a one-batch memory test.
- Begin with batch size 8 and adjust based on measured memory.
- Use mixed precision only if supported and stable.
- Save checkpoints and logs to persistent Drive storage at regular intervals.
- Keep a copy of the exact experiment configuration and dataset manifest beside each run.
- Resume only from a checkpoint with a matching configuration; document any changed settings.

If the selected Colab GPU is insufficient, reduce batch size first. Reduce image size only after recording the accuracy trade-off. Do not silently change input size or split between runs.

## 7. Reproducibility record

For every run, record:
- Run ID and date.
- Git commit SHA for the training code/configuration.
- Dataset source, download date, license and archive checksums.
- Split-manifest checksum and random seed.
- Class mapping and annotation-conversion version.
- Model architecture, pretrained checkpoint source and checksum.
- Python, PyTorch, CUDA and YOLOX versions.
- GPU model, VRAM, image size, batch size and epoch count.
- Optimizer, learning rate, scheduler, augmentation and precision settings.
- Best epoch and validation metrics.
- Final held-out test metrics.
- Inference latency/FPS measurement conditions.

## 8. Outputs and storage

Keep outputs outside Git:
- Dataset files and converted annotations.
- Training logs and TensorBoard/W&B artifacts, if used.
- Latest and best checkpoints.
- Evaluation predictions and confusion matrices.
- Exported inference weights.

Commit only code, small configuration files, manifests without private data, and summarized reports. Before sharing weights publicly, confirm the checkpoint, training-code, pretrained-data and fine-tuning-dataset terms allow it.

## 9. P5 completion versus later implementation

P5 can be closed when the dataset/model choices, preprocessing design, training configuration and benchmark protocol are approved and documented. Actual training, metric collection, tracker integration and model packaging belong to later implementation/evaluation tasks (P6/P7).

## 10. Training acceptance criteria

- [ ] Colab GPU is inspected and recorded before selecting final batch size.
- [ ] Dataset and annotations pass validation and visual spot checks.
- [ ] Split manifests are fixed and leakage checks are documented.
- [ ] Smoke-test configuration and full baseline configuration are saved.
- [ ] Training run can be resumed from persistent checkpoints.
- [ ] Best-checkpoint selection uses validation data only.
- [ ] Held-out test metrics are not used for tuning.
- [ ] Model/data/package licenses are reviewed before distribution.
- [ ] No training has been claimed as complete until logs and outputs exist.

**Status:** Planning only. No dataset download, dependency installation, model training or benchmark execution was performed while preparing this document.
