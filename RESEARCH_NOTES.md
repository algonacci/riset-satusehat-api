# Catatan Riset SATUSEHAT

Tanggal akses terakhir: 5 Oktober 2026.

## Sumber Resmi

- [Endpoint Information](https://satusehat.kemkes.go.id/platform/docs/id/postman-workshop/endpoint-information/)
  menetapkan OAuth base URL sandbox dan FHIR base URL sandbox
  `https://api-satusehat-stg.dto.kemkes.go.id/fhir-r4/v1`.
- [Framework FHIR](https://satusehat.kemkes.go.id/platform/docs/id/fhir/framework/)
  menjelaskan Resource, DomainResource, dan Bundle yang digunakan SATUSEHAT.
- `[V2.0] 010926 - Petunjuk Teknis SATUSEHAT Rekam Medis Elektronik
  (SSRME).pdf` mendokumentasikan autentikasi OAuth2 serta API CHLink/SHLink.

## Hasil Pengujian

### 01 — Generate token

- **PASS** — OAuth2 `client_credentials` sandbox menghasilkan access token.
- Token dimasking secara default dan tidak disimpan.

### 02 — CapabilityStatement

- Endpoint yang diuji: `GET <FHIR base URL>/metadata`.
- Dasar pengujian: endpoint metadata adalah konvensi FHIR R4, tetapi belum
  ditemukan halaman dokumentasi SATUSEHAT yang secara eksplisit menjamin
  endpoint ini.
- **PASS** — HTTP sukses dan respons berupa `CapabilityStatement`.
- `status`: `draft`.
- `fhirVersion`: `4.0.1` (FHIR R4).
- Terdapat 148 resource type dalam metadata saat pengujian.
- Resource Fase 1 yang terdeklarasi: `Organization`, `Location`, `Patient`,
  `Practitioner`, dan `PractitionerRole`.
- Interaction yang terdeklarasi mencakup operasi baca dan tulis. Ini hanya
  metadata server, bukan bukti bahwa credential diizinkan menjalankannya dan
  bukan izin untuk melakukan operasi tulis dalam riset ini.
- Elemen nama software dan deskripsi implementation tidak tersedia.

### 03 — Get Organization

- Dokumentasi resmi: [Organization ReST API](https://satusehat.kemkes.go.id/platform/docs/id/api-catalogue/onboardings/apis/organization/).
- Endpoint terdokumentasi: `GET <FHIR base URL>/Organization/:id`.
- ID request berasal dari `ORGANIZATION_ID` pada `.env` dan tidak dicetak.
- **PASS** — respons sukses berupa resource `Organization` dan logical ID cocok
  dengan `ORGANIZATION_ID` credential.
- Organization berstatus aktif, tidak memiliki `partOf`, dan respons saat uji
  tidak memuat identifier maupun endpoint reference.
- Raw response sandbox ditampilkan untuk riset; data tidak disimpan oleh script.

## Batas Interpretasi

- PDF SSRME bukan dokumentasi lengkap API FHIR SATUSEHAT.
- Resource standar FHIR atau resource yang muncul di portal dokumentasi tidak
  otomatis membuktikan akses credential maupun dukungan seluruh interaction.
- Tidak ada operasi tulis resource FHIR yang dilakukan dalam riset ini.

## Fase 1 Lanjutan

Dokumentasi resmi yang digunakan:

- [Location](https://satusehat.kemkes.go.id/platform/docs/id/api-catalogue/onboardings/apis/location/)
- [Patient](https://satusehat.kemkes.go.id/platform/docs/id/api-catalogue/onboardings/apis/patient/)
- [Practitioner](https://satusehat.kemkes.go.id/platform/docs/id/api-catalogue/onboardings/apis/practitioner/)
- [PractitionerRole](https://satusehat.kemkes.go.id/platform/docs/id/api-catalogue/integrations/apis/practitioner-role/)

### 04 — Search Location

- **PASS** — `GET /Location?organization=<ORGANIZATION_ID>&_count=10`
  menghasilkan searchset Bundle HTTP 200.
- Hasil saat uji: total 0 dan tidak memiliki next page. Credential valid, tetapi
  Organization sandbox belum memiliki Location yang dapat ditemukan.

### 05 — Get Location

- **BLOCKED** — tidak ada Location ID dari hasil search Organization ini.
- Script tersedia dan menerima ID eksplisit; contoh ID dokumentasi tidak dipakai
  karena dokumentasi menyatakan nilai contoh tidak dapat digunakan.

### 06–07 — Patient

- **PASS** — pencarian memakai salah satu NIK dummy sandbox yang secara resmi
  diterbitkan pada halaman Patient, dilanjutkan GET logical ID resminya.
- Search menghasilkan total 2 hasil, bukan 1. Ini membuktikan caller harus
  menangani hasil ganda dan tidak menganggap NIK sebagai logical ID unik.
- Detail fixture dummy terlihat pada raw response tetapi tidak disimpan.

### 08–09 — Practitioner

- **PASS** — pencarian memakai NIK dummy resmi sandbox dan GET memakai Nomor IHS
  resmi dari halaman Practitioner.
- Search menghasilkan total 10 hasil. Sandbox dapat memiliki banyak kecocokan
  untuk fixture tersebut; integrasi wajib menangani ambiguity.
- Detail fixture dummy terlihat pada raw response tetapi tidak disimpan.

### 10–11 — PractitionerRole

- Pengujian awal sempat **BLOCKED** oleh HTTP 429 saat autentikasi sebelum
  request FHIR dikirim. Server mengembalikan `OperationOutcome` dengan severity
  `transient`, code `throttled`.
- Temuan ini menunjukkan setiap CLI meminta token baru dan autentikasi memiliki
  rate limit. Pengujian lanjutan harus menggunakan satu token per batch/proses.
- **PASS** untuk search setelah cooldown dengan satu token yang dipakai ulang:
  HTTP 200, searchset Bundle, total 0 untuk kombinasi Practitioner dummy resmi
  dan Organization credential.
- **BLOCKED** untuk detail GET karena search tidak menghasilkan logical ID.
  ID contoh dokumentasi sengaja tidak digunakan.

### 12 — Operational Behavior

- HTTP 401 teramati saat endpoint metadata dipanggil tanpa bearer token.
- HTTP 429 `throttled` teramati pada endpoint autentikasi setelah beberapa
  panggilan berurutan. Tidak dilakukan retry agresif atau upaya memicu limit.
- **PASS** — authenticated `GET /metadata` mengembalikan HTTP 200 dan
  `CapabilityStatement`.
- Header `content-type` dan `x-request-id` tersedia. Header `etag`,
  `last-modified`, `x-correlation-id`, dan `retry-after` tidak tersedia pada
  respons sukses tersebut. Nilai header tidak dicatat.

## Status Exit Gate Fase 1

- PASS: autentikasi, capability discovery, Organization, Location search,
  Patient search/detail, Practitioner search/detail, PractitionerRole search,
  dan inspeksi operasional dasar.
- BLOCKED: Location detail karena Organization tidak memiliki hasil Location;
  PractitionerRole detail karena search terfilter tidak memiliki hasil.
- Tidak ada operasi tulis, data nyata, token, secret, atau respons mentah yang
  disimpan oleh script. Raw sandbox response hanya ditulis ke terminal.
