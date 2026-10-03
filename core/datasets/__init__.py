"""Dataset preparation and integrity infrastructure."""

from core.datasets.annotations import (
    AnnotationDataset,
    AnnotationExportError,
    BinaryMask,
    NormalizedImage,
    NormalizedObject,
    build_coco,
    build_voc_xml,
    load_annotation_dataset,
    normalize_generator_annotation,
    write_coco,
    write_voc,
)
from core.datasets.integrity import (
    DatasetIntegrityError,
    IntegrityIssue,
    VerificationResult,
    build_manifest,
    compute_sha256,
    verify_dataset,
    write_manifest,
)

__all__ = [
    "AnnotationDataset",
    "AnnotationExportError",
    "BinaryMask",
    "DatasetIntegrityError",
    "IntegrityIssue",
    "NormalizedImage",
    "NormalizedObject",
    "VerificationResult",
    "build_manifest",
    "build_coco",
    "build_voc_xml",
    "compute_sha256",
    "load_annotation_dataset",
    "normalize_generator_annotation",
    "verify_dataset",
    "write_manifest",
    "write_coco",
    "write_voc",
]
