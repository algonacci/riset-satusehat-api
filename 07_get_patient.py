"""07 - Get one sandbox Patient by explicit logical ID."""
import argparse, sys
from satusehat_client import get, print_raw, require_resource, safe_summary, validate_resource_id

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("patient_id")
    args = parser.parse_args(); args.patient_id = validate_resource_id(args.patient_id)
    try:
        data, _ = get(f"Patient/{args.patient_id}"); require_resource(data, "Patient", args.patient_id)
        print_raw(data)
        print("Patient berhasil dibaca."); print(safe_summary(data))
        print("Detail Patient tidak diulang dalam summary."); return 0
    except RuntimeError as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
