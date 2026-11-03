import argparse
import re
from pathlib import Path


REDACTED = "[REDACTED]"

_SECRET_FIELDS = (
    r"(?:password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|"
    r"client[_-]?secret)"
)


def _replace_quoted_value(match):
    quote = match.group(2)
    return f"{match.group(1)}{quote}{REDACTED}{quote}"


def _replace_prefixed_value(match):
    return match.group(1) + REDACTED


_PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?"
    r"-----END [A-Z0-9 ]*PRIVATE KEY-----",
    re.IGNORECASE | re.DOTALL,
)
_QUOTED_AUTHORIZATION = re.compile(
    r"(?i)(\b(?:authorization|proxy-authorization)\b[\"']?\s*[:=]\s*)"
    r"([\"'])(.*?)\2"
)
_UNQUOTED_AUTHORIZATION = re.compile(
    r"(?i)(\b(?:authorization|proxy-authorization)\b[\"']?\s*[:=]\s*)"
    r"(?:(?:bearer|basic)\s+)?[^\s,;\"']+"
)
_QUOTED_SECRET = re.compile(
    r"(?i)(\b" + _SECRET_FIELDS + r"\b[\"']?\s*[:=]\s*)"
    r"([\"'])(.*?)\2"
)
_UNQUOTED_SECRET = re.compile(
    r"(?i)(\b" + _SECRET_FIELDS + r"\b[\"']?\s*[:=]\s*)"
    r"[^\s,;\"'&]+"
)
_BEARER_TOKEN = re.compile(
    r"(?i)(\bbearer\s+)[A-Za-z0-9._~+/-]+=*"
)
_KNOWN_TOKENS = re.compile(
    r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
    r"AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35})\b"
)
_EMAIL_ADDRESS = re.compile(
    r"\b[A-Za-z0-9.!#$%&'*+/?^_`{|}~-]+@"
    r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

_DEFAULT_REDACTIONS = (
    (_PRIVATE_KEY, REDACTED),
    (_QUOTED_AUTHORIZATION, _replace_quoted_value),
    (_UNQUOTED_AUTHORIZATION, _replace_prefixed_value),
    (_QUOTED_SECRET, _replace_quoted_value),
    (_UNQUOTED_SECRET, _replace_prefixed_value),
    (_BEARER_TOKEN, _replace_prefixed_value),
    (_KNOWN_TOKENS, REDACTED),
    (_EMAIL_ADDRESS, REDACTED),
)


def scrub_text(text, redact_values=(), regex_patterns=()):
    """Redact common secrets and caller-supplied literal values or patterns."""
    if any(not value.strip() for value in redact_values):
        raise ValueError("Values passed to --redact cannot be empty or whitespace.")

    compiled_patterns = []
    for expression in regex_patterns:
        try:
            pattern = re.compile(expression)
        except re.error as error:
            raise ValueError(f"Invalid redaction pattern: {error}") from error
        if pattern.search(""):
            raise ValueError("Redaction patterns must not match an empty string.")
        compiled_patterns.append(pattern)

    for pattern, replacement in _DEFAULT_REDACTIONS:
        text = pattern.sub(replacement, text)

    if redact_values:
        alternatives = sorted(set(redact_values), key=len, reverse=True)
        literal_pattern = re.compile("|".join(re.escape(value) for value in alternatives))
        text = literal_pattern.sub(REDACTED, text)

    for pattern in compiled_patterns:
        text = pattern.sub(REDACTED, text)

    return text


def default_output_path(input_path):
    """Return a sibling output path that keeps the source file unchanged."""
    input_path = Path(input_path)
    return input_path.with_name(
        f"{input_path.stem}.scrubbed{input_path.suffix}"
    )


def scrub_file(
    input_path,
    output_path=None,
    redact_values=(),
    regex_patterns=(),
    encoding="utf-8",
    overwrite=False,
):
    """Scrub a text log into a separate output file and return its path."""
    input_path = Path(input_path)
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    output_path = Path(output_path) if output_path else default_output_path(input_path)
    if input_path.resolve() == output_path.resolve():
        raise ValueError("The output path must not overwrite the input file.")
    if not output_path.parent.is_dir():
        raise FileNotFoundError(
            f"Output directory does not exist: {output_path.parent}"
        )
    if output_path.exists() and input_path.samefile(output_path):
        raise ValueError("The output path must not overwrite the input file.")
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Output file already exists: {output_path} (use --force to replace it)"
        )

    with input_path.open("r", encoding=encoding, newline="") as source_file:
        content = source_file.read()
    scrubbed_content = scrub_text(content, redact_values, regex_patterns)
    with output_path.open("w", encoding=encoding, newline="") as scrubbed_file:
        scrubbed_file.write(scrubbed_content)
    return output_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Redact common secrets and selected values from a log file."
    )
    parser.add_argument("input", type=Path, help="Path to the source log file")
    parser.add_argument(
        "-o", "--output", type=Path, help="Output path (default: add .scrubbed)"
    )
    parser.add_argument(
        "--redact",
        action="append",
        default=[],
        metavar="TEXT",
        help="Also redact this exact, case-sensitive value (repeatable)",
    )
    parser.add_argument(
        "--pattern",
        action="append",
        default=[],
        metavar="REGEX",
        help="Also redact matches for this Python regular expression (repeatable)",
    )
    parser.add_argument(
        "--encoding", default="utf-8", help="Input/output text encoding (default: utf-8)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output file (never overwrites the input)",
    )
    args = parser.parse_args(argv)

    try:
        output_path = scrub_file(
            args.input,
            args.output,
            args.redact,
            args.pattern,
            args.encoding,
            args.force,
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Scrubbed log saved to: {output_path}")


if __name__ == "__main__":
    main()
