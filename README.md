# Riset SATUSEHAT API

Eksplorasi endpoint SATUSEHAT secara incremental menggunakan script Python
bernomor (`01_*.py`, `02_*.py`, dan seterusnya).

## Persiapan

Isi `.env`:

```dotenv
ORGANIZATION_ID=...
CLIENT_ID=...
CLIENT_SECRET=...
```

Secara default script menggunakan endpoint sandbox/staging. Untuk environment
lain, tambahkan URL endpoint token ke `.env`:

```dotenv
SATUSEHAT_AUTH_URL=https://api-satusehat-stg.dto.kemkes.go.id/oauth2/v1/accesstoken
```

## 01 - Generate token

```bash
uv run 01_generate_token.py
```

Token dimasking secara default. Untuk menampilkan token lengkap:

```bash
uv run 01_generate_token.py --show-token
```

Jangan commit `.env`, credential, atau access token ke repository.

## 02 - CapabilityStatement

Menguji discovery metadata FHIR sandbox secara read-only:

```bash
uv run 02_get_capability_statement.py
```

Endpoint `/metadata` merupakan konvensi FHIR dan hasil aktualnya dicatat di
`RESEARCH_NOTES.md`; ketersediaannya tidak diasumsikan.

## 03 - Get Organization

Membaca Organization yang ID-nya berasal dari `.env`, tanpa menampilkan nama,
identifier, alamat, atau kontak:

```bash
uv run 03_get_organization.py
```

## Fase 1 read-only

```bash
uv run 04_search_locations.py
uv run 05_get_location.py <LOCATION_ID>
uv run 06_search_patient.py --nik <NIK_DUMMY_RESMI>
uv run 07_get_patient.py <PATIENT_ID>
uv run 08_search_practitioner.py --nik <NIK_DUMMY_RESMI>
uv run 09_get_practitioner.py <PRACTITIONER_ID>
uv run 10_search_practitioner_roles.py <PRACTITIONER_ID>
uv run 11_get_practitioner_role.py <PRACTITIONER_ROLE_ID>
uv run 12_inspect_fhir_behavior.py
```

Gunakan hanya fixture dummy sandbox dari dokumentasi resmi. Script tidak
pernah menampilkan token atau secret. Untuk kebutuhan riset, script `02–12`
menampilkan raw JSON response sandbox terlebih dahulu, lalu summary. Raw response
dapat memuat identifier dan data dummy; jangan gunakan script ini terhadap data
nyata atau menyalin output ke log production. Hasil dan blocker pengujian
tersedia di `RESEARCH_NOTES.md`; implikasi produk tersedia di
`PRODUCT_READINESS.md`.
