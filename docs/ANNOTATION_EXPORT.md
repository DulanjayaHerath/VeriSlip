# Synthetic annotation export

VeriSlip can export its offline synthetic receipt annotations as COCO JSON or
Pascal VOC XML. The exporter is dataset tooling only: it does not run, train,
or modify any neural network.

## Source format

`scripts/generate_kaggle_dataset.py` creates the canonical input:

- `dataset_metadata.csv` contains relative image and mask filenames,
  `is_tampered`, `tamper_type`, and `bbox_x`, `bbox_y`, `bbox_w`, `bbox_h`.
- `images/` contains the generated receipt images.
- `masks/` contains genuine one-channel binary masks, where non-zero pixels
  identify generated tampering.

The native `SyntheticSlipGenerator` metadata is also supported by the reusable
Python adapter `normalize_generator_annotation`. Its `ground_truth_boxes` are
already `[x, y, width, height]` dictionaries and are not replaced with a new
generator representation.

## Deterministic mapping

Images are ordered by their relative POSIX-style dataset path. Categories are
the concrete `tamper_type` values present in the metadata, sorted by name and
assigned one-based IDs. Authentic rows (`NONE`) create an image entry without
an object annotation. Image and annotation IDs are assigned sequentially after
sorting, so identical inputs produce identical output.

COCO bounding boxes use `[x, y, width, height]`; `area` is `width * height`.
Pascal VOC files use `xmin`, `ymin`, `xmax`, `ymax`. Fractional VOC coordinates
are rounded outward so the annotated region is not reduced.

Negative origins and right/bottom overflow are clipped to the actual decoded
image dimensions. Non-finite values, non-positive widths or heights, boxes
entirely outside the image, malformed rows, unsafe paths, and mismatched masks
fail the export instead of being silently converted into training data.

## Segmentation

When a metadata row references an actual binary mask, COCO receives that mask
as deterministic, uncompressed, column-major run-length encoding. The exporter
does not invent polygons from bounding boxes. If no mask is referenced, the
object remains a valid bounding-box annotation without a `segmentation` field.
Pascal VOC has no standard instance-mask field, so its output contains boxes
and reports whether source segmentation was available.

## Windows CMD usage

Create COCO JSON:

```cmd
python scripts\export_annotations.py verislip_dataset --format coco --output exports\annotations.json
```

Create Pascal VOC XML files (relative subdirectories are retained):

```cmd
python scripts\export_annotations.py verislip_dataset --format voc --output exports\voc
```

Create both formats:

```cmd
python scripts\export_annotations.py verislip_dataset --format both --output exports
```

Existing exporter-owned files are not replaced unless `--overwrite` is given.
Source images, masks, and metadata are always read-only.

## Output examples

A COCO annotation resembles:

```json
{
  "id": 1,
  "image_id": 1,
  "category_id": 1,
  "bbox": [50, 210, 320, 43],
  "area": 13760,
  "iscrowd": 0,
  "segmentation": {"size": [740, 420], "counts": [15500, 43]}
}
```

The displayed RLE counts are abbreviated; real counts span the full mask.
Pascal VOC emits one UTF-8 XML document per image with its decoded size and one
`object/bndbox` node per tamper annotation.

## Limitations

- The current packaged generator writes one primary bounding box per CSV row.
  The normalization layer supports repeated image rows when multiple boxes are
  available.
- COCO segmentation is emitted only from a real mask supplied by the dataset
  or generator caller. Bounding-box-only legacy rows remain box-only.
- Mask-to-instance separation is not inferred when one combined mask is reused
  for several object rows; producers should provide an object-specific mask for
  each such row.
- Export validates annotation geometry and basic image decoding but does not
  replace `scripts\verify_dataset.py` checksum verification.

