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
