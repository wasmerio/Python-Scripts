#!/usr/bin/env python3
"""
AI Text Summarizer
A simple command-line tool to summarize text files.
Author: Dimas D. Angga
"""

import argparse
import sys
import os


def read_file(file_path):
    """
    Reads the content of a text file.

    Args:
        file_path (str): Path to the text file

    Returns:
        str: Content of the file

    Raises:
        FileNotFoundError: If the file doesn't exist
        PermissionError: If the file can't be read
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")
    except PermissionError:
        raise PermissionError(f"Error: Permission denied to read '{file_path}'.")
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")


def summarize_text(text, num_sentences=3):
    """
    Creates a simple summary by extracting the first few sentences.

    Args:
        text (str): The text to summarize
        num_sentences (int): Number of sentences to include in the summary

    Returns:
        str: The summarized text
    """
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())

    # Check if text is empty
    if not text.strip():
        return "Error: The file is empty or contains only whitespace."

    # Split text into sentences (simple approach using common sentence endings)
    sentences = []
    temp_sentence = ""

    for char in text:
        temp_sentence += char
        # Check for sentence ending punctuation followed by space or end of text
        if char in '.!?' and (len(temp_sentence) > 1):
            sentences.append(temp_sentence.strip())
            temp_sentence = ""

    # Add any remaining text as a sentence
    if temp_sentence.strip():
        sentences.append(temp_sentence.strip())

    # If no sentences were found, return the first N words
    if not sentences:
        words = text.split()
        if len(words) <= 50:
            return text
        return ' '.join(words[:50]) + "..."

    # Return the first N sentences
    if len(sentences) <= num_sentences:
        summary = ' '.join(sentences)
    else:
        summary = ' '.join(sentences[:num_sentences])

    return summary


def format_output(summary, original_length, summary_length):
    """
    Formats the output in a user-friendly way.

    Args:
        summary (str): The summarized text
        original_length (int): Character count of original text
        summary_length (int): Character count of summary
    """
    print("\n" + "="*70)
    print("TEXT SUMMARY")
    print("="*70)
    print(f"\n{summary}\n")
    print("-"*70)
    print(f"Original length: {original_length} characters")
    print(f"Summary length: {summary_length} characters")
    reduction = ((original_length - summary_length) / original_length * 100) if original_length > 0 else 0
    print(f"Reduction: {reduction:.1f}%")
    print("="*70 + "\n")


def main():
    """
    Main function to handle command-line arguments and orchestrate the summarization.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Summarize text files by extracting key sentences.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py document.txt
  python main.py article.txt --sentences 5
  python main.py story.txt -s 2
        """
    )

    parser.add_argument(
        'file',
        type=str,
        help='Path to the text file to summarize'
    )

    parser.add_argument(
        '-s', '--sentences',
        type=int,
        default=3,
        help='Number of sentences to include in summary (default: 3)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate number of sentences
    if args.sentences < 1:
        print("Error: Number of sentences must be at least 1.")
        sys.exit(1)

    try:
        # Read the file
        print(f"\nReading file: {args.file}...")
        text = read_file(args.file)

        # Generate summary
        print("Generating summary...\n")
        summary = summarize_text(text, args.sentences)

        # Display results
        format_output(summary, len(text), len(summary))

    except FileNotFoundError as e:
        print(f"\n{e}")
        print("Please check the file path and try again.\n")
        sys.exit(1)
    except PermissionError as e:
        print(f"\n{e}")
        print("Please check file permissions and try again.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
