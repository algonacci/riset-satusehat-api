"""06 - Search a sandbox Patient by an official dummy NIK supplied via CLI."""
import argparse, re, sys
from satusehat_client import get, print_raw, require_bundle

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--nik", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"\d{16}", args.nik): print("FAIL: NIK harus 16 digit.", file=sys.stderr); return 1
    try:
        data, _ = get("Patient", {"identifier": f"https://fhir.kemkes.go.id/id/nik|{args.nik}", "_count": "10"})
        resources = require_bundle(data, "Patient")
        print_raw(data)
        print("Pencarian Patient berhasil."); print(f"total: {data.get('total', len(resources))}")
        print(f"hasil halaman ini: {len(resources)}")
        print("Detail Patient tidak diulang dalam summary."); return 0
    except RuntimeError as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
