# Product Readiness SIMKlinik/SIMRS — SATUSEHAT

## Verified

- OAuth2 sandbox menggunakan `client_credentials` dan token memiliki expiry.
- FHIR sandbox menggunakan FHIR R4 (`4.0.1`).
- Credential terikat pada `ORGANIZATION_ID` yang dapat dibaca sebagai resource
  Organization.
- Server menerapkan rate limit autentikasi dan mengembalikan HTTP `429` dengan
  `OperationOutcome` berkode `throttled`.
- Search identifier sandbox dapat menghasilkan lebih dari satu hasil; aplikasi
  tidak boleh menganggap NIK selalu memetakan tepat ke satu logical ID.

## Product Design Requirements

### Multi-tenant credentials

Setiap tenant/fasyankes harus memiliki environment, Organization ID, Client ID,
dan encrypted Client Secret sendiri. Token cache wajib terisolasi per tenant dan
environment. Jangan memakai satu credential global untuk seluruh pelanggan.

### Token lifecycle

Cache token in-memory atau di secret-aware distributed cache sampai beberapa
menit sebelum expiry. Gunakan single-flight lock agar banyak request tidak
melakukan autentikasi bersamaan. Hormati `429`/`Retry-After` dengan bounded
exponential backoff; jangan retry loop tanpa batas.

### Domain and FHIR mapping

Model domain SIM tidak boleh identik dengan JSON FHIR. Simpan mapping:

```text
tenant_id, local_entity_type, local_id,
fhir_resource_type, fhir_logical_id, version_id,
sync_status, last_attempt_at, last_error_code
```

Identifier seperti NIK bukan primary key internal maupun jaminan hasil unik.

### Reliability

Untuk fase write di masa depan gunakan transactional outbox, worker queue,
idempotency/duplicate prevention, bounded retry, dead-letter queue, dan proses
rekonsiliasi. SIM harus tetap dapat melayani operasional ketika SATUSEHAT down.

### Security and privacy

- Jangan log token, secret, NIK, nama, alamat, telecom, tanggal lahir, payload
  klinis, maupun URL yang mengandung identifier.
- Terapkan encryption at rest/in transit, least privilege, RBAC/ABAC, audit log
  immutable, retention policy, dan prosedur incident response.
- Pisahkan sandbox dan production secara teknis, bukan hanya konfigurasi UI.

## Assumptions

- Detail onboarding vendor dan pola pengelolaan credential production perlu
  diverifikasi saat memperoleh fasilitas mitra.
- Resource yang tampil pada CapabilityStatement belum tentu dapat digunakan oleh
  seluruh credential atau use case.

## Unknown / Blockers

- Belum ada tenant fasyankes nyata untuk menguji lifecycle onboarding.
- Belum ada data Location milik Organization sandbox saat pengujian awal.
- Dukungan rate-limit headers dan correlation ID masih dalam pengujian.
- Kebijakan consent, retention, dan akses production memerlukan validasi legal
  serta dokumentasi resmi terbaru.

## Future Work

Fase 2 dan seterusnya tetap terkunci sesuai `ROADMAP.md`, termasuk resource
klinis, SSRME, CHLink/SHLink, dan seluruh operasi tulis.
