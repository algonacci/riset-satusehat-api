"""09 - Get one sandbox Practitioner by explicit logical ID."""
import argparse, sys
from satusehat_client import get, print_raw, require_resource, safe_summary, validate_resource_id

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("practitioner_id")
    args = parser.parse_args(); args.practitioner_id = validate_resource_id(args.practitioner_id)
    try:
        data, _ = get(f"Practitioner/{args.practitioner_id}"); require_resource(data, "Practitioner", args.practitioner_id)
        print_raw(data)
        print("Practitioner berhasil dibaca."); print(safe_summary(data))
        print("Detail Practitioner tidak diulang dalam summary."); return 0
    except RuntimeError as exc: print(f"FAIL: {exc}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
