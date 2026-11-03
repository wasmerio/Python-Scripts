# Log Scrubber

A command-line utility that creates a scrubbed copy of a text log before it is
shared. It redacts common credentials and email addresses, and lets you add
company-specific values or regular-expression patterns.

## Requirements

- Python 3.6 or newer
- No third-party packages

## Usage

From the repository root, run:

```bash
python "Log Scrubber/log_scrubber.py" path/to/application.log
```

By default, the script writes a sibling file named
`application.scrubbed.log`; the source log is never modified. Choose another
destination with `--output`:

```bash
python "Log Scrubber/log_scrubber.py" application.log --output scrubbed.log
```

Common password/token fields, authorization values, private-key blocks,
recognized GitHub/AWS/Google token formats, and email addresses are redacted
automatically. Add exact, case-sensitive strings with `--redact`, or custom
Python regular expressions with `--pattern`:

```bash
python "Log Scrubber/log_scrubber.py" application.log \
  --redact "Internal Project Name" \
  --pattern 'customer_id=\d+'
```

Use `--encoding` for logs that are not UTF-8. The program refuses to overwrite
an existing output unless `--force` is specified. It never allows the output
path to be the source path.

## Important

Redaction is pattern-based and cannot reliably identify every confidential or
proprietary detail. Add rules for organization-specific data and review the
output before sharing it. Custom regular expressions are applied to the full
text of the log.
