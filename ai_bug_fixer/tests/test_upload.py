def test_upload_project_accepts_zip():
    # TODO: use TestClient to POST a small zip fixture to /upload/
    # and assert a 200 with a project_id in the response.
    assert True


def test_upload_rejects_path_traversal_zip():
    # TODO: build a zip containing "../../etc/passwd" and assert
    # safe_extract_zip raises ValueError.
    assert True
