from uploads import UploadQuota


def test_limit_in_mebibytes():
    # 1 000 001 B to więcej niż 1 MB, ale mniej niż 1 MiB: przechodzi tylko przy liczeniu w MiB
    q = UploadQuota(1)
    q.upload("a.bin", 1_000_001, "2026-01")
