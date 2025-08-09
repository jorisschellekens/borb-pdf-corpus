import pathlib
import shutil
import typing

SRC_DIR: pathlib.Path = pathlib.Path("/home/joris-schellekens/Code/borb-pdf-corpus-002/pdf")

DIGEST_DIR: pathlib.Path = pathlib.Path(__file__).parent / "digest"
FIRST_PAGE_PDF_DIR: pathlib.Path = pathlib.Path(__file__).parent / "first-page-pdf"
FIRST_PAGE_TXT_DIR: pathlib.Path = pathlib.Path(__file__).parent / "first-page-txt"
PDF_DIR: pathlib.Path = pathlib.Path(__file__).parent / "pdf"
TXT_DIR: pathlib.Path = pathlib.Path(__file__).parent / "txt"

#
# PRIVATE
#


def __get_digest(file: pathlib.Path) -> str:
    import hashlib

    hasher = hashlib.sha256()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def __store_text(src_file: pathlib.Path, dst_name: str) -> None:
    from PyPDF2 import PdfReader

    txt_in_pdf: str = ""
    try:
        reader = PdfReader(src_file)
        txt_in_pdf = "\n".join(page.extract_text() or "" for page in reader.pages)
    except:
        pass
    with open(TXT_DIR / dst_name, "w") as fh:
        fh.write(txt_in_pdf)


def __store_first_page_pdf(src_file: pathlib.Path, dst_name: str) -> None:
    from PyPDF2 import PdfReader, PdfWriter

    try:
        reader = PdfReader(src_file)
        writer = PdfWriter()
        writer.add_page(reader.pages[0])
        with open(FIRST_PAGE_PDF_DIR / dst_name, "wb") as f:
            writer.write(f)
    except:
        pass


def __store_first_page_txt(src_file: pathlib.Path, dst_name: str) -> None:
    from PyPDF2 import PdfReader

    txt_in_pdf: str = ""
    try:
        reader = PdfReader(src_file)
        txt_in_pdf = reader.pages[0].extract_text()
    except:
        pass
    with open(FIRST_PAGE_TXT_DIR / dst_name, "w") as fh:
        fh.write(txt_in_pdf)


#
# PUBLIC
#


def main():

    # find all PDF file(s)
    pdfs_to_do: typing.List[pathlib.Path] = []
    if SRC_DIR.is_file():
        pdfs_to_do += [SRC_DIR]
    if SRC_DIR.is_dir():
        pdfs_to_do += [x for x in SRC_DIR.iterdir()]
    pdfs_to_do = [x for x in pdfs_to_do if x.suffix == ".pdf"]

    # easy out
    if len(pdfs_to_do) == 0:
        return

    # get all digests
    pdf_digests: typing.List[str] = []
    for digest_file in DIGEST_DIR.iterdir():
        try:
            with open(digest_file, "r") as fh:
                pdf_digests += [fh.read()]
        except:
            pass

    # process
    for pdf_file in pdfs_to_do:

        # calculate digest
        new_digest: str = __get_digest(pdf_file)

        # IF the digest already exists
        # THEN display warning AND continue
        if new_digest in pdf_digests:
            print(f"DUPLICATE {pdf_file.name}")
            continue

        # determine the new filename
        n: int = 0
        while (PDF_DIR / f"{n:04d}.pdf").exists():
            n += 1

        # store digest
        print(f"Processing {pdf_file}:")
        print(f"\tdigest          : {n:04d}.sha256")
        with open(DIGEST_DIR / f"{n:04d}.sha256", "w") as fh:
            fh.write(new_digest)

        # store PDF
        print(f"\tcopy            : {n:04d}.pdf")
        shutil.copy(pdf_file, PDF_DIR / f"{n:04d}.pdf")

        # store txt
        print(f"\ttext            : {n:04d}.txt")
        __store_text(src_file=pdf_file, dst_name=f"{n:04d}.txt")

        # store first-page-pdf

        print(f"\tfirst-page-pdf  : {n:04d}.pdf")
        __store_first_page_pdf(src_file=pdf_file, dst_name=f"{n:04d}.pdf")

        # store first-page-txt
        print(f"\tfirst-page-txt  : {n:04d}.pdf")
        __store_first_page_txt(src_file=pdf_file, dst_name=f"{n:04d}.txt")


if __name__ == "__main__":
    main()
