# Roadmap Riset Read-Only SATUSEHAT

> Dokumen ini sekaligus merupakan prompt kerja untuk AI worker berikutnya.

## Konteks

Repository ini digunakan untuk riset awal integrasi SATUSEHAT bagi produk baru
SIMKlinik/SIMRS. Produk belum memiliki fasilitas kesehatan pengguna dan belum
menggunakan data pasien nyata. Credential sandbox tersedia di `.env`.

Script `01_generate_token.py` sudah tersedia dan berhasil diuji. Dokumentasi
lokal berikut tersedia sebagai referensi:

```text
[V2.0] 010926 - Petunjuk Teknis SATUSEHAT Rekam Medis Elektronik (SSRME).pdf
```

PDF tersebut berfokus pada SSRME (CHLink dan SHLink), bukan dokumentasi lengkap
FHIR SATUSEHAT. Jangan menganggap endpoint yang tidak tercantum di PDF sebagai
terverifikasi. Cari dokumentasi resmi SATUSEHAT Platform untuk API FHIR umum,
dan catat sumber serta tanggal aksesnya.

## Prompt untuk AI Worker

Anda adalah AI coding worker yang bertugas mengeksplorasi kemampuan **read-only**
SATUSEHAT sandbox untuk persiapan produk multi-tenant SIMKlinik/SIMRS.

Kerjakan roadmap secara incremental. Mulai dengan memeriksa repository,
`README.md`, `.gitignore`, `pyproject.toml`, `01_generate_token.py`, nama variabel
di `.env` tanpa pernah mencetak nilainya, serta dokumentasi PDF lokal. Pertahankan
gaya penamaan script bernomor `NN_nama_deskriptif.py`.

### Tujuan

1. Memvalidasi autentikasi dan akses credential sandbox.
2. Mengidentifikasi endpoint GET yang benar-benar tersedia bagi credential.
3. Mengeksplorasi resource dasar yang diperlukan SIMKlinik/SIMRS:
   `Organization`, `Location`, `Patient`, dan `Practitioner`.
4. Mendokumentasikan struktur respons, parameter pencarian, pagination, error,
   rate limit jika terlihat, dan implikasi desain produk.
5. Menghasilkan script riset yang aman, sederhana, dapat diulang, dan tidak
   mengubah data SATUSEHAT.

### Batasan Mutlak

- Sandbox only. Jangan mengakses production.
- Untuk API bisnis/FHIR, hanya gunakan HTTP `GET` dan bila memang diperlukan
  untuk discovery yang terdokumentasi, `HEAD` atau `OPTIONS`.
- Pengecualian tunggal adalah `POST /oauth2/v1/accesstoken` untuk memperoleh
  access token karena OAuth2 memang mensyaratkannya.
- Jangan memanggil `POST`, `PUT`, `PATCH`, atau `DELETE` pada resource FHIR,
  CHLink, SHLink, maupun endpoint bisnis lain.
- Jangan menggunakan NIK, nama, tanggal lahir, atau data pasien nyata.
- Jangan menebak data dummy. Gunakan hanya fixture/contoh sandbox yang berasal
  dari dokumentasi resmi dan tuliskan sumbernya.
- Jangan mencetak atau menyimpan `CLIENT_SECRET` dan access token lengkap.
- Jangan memasukkan token ke URL/query string.
- Jangan commit `.env`, hasil respons sensitif, cache token, atau file temporer.
- Jangan mengubah credential dan jangan membuat klaim kompatibilitas production.
- Jangan meneruskan pekerjaan write-flow walaupun endpoint terlihat tersedia.

Jika data contoh resmi tidak ditemukan, implementasikan script dengan argumen
CLI wajib atau variabel environment opsional, dokumentasikan cara pakainya,
lalu tandai pengujian sebagai **BLOCKED — official sandbox fixture required**.
Jangan mengarang identifier agar script tampak berhasil.

## Konvensi Implementasi

- Gunakan Python, `httpx`, `python-dotenv`, dan `uv` yang sudah tersedia.
- Default base URL harus sandbox dan dapat dioverride dengan environment variable
  yang namanya eksplisit, misalnya `SATUSEHAT_FHIR_BASE_URL`.
