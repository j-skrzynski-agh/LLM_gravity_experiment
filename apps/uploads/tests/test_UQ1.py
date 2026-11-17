import pytest
from uploads import UploadQuota

def test_empty_file_rejected():
    with pytest.raises(ValueError):
        UploadQuota(1).upload("a.txt", 0, "2026-01")
