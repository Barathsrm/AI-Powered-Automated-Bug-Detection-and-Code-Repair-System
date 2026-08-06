import re

TRACEBACK_FILE_RE = re.compile(r'File "([^"]+)", line (\d+)')


def parse_errors(pytest_output: str) -> list[dict]:
    """Very small pytest-log parser: pulls out failing test names,
    exception types, and the (file, line) locations from tracebacks."""
    errors = []
    blocks = pytest_output.split("FAILED ")[1:]
    for block in blocks:
        first_line = block.splitlines()[0] if block.splitlines() else ""
        matches = TRACEBACK_FILE_RE.findall(pytest_output)
        file_path, line_number = (matches[-1] if matches else (None, None))
        errors.append(
            {
                "test": first_line.strip(),
                "file_path": file_path,
                "line_number": int(line_number) if line_number else None,
                "raw": block[:2000],
            }
        )
    return errors
