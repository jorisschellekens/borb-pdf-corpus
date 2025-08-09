# ![borb logo](https://github.com/jorisschellekens/borb/raw/master/logo/borb_square_64_64.png) borb-pdf-corpus

This repository contains a curated corpus of PDF documents and their extracted content, organized to support document analysis, processing, and duplication detection workflows. Each PDF is accompanied by its full text (`txt/`), a first-page extract (`first-page-pdf/` and `first-page-txt/`), and a corresponding SHA-256 digest (`digest/`) for efficient duplication checks. 

```mermaid
---
config:
theme: default
---
graph TD
pdf
pdf --> txt
pdf --> digest
pdf --> first-page
first-page --> first-page-pdf
first-page --> first-page-txt

%% Define classes
classDef gray fill:#ccc,stroke:#999,stroke-width:1px;
classDef highlight fill:#F1CD2E,stroke:#999,stroke-width:2px;

%% Assign classes
class pdf highlight;
class txt,digest,first-page,first-page-pdf,first-page-txt gray;
```

The repository also includes automated metrics to help understand the overall structure, size, and temporal distribution of the documents.

## 1. File Size

| Property      | Value |
| ------------- | ----- |
| Smallest PDF | 2.00 KB |
| Average PDF | 1.48 MB |
| Largest PDF  | 55.19 MB |

## 2. Creation Year

| Property      | Value |
| ------------- | ----- |
| Youngest PDF | 2025 |
| Average PDF | 2015 |
| Oldest PDF  | 1999 |

## 3. Word Count

| Property      | Value |
| ------------- | ----- |
| Largest PDF | 346574 |
| Average PDF | 6682 |
| Smallest PDF  | 14 |

