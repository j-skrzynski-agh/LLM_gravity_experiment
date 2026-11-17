from uploads import UploadQuota

def test_delete_does_not_free_quota():
    q = UploadQuota(1)
    q.upload("a.bin", 600_000, "2026-01")
    q.delete("a.bin", "2026-01")
    assert q.used_bytes("2026-01") == 600_000
