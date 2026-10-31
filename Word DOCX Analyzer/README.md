# Word DOCX Analyzer

A command-line utility that counts the paragraphs, words, and characters in a
Microsoft Word `.docx` document.

## Requirements

- Python 3.6 or newer
- No third-party packages (uses only the Python standard library)

## Usage

From the repository root, run:

```bash
python "Word DOCX Analyzer/docx_analyzer.py" path/to/document.docx
```

The program reports the counts in the terminal. It counts paragraphs in the
document body, including paragraphs in tables and empty paragraphs. Word counts
are based on sequences of letters or numbers; characters include spaces, tabs,
and line breaks within paragraphs. Paragraph separators, headers, and footers
are not included in the character count.

## Tests

Run the unit tests from the repository root with:

```bash
python -m unittest discover -s "Word DOCX Analyzer" -p "test_*.py"
```
