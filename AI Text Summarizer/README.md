# AI Text Summarizer

## Overview

A simple, beginner-friendly command-line tool that summarizes text files by extracting the most important sentences. This tool helps you quickly understand the main points of large text documents without reading the entire content.

## Features

- **Easy to Use**: Simple command-line interface with clear instructions
- **Customizable**: Choose how many sentences you want in your summary
- **Smart Extraction**: Automatically identifies and extracts key sentences
- **Error Handling**: Gracefully handles missing files, empty files, and permission errors
- **Clean Output**: Displays summary with statistics (original length, summary length, reduction percentage)
- **No Dependencies**: Uses only Python standard library - no external packages required!

## Prerequisites

- Python 3.6 or higher

## Installation

1. Clone or download this repository
2. Navigate to the `AI Text Summarizer` folder
3. No additional packages to install!

## Usage

### Basic Usage

Summarize a text file with default settings (3 sentences):

```bash
python main.py yourfile.txt
```

### Custom Number of Sentences

Specify how many sentences you want in the summary:

```bash
python main.py yourfile.txt --sentences 5
```

Or use the short form:

```bash
python main.py yourfile.txt -s 2
```

### Examples

```bash
# Summarize an article with 3 sentences
python main.py article.txt

# Summarize a story with 5 sentences
python main.py story.txt --sentences 5

# Quick summary with just 1 sentence
python main.py document.txt -s 1
```

## How It Works

1. **File Reading**: The tool reads your text file using UTF-8 encoding
2. **Text Processing**: Removes extra whitespace and normalizes the text
3. **Sentence Extraction**: Intelligently splits the text into sentences using punctuation marks (., !, ?)
4. **Summary Generation**: Selects the first N sentences based on your preference
5. **Output Display**: Shows the summary with helpful statistics

## Example Output

```
======================================================================
TEXT SUMMARY
======================================================================

This is the first sentence of the document. This is the second
sentence with important information. Here is the third sentence
that concludes the main idea.

----------------------------------------------------------------------
Original length: 1247 characters
Summary length: 156 characters
Reduction: 87.5%
======================================================================
```

## Error Handling

The tool handles common errors gracefully:

- **File not found**: Clear message indicating the file doesn't exist
- **Empty file**: Informs you when the file is empty or contains only whitespace
- **Permission denied**: Alerts you if the file can't be read due to permissions
- **Invalid arguments**: Validates that the number of sentences is at least 1

## Sample Test

Create a test file to try the summarizer:

```bash
echo "Python is a high-level programming language. It is known for its simplicity and readability. Python is widely used in web development, data science, and automation. The language was created by Guido van Rossum in 1991. Today, Python is one of the most popular programming languages in the world." > test.txt

python main.py test.txt
```

## Future Enhancements

Potential improvements for future versions:

- AI-powered summarization using NLP techniques
- Support for multiple file formats (PDF, DOCX, etc.)
- Keyword extraction
- Summary quality scoring
- Export summary to file

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## License

This project is open source and available for educational purposes.

## Author

Created by **Dimas D. Angga** as a contribution to the Python-Scripts repository.
