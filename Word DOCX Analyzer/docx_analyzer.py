import argparse
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WORD_TAG = "{" + WORD_NAMESPACE + "}"
WORD_PATTERN = re.compile(r"\b[\w]+(?:['’][\w]+)*\b", re.UNICODE)


def _paragraph_text(paragraph):
    """Extract text from a Word paragraph, preserving tabs and line breaks."""
    text_parts = []

    def visit(element):
        for child in element:
            # Text boxes can contain nested paragraphs. They are counted as
            # their own paragraphs, so don't include their text twice here.
            if child.tag == WORD_TAG + "p":
                continue
            if child.tag == WORD_TAG + "t":
                text_parts.append(child.text or "")
            elif child.tag == WORD_TAG + "tab":
                text_parts.append("\t")
            elif child.tag in (WORD_TAG + "br", WORD_TAG + "cr"):
                text_parts.append("\n")
            else:
                visit(child)

    visit(paragraph)
    return "".join(text_parts)


def analyze_docx(file_path):
    """Count body paragraphs, words, and characters in a .docx document."""
    file_path = Path(file_path)
    if file_path.suffix.lower() != ".docx":
        raise ValueError("The input file must have a .docx extension.")
    if not file_path.is_file():
        raise FileNotFoundError("The input file does not exist or is not a file.")

    try:
        with zipfile.ZipFile(file_path) as package:
            document_xml = package.read("word/document.xml")
    except (OSError, KeyError, zipfile.BadZipFile) as error:
        raise ValueError("The file is not a valid DOCX document.") from error

    try:
        root = ET.fromstring(document_xml)
    except ET.ParseError as error:
        raise ValueError("The DOCX document contains invalid document XML.") from error

    body = root.find(".//" + WORD_TAG + "body")
    if body is None:
        raise ValueError("The DOCX document does not contain a document body.")

    paragraphs = [
        _paragraph_text(paragraph)
        for paragraph in body.iter(WORD_TAG + "p")
    ]

    return {
        "paragraphs": len(paragraphs),
        "words": sum(len(WORD_PATTERN.findall(text)) for text in paragraphs),
        "characters": sum(len(text) for text in paragraphs),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Count paragraphs, words, and characters in a DOCX file."
    )
    parser.add_argument("file", type=Path, help="Path to the .docx file")
    args = parser.parse_args()

    try:
        counts = analyze_docx(args.file)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Paragraphs: {counts['paragraphs']}")
    print(f"Words: {counts['words']}")
    print(f"Characters: {counts['characters']}")


if __name__ == "__main__":
    main()