- Tolak URL non-HTTPS dan, secara default, tolak host production.
- Semua request memakai timeout eksplisit.
- Gunakan `Authorization: Bearer <token>` hanya pada header.
- Kirim `Accept: application/fhir+json` untuk endpoint FHIR jika sesuai docs.
- Tampilkan ringkasan aman secara default; JSON lengkap hanya melalui `--raw`.
- Pada `--raw`, redaksi field sensitif seperti identifier/NIK, nama, alamat,
  telecom, birth date, token, dan secret. Bila respons belum bisa diredaksi
  dengan aman, jangan sediakan `--raw`.
- Tangani timeout, DNS/network error, respons non-JSON, HTTP 401/403/404/429,
  FHIR `OperationOutcome`, dan bundle kosong tanpa traceback yang membingungkan.
- Exit code `0` untuk sukses, non-zero untuk kegagalan atau konfigurasi kurang.
- Jangan membuat dependency baru kecuali benar-benar perlu.
- Hindari duplikasi. Setelah pola dua script terbukti, ekstrak helper reusable
  ke modul bernama jelas, tetapi pertahankan setiap script dapat dijalankan dari
  root repository.
- Jangan menaruh contoh identifier sensitif dalam source code atau README.

## Execution Gate Saat Ini

**AUTHORIZED NOW: Fase 1 saja.**

AI worker saat ini hanya diizinkan mengerjakan **Fase 1 — Fondasi dan Discovery
Aman**. Fase 2 dan seterusnya adalah master backlog agar arah riset tidak hilang,
tetapi belum boleh diimplementasikan atau diuji ke API sampai pemilik repository
memberikan persetujuan eksplisit.

- Boleh membaca dokumentasi untuk memetakan fase mendatang.
- Boleh mencatat tautan resmi dan pertanyaan terbuka.
- Tidak boleh membuat script fase berikutnya "sekalian".
- Tidak boleh memanggil endpoint fase berikutnya walaupun hanya GET.
- Keberhasilan satu endpoint bukan izin mencoba endpoint lain.
- Setelah acceptance criteria Fase 1 terpenuhi, berhenti dan laporkan hasil.

## Master Roadmap Read-Only

Nomor file setelah Fase 1 masih tentatif. Jangan mengganti histori atau nomor
script yang telah selesai.

### Fase 1 — Fondasi dan Discovery Aman (AUTHORIZED NOW)

#### 1A — Verifikasi dan Dokumentasi Dasar

1. Audit `01_generate_token.py` terhadap PDF lokal.
2. Pastikan token tidak tercetak penuh secara default.
3. Temukan dokumentasi resmi FHIR SATUSEHAT terbaru untuk:
   - base URL sandbox;
   - authentication header;
   - `CapabilityStatement`/metadata bila didukung;
   - `Organization`, `Location`, `Patient`, dan `Practitioner`;
   - parameter pencarian resmi setiap resource.
4. Buat `RESEARCH_NOTES.md` berisi:
   - URL sumber resmi;
   - tanggal akses;
   - fakta yang terverifikasi;
   - asumsi yang belum terverifikasi;
   - perbedaan dokumentasi SSRME vs FHIR Platform;
   - pertanyaan terbuka/blocker.

Jangan menggunakan blog pihak ketiga sebagai sumber kebenaran utama. Jika
dokumentasi resmi berbeda dengan Postman, catat perbedaannya dan pilih perilaku
yang paling aman; jangan mengubah request secara spekulatif.

#### 1B — Capability Discovery

Buat, jika didukung dokumentasi resmi:

```text
02_get_capability_statement.py
```

Tugas script:

- memperoleh token tanpa menampilkannya;
- memanggil endpoint metadata memakai GET;
- menampilkan versi FHIR, software/server, dan daftar resource/interaksi yang
  relevan;
- tidak menyimpulkan bahwa seluruh resource writable hanya karena metadata
  menyebutkannya;
- menyimpan temuan aman ke dokumentasi, bukan dump respons mentah.

Jika endpoint metadata tidak didukung atau akses ditolak, dokumentasikan status
HTTP dan `OperationOutcome` yang sudah diredaksi. Jangan mencoba endpoint acak.

#### 1C — Organization dan Location

Buat:

```text
03_get_organization.py
04_search_locations.py
05_get_location.py
```

Ketentuan:

- `03_get_organization.py` menggunakan `ORGANIZATION_ID` dari `.env`.
- Search Location harus dibatasi ke organization/identifier sesuai parameter
  yang benar-benar didokumentasikan.
- `05_get_location.py` menerima Location ID melalui argumen CLI atau env;
  jangan hardcode ID hasil lokal.
- Ringkasan hanya menampilkan resource type, logical ID yang dimasking bila
  perlu, active/status, dan jumlah hasil.
