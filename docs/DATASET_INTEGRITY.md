# Dataset integrity manifests

VeriSlip dataset manifests detect accidental corruption, replacement, deletion,
or addition of JPEG and PNG samples before research or training use. The tool is
read-only with respect to dataset images: it never repairs, rewrites, deletes, or
automatically accepts changed files.

## Manifest format

The deterministic JSON document contains:

- `schema_version`: currently `1`;
- `hash_algorithm`: `sha256`;
- `files`: records sorted by relative POSIX path;
- `duplicates`: groups of different paths with identical SHA-256 content.

Each file record contains its relative path, lowercase SHA-256 checksum, byte
size, decoded width and height, and actual image format. Absolute paths,
timestamps, host details, and image metadata are excluded, so repeated creation
against identical content produces identical manifest bytes.

SHA-256 is calculated with 1 MiB streaming reads. Image validation fully decodes
the file with Pillow and enforces VeriSlip's existing JPEG/PNG, single-frame,
dimension, pixel-count, and decompression-bomb constraints. Validation never
sanitizes or resaves the source image.

## Windows CMD usage

Create a manifest after dataset generation or collection:

```cmd
python scripts\verify_dataset.py create verislip_dataset verislip_dataset.integrity.json
```

Verify the dataset later, before consuming it:

```cmd
python scripts\verify_dataset.py verify verislip_dataset verislip_dataset.integrity.json
```

Successful verification exits with code `0`. Creation or verification failure
exits nonzero. In a batch workflow, inspect `%ERRORLEVEL%`:

```cmd
python scripts\verify_dataset.py verify verislip_dataset verislip_dataset.integrity.json
if errorlevel 1 exit /b 1
```

Manifest creation fails without writing a new manifest if a supported candidate
has invalid content, unsafe dimensions, a decode error, or a symlink. Existing
manifest files are not replaced in that case.

## Interpreting verification failures

| Code | Meaning |
| --- | --- |
| `checksum_mismatch` | File bytes changed after manifest creation. |
| `size_mismatch` | File byte size differs from the manifest. |
| `metadata_mismatch` | Decoded dimensions or actual format changed. |
| `corrupt_file` | The image is malformed, truncated, unsafe, or cannot decode. |
| `missing_file` | A manifest image no longer exists. |
| `unexpected_file` | A supported image exists but is absent from the manifest. |
| `unsafe_path` | A symlink or unsafe filesystem path was found. |
| `malformed_manifest` | JSON, schema, checksum, metadata, or relative path is invalid. |

Problem reports use paths relative to the selected dataset root. Manifest paths
containing absolute locations, Windows drive prefixes, backslashes, or `..`
segments are rejected. Symlinked images are refused, and manifest entries are
matched only against safely discovered files under the dataset root.

Duplicate groups are informational: identical content is not automatically an
integrity failure because paired datasets may intentionally contain equivalent
masks or samples. Review duplicate groups according to the dataset policy.

## Limitations

- Discovery intentionally considers `.jpg`, `.jpeg`, and `.png` files only.
  Other files, including dataset cards and CSV annotations, are outside this
  image-integrity manifest.
- A manifest proves that bytes match a previously recorded local state; it does
  not authenticate who created the manifest. Sign or distribute manifests over
  a trusted channel when provenance matters.
- Filesystem changes made concurrently during a scan can cause a failed or
  subsequently inconsistent verification. Generate datasets first, then create
  the manifest while the dataset is not being modified.
