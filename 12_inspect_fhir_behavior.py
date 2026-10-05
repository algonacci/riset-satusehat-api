"""12 - Inspect safe operational metadata using one authenticated GET."""
import argparse, sys
from satusehat_client import get, print_raw

SAFE_HEADERS = ("content-type", "etag", "last-modified", "x-request-id", "x-correlation-id", "retry-after")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.parse_args()
    try:
        data, response = get("metadata")
        print_raw(data)
        print("Inspeksi perilaku FHIR berhasil.")
        print(f"HTTP: {response.status_code}")
        print(f"resourceType: {data.get('resourceType', '-')}")
        for name in SAFE_HEADERS:
            if name in response.headers: print(f"header {name}: tersedia")
        print("Nilai request ID, ETag, tanggal, dan header sensitif tidak ditampilkan.")
        return 0
    except RuntimeError as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