- Catat apakah Organization credential sama dengan Organization FHIR serta
  jangan menganggap keduanya identik tanpa verifikasi.

#### 1D — Patient Read-Only

Buat:

```text
06_search_patient.py
07_get_patient.py
```

Ketentuan:

- Hanya gunakan identifier pasien dummy resmi sandbox.
- Nilai pencarian diberikan melalui CLI/env, tidak disimpan dalam source.
- Validasi format input tanpa mencetak ulang nilai lengkap.
- Dukung pagination dengan batas halaman dan jumlah hasil yang konservatif.
- Jangan melakukan enumerasi identifier atau pencarian luas tanpa filter.
- Output default tidak menampilkan nama, NIK, alamat, telecom, atau tanggal
  lahir lengkap.
- Bedakan secara eksplisit: bundle kosong, unauthorized, forbidden, invalid
  search parameter, dan resource tidak ditemukan.

#### 1E — Practitioner dan PractitionerRole Read-Only

Buat:

```text
08_search_practitioner.py
09_get_practitioner.py
10_search_practitioner_roles.py
11_get_practitioner_role.py
```

Gunakan aturan keamanan yang sama dengan Patient. Jangan menganggap NIK dokter,
nomor STR, dan IHS Practitioner ID dapat saling dipertukarkan. Verifikasi sistem
identifier dan parameter search dari dokumentasi resmi.

`PractitionerRole` diteliti untuk memahami relasi tenaga kesehatan dengan
Organization, specialty, role, Location, dan HealthcareService. Jika resource
atau fixture tidak tersedia, beri status `BLOCKED`, bukan mencari data luas.

#### 1F — Perilaku Operasional Aman

Eksplorasi hanya melalui endpoint Fase 1 yang sudah terverifikasi:

- pagination Bundle (`link.next`) dengan batas konservatif;
- bundle kosong dan FHIR `OperationOutcome`;
- perbedaan `401`, `403`, `404`, dan `429` bila terjadi secara natural;
- request/correlation ID, content type, serta rate-limit metadata;
- `_count`, `_summary`, `_sort`, `_include`, dan `_revinclude` hanya jika
  terdokumentasi dan tersedia fixture resmi;
- token expiry metadata tanpa loop request;
- redaksi log dan error lokal.

Script tentatif:

```text
12_inspect_fhir_behavior.py
```

Jangan sengaja memicu rate limit. Scanning, enumeration, security testing, dan
load testing dilarang.

#### 1G — Analisis Readiness Produk

Perbarui `RESEARCH_NOTES.md` dan buat `PRODUCT_READINESS.md` yang membahas:

- pemisahan domain model internal dari FHIR;
- mapping local ID ke SATUSEHAT logical ID;
- credential dan Organization per tenant;
- secret encryption dan token cache per tenant;
- audit log tanpa payload klinis/token;
- timeout, retry, backoff, dan penanganan `429`;
- pagination;
- idempotency untuk fase write di masa depan;
- terminology mapping (ICD-10, SNOMED CT, LOINC, KFA, dan lainnya) sebagai
  area riset lanjutan, tanpa mengklaim seluruh terminologi wajib;
- antrean/outbox agar SIM tetap berjalan saat SATUSEHAT tidak tersedia;
- consent, privacy, retention, access control, dan observability;
- gap menuju onboarding fasilitas nyata dan production.

Jangan membuat implementasi write, database production, atau arsitektur besar
yang belum diperlukan. Dokumen harus membedakan **verified**, **assumption**,
**unknown**, dan **future work**.

#### Exit Gate Fase 1

Fase 1 selesai ketika autentikasi dan dokumentasi tervalidasi; capability,
Organization, Location, Patient, Practitioner, dan PractitionerRole sudah diuji
aman atau memiliki blocker jelas; perilaku operasional dasar terdokumentasi;
README, `RESEARCH_NOTES.md`, dan `PRODUCT_READINESS.md` diperbarui; serta tidak
ada data sensitif atau dump mentah tersimpan. Setelah itu worker wajib berhenti.

---

### Fase 2 — Struktur Layanan dan Administrasi (BACKLOG — NOT AUTHORIZED)

Resource kandidat:

- `HealthcareService`, `Endpoint`;
- `Schedule`, `Slot`, `Appointment`;
- `EpisodeOfCare`, `CareTeam`, `RelatedPerson`, `Flag`;
- `Consent`, `Coverage`.

