from uploads import UploadQuota

def test_reupload_same_name_counted_once():
    q = UploadQuota(1)
    q.upload("a.bin", 600_000, "2026-01")
    q.upload("a.bin", 600_000, "2026-01")
    assert q.used_bytes("2026-01") == 600_000
