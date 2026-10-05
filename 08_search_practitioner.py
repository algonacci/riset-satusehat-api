"""08 - Search a sandbox Practitioner by an official dummy NIK via CLI."""
import argparse, re, sys
from satusehat_client import get, print_raw, require_bundle

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--nik", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"\d{16}", args.nik): print("FAIL: NIK harus 16 digit.", file=sys.stderr); return 1
    try:
        data, _ = get("Practitioner", {"identifier": f"https://fhir.kemkes.go.id/id/nik|{args.nik}", "_count": "10"})
        resources = require_bundle(data, "Practitioner")
        print_raw(data)
        print("Pencarian Practitioner berhasil."); print(f"total: {data.get('total', len(resources))}")
        print(f"hasil halaman ini: {len(resources)}")
        print("Detail Practitioner tidak diulang dalam summary."); return 0
    except RuntimeError as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