Riset hubungan Organization–Location–layanan–jadwal–tenaga medis, identifier
system, scope per Organization, dan apakah resource benar-benar didukung. Jangan
menyamakan Coverage SATUSEHAT dengan BPJS PCare/VClaim.

```text
NN_search_healthcare_services.py
NN_get_healthcare_service.py
NN_search_schedules.py
NN_search_slots.py
NN_search_appointments.py
NN_search_episodes_of_care.py
NN_search_care_teams.py
NN_get_related_person.py
NN_search_consents.py
NN_search_coverages.py
```

### Fase 3 — Kunjungan dan Rekam Klinis Inti (BACKLOG — NOT AUTHORIZED)

Resource kandidat: `Encounter`, `Condition`, `AllergyIntolerance`, `Procedure`,
`ClinicalImpression`, dan `Observation`.

Riset lifecycle rawat jalan/IGD/rawat inap; relasi Patient, PractitionerRole,
Organization, dan Location; diagnosis utama/sekunder; coding; alergi; tindakan;
tanda vital; UCUM; profile/extension wajib; dan search parameters. Wajib memakai
dataset sandbox resmi dan tidak menampilkan narasi klinis/identitas pasien.

```text
NN_search_encounters.py
NN_get_encounter.py
NN_search_conditions.py
NN_get_condition.py
NN_search_allergies.py
NN_search_procedures.py
NN_search_clinical_impressions.py
NN_search_observations.py
NN_get_observation.py
```

### Fase 4 — Laboratorium, Radiologi, dan Dokumen (BACKLOG — NOT AUTHORIZED)

Resource kandidat: `ServiceRequest`, `Specimen`, `Observation`,
`DiagnosticReport`, `ImagingStudy`, `DocumentReference`, dan `BodyStructure` bila
digunakan profile resmi.

Riset alur order → specimen → result → report, panel laboratorium, LOINC,
SNOMED CT, UCUM, performer, status, metadata radiologi, dan attachment metadata.
Jangan mengunduh attachment, DICOM, image, atau `Binary`; metadata saja sampai
risiko serta otorisasi dipahami.

```text
NN_search_service_requests.py
NN_search_specimens.py
NN_search_lab_observations.py
NN_search_diagnostic_reports.py
NN_search_imaging_studies.py
NN_search_document_references.py
```

### Fase 5 — Farmasi (BACKLOG — NOT AUTHORIZED)

Resource kandidat: `Medication`, `MedicationRequest`, `MedicationDispense`,
`MedicationAdministration`, `MedicationStatement`, dan katalog KFA resmi.

Riset lifecycle resep/dispensing/administration; KFA; bentuk dan satuan sediaan;
dose, route, frequency, duration, quantity; racikan; aturan pakai; serta relasi
Encounter, prescriber, dispenser, Patient, dan Organization.

```text
NN_search_medications.py
NN_search_medication_requests.py
NN_get_medication_request.py
NN_search_medication_dispenses.py
NN_search_medication_administrations.py
NN_search_medication_statements.py
NN_lookup_kfa_product.py
```

### Fase 6 — Terminologi dan Conformance (BACKLOG — NOT AUTHORIZED)

Riset `StructureDefinition`, `SearchParameter`, `ValueSet`, `CodeSystem`,
`ConceptMap`, ICD-10, SNOMED CT, LOINC, UCUM, KFA, serta kode administratif dan
specialty resmi.

Operasi `$lookup`, `$expand`, dan `$validate-code` harus mengikuti method resmi.
Walaupun semantiknya read-only, HTTP POST tetap dilarang tanpa izin eksplisit.
Prioritaskan artefak Implementation Guide dan endpoint GET resmi. Jangan
mengunduh seluruh terminologi; petakan kebutuhan validasi dan lisensinya.

```text
NN_inspect_structure_definitions.py
NN_inspect_search_parameters.py
NN_lookup_code_system.py
NN_expand_value_set.py
NN_validate_code_get.py
TERMINOLOGY_NOTES.md
```

### Fase 7 — Financial dan Ekosistem Eksternal (BACKLOG — NOT AUTHORIZED)

Verifikasi dokumentasi untuk `Account`, `Claim`, `ClaimResponse`, `Invoice`, dan
`Coverage`; jangan berasumsi tersedia. SATUSEHAT tidak boleh disamakan dengan
BPJS PCare, VClaim, Aplicares, Antrean, atau Mobile JKN. Output fase ini terutama
gap analysis dan peta integrasi terpisah, bukan percobaan endpoint.

