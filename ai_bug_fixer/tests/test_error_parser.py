def test_parse_errors_extracts_file_and_line():
    from backend.services.error_parser import parse_errors

    sample = 'FAILED test_x.py::test_a\nFile "test_x.py", line 10\n'
    errors = parse_errors(sample)
    assert len(errors) == 1
    assert errors[0]["file_path"] == "test_x.py"
    assert errors[0]["line_number"] == 10
