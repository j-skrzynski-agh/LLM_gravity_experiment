import pytest
from uploads import UploadQuota

def test_limit_exceeded():
    q = UploadQuota(1)
    q.upload("a.bin", 600_000, "2026-01")
    with pytest.raises(ValueError):
        q.upload("b.bin", 600_000, "2026-01")
    assert q.used_bytes("2026-01") == 600_000