### Fase 8 — SSRME, CHLink, dan SHLink (BACKLOG — NOT READ-ONLY)

PDF lokal mendokumentasikan `POST /ssrme/v2/ntl/chl` dan
`POST /ssrme/v2/ntl/shl`. Keduanya di luar izin read-only. Saat ini hanya boleh
meneliti prasyarat, payload, consent normal/bypass, expiry, security, dan error
response tanpa memanggil endpoint.

Sebelum fase dibuka, validasi integrasi dan pengiriman kunjungan fasyankes,
KYC/consent, ID Patient/Practitioner/Organization, kontrol akses UI/session,
audit, dan perlindungan URL/token sensitif.

### Fase 9 — Write Flow End-to-End (FUTURE — NOT AUTHORIZED)

```text
Encounter
  → Condition
  → Observation
  → Procedure
  → ServiceRequest / DiagnosticReport
  → MedicationRequest / MedicationDispense
  → finalisasi Encounter
```

Memerlukan roadmap terpisah untuk tenant sandbox sah, fixture klinis dummy,
profile validation, dependency ordering, mapping ID, idempotency, outbox, retry,
dead letter, reconciliation, provenance/audit, correction/cancel/error workflow,
privacy, consent, retention, RBAC, dan incident response.

### Fase 10 — Production Readiness dan Multi-Tenant (FUTURE)

Audit onboarding/offboarding fasyankes, credential dan token cache per tenant,
secret manager/rotation, isolasi sandbox-production, queue isolation,
rate-limit/backpressure, observability tanpa PHI/PII, immutable audit trail,
backup/DR/reconciliation, retention, RBAC/ABAC, least privilege, break-glass,
legal/compliance, dan regression test perubahan Implementation Guide.

Jangan membuat klaim "SATUSEHAT ready/certified" tanpa verifikasi resmi.

## Acceptance Criteria per Script

Sebuah script dianggap selesai hanya jika:

1. Memiliki `--help` yang jelas.
2. Berjalan melalui `uv run NN_script.py ...`.
3. Tidak mengandung credential atau identifier sensitif hardcoded.
4. Hanya memanggil endpoint/method yang diizinkan roadmap ini.
5. Memiliki timeout dan error handling.
6. Tidak membocorkan token atau data personal pada output default/error.
7. URL dan parameter request mempunyai referensi dokumentasi resmi di
   `RESEARCH_NOTES.md`.
8. Hasil uji dicatat sebagai `PASS`, `FAIL`, atau `BLOCKED`, berikut alasan dan
   status HTTP yang aman untuk dicatat.
9. README diperbarui dengan contoh perintah tanpa data nyata.
10. Syntax seluruh file Python lolos pemeriksaan dan script tidak merusak
    pekerjaan pengguna yang sudah ada.

## Validasi Akhir

Lakukan pemeriksaan berikut tanpa mencetak isi `.env`:

```bash
uv run python -m compileall -q .
uv run 01_generate_token.py
uv run 02_get_capability_statement.py
```

Jalankan script lain hanya jika fixture resmi yang diperlukan tersedia. Jangan
memaksakan request agar semua script berstatus sukses.

Periksa juga perubahan Git dan pastikan tidak ada secret atau hasil respons yang
ter-track. Jangan melakukan commit kecuali diminta.

## Format Laporan Akhir Worker

Laporkan secara ringkas:

1. file yang dibuat/diubah;
2. endpoint dan parameter yang berhasil diverifikasi;
3. hasil tiap script: `PASS`, `FAIL`, atau `BLOCKED`;
4. risiko keamanan atau ketidakpastian dokumentasi;
5. blocker yang membutuhkan fixture/credential/fasilitas nyata;
6. rekomendasi fase riset berikutnya.

## Definition of Done Roadmap Read-Only

Fase 1 read-only selesai ketika autentikasi, discovery (jika didukung),
Organization, Location, Patient, Practitioner, PractitionerRole, serta perilaku
operasional dasar telah memiliki script/dokumentasi aman; atau status blocker
masing-masing telah dijelaskan tanpa data nyata maupun operasi tulis.

Setelah itu **berhenti**. Semua Fase 2–10 tetap terkunci sampai pemilik repository
secara eksplisit membuka fase tertentu. Jangan melanjutkan ke Encounter,
Condition, Observation, Medication, CHLink, SHLink, atau resource lain hanya
karena tercantum dalam master backlog.
