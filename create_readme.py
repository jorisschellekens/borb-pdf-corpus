import datetime
import os
import pathlib
import re
import typing

ROOT: pathlib.Path = pathlib.Path(__file__).parent
PDF_DIR: pathlib.Path = ROOT / "pdf"
TXT_DIR: pathlib.Path = ROOT / "txt"

def file_size_to_legible(s: int ) -> str:
    # smaller than 1Kb
    if s < 1024:
        return f"{s:.2f} KB"
    # Smaller than 1 Mb
    elif s < 1024 * 1024:
        s /= (1024*1024)
        return f"{s:.2f} MB"
    # Smaller than 1 Gb
    elif s < 1024 * 1024 * 1024:
        s /= (1024*1024)
        return f"{s:.2f} MB"
    # Default
    else:
        s /= (1024*1024*1024)
        return f"{s:.2f} GB"

def get_creation_year(pdf_file: pathlib.Path) -> typing.Optional[int]:
    try:
        from PyPDF2 import PdfReader, DocumentInformation
        reader: PdfReader = PdfReader(pdf_file)
        metadata: typing.Optional[DocumentInformation] = reader.metadata
        creation_date = getattr(metadata, 'creation_date', None) or metadata.get('/CreationDate')
        return creation_date.year
    except:
        return None

def main():
    content: str = ""

    #
    # LOGO
    #

    content += "# ![borb logo](https://github.com/jorisschellekens/borb/raw/master/logo/borb_square_64_64.png) borb-pdf-corpus"
    content += "\n"
    content += "\n"

    #
    # EXPLANATORY PARAGRAPH
    #

    content += "This repository contains a curated corpus of PDF documents and their extracted content, "
    content += "organized to support document analysis, processing, and duplication detection workflows. "
    content += "Each PDF is accompanied by its full text (`txt/`), a first-page extract (`first-page-pdf/` and `first-page-txt/`), "
    content += "and a corresponding SHA-256 digest (`digest/`) for efficient duplication checks. "
    content += "\n"
    content += "\n"

    #
    # DIAGRAM
    #

    content += "```mermaid\n"
    content += "---\n"
    content +=  "config:\n"
    content += "theme: default\n"
    content += "---\n"
    content += "graph TD\n"
    content += "pdf\n"
    content += "pdf --> txt\n"
    content += "pdf --> digest\n"
    content += "pdf --> first-page\n"
    content += "first-page --> first-page-pdf\n"
    content += "first-page --> first-page-txt\n"
    content += "\n"
    content += "%% Define classes\n"
    content += "classDef gray fill:#ccc,stroke:#999,stroke-width:1px;\n"
    content += "classDef highlight fill:#F1CD2E,stroke:#999,stroke-width:2px;\n"
    content += "\n"
    content += "%% Assign classes\n"
    content += "class pdf highlight;\n"
    content += "class txt,digest,first-page,first-page-pdf,first-page-txt gray;\n"
    content += "```\n"
    content += "\n"

    content += "The repository also includes automated metrics to help understand the overall structure, size, and temporal distribution of the documents."
    content += "\n"
    content += "\n"

    #
    # FILE SIZE
    #

    content += "## 1. File Size\n"
    content += "\n"

    largest_size: typing.Optional[int] = None
    smallest_size: typing.Optional[int] = None
    avg_size: int = 0
    count: int = 0
    for f in PDF_DIR.iterdir():
        if not f.is_file():
            continue
        if not f.name.endswith(".pdf"):
            continue
        size: int = os.path.getsize(f)
        avg_size += size
        count += 1
        if largest_size is None or size > largest_size:
            largest_size = size
        if smallest_size is None or size < smallest_size:
            smallest_size = size
    avg_size /= count

    content += "| Property      | Value |\n"
    content += "| ------------- | ----- |\n"
    content += f"| Smallest PDF | {file_size_to_legible(smallest_size)} |\n"
    content += f"| Average PDF | {file_size_to_legible(avg_size)} |\n"
    content += f"| Largest PDF  | {file_size_to_legible(largest_size)} |\n"
    content += "\n"

    #
    # YEAR
    #

    content += "## 2. Creation Year\n"
    content += "\n"

    largest_year: typing.Optional[int] = None
    smallest_year: typing.Optional[int] = None
    avg_year: int = 0
    count: int = 0
    for f in PDF_DIR.iterdir():
        if not f.is_file():
            continue
        if not f.name.endswith(".pdf"):
            continue
        year: typing.Optional[int] =  get_creation_year(f)
        if year is None:
            continue
        avg_year += year
        count += 1
        if largest_year is None or year > largest_year:
            largest_year = year
        if smallest_year is None or year < smallest_year:
            smallest_year = year
    avg_year /= count

    content += "| Property      | Value |\n"
    content += "| ------------- | ----- |\n"
    content += f"| Youngest PDF | {largest_year} |\n"
    content += f"| Average PDF | {int(avg_year)} |\n"
    content += f"| Oldest PDF  | {smallest_year} |\n"
    content += "\n"

    #
    # word count
    #

    content += "## 3. Word Count\n"
    content += "\n"

    largest_word_count: typing.Optional[int] = None
    smallest_word_count: typing.Optional[int] = None
    avg_word_count: int = 0
    count: int = 0
    for f in TXT_DIR.iterdir():
        if not f.is_file():
            continue
        if not f.name.endswith(".txt"):
            continue
        txt: str = ''
        try:
            with open(f, 'r') as fh:
                txt = fh.read()
        except:
            pass
        nof_words: int = len(re.split('[^a-zA-Z0-9]+', txt))
        avg_word_count += nof_words
        count += 1
        if largest_word_count is None or nof_words > largest_word_count:
            largest_word_count = nof_words
        if smallest_word_count is None or nof_words < smallest_word_count:
            smallest_word_count = nof_words
    avg_word_count /= count

    content += "| Property      | Value |\n"
    content += "| ------------- | ----- |\n"
    content += f"| Largest PDF | {largest_word_count} |\n"
    content += f"| Average PDF | {int(avg_word_count)} |\n"
    content += f"| Smallest PDF  | {smallest_word_count} |\n"
    content += "\n"

    #
    # WRITE TO FILE
    #

    with open(ROOT / "README.md", "w") as f:
        f.write(content)

if __name__ == '__main__':
    main()