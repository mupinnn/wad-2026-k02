# Kontrak API

## Ringkasan

API ini melayani sistem pencatatan dan pengelolaan jadwal konsultasi pasien untuk klinik. Aplikasi ini digunakan oleh staf atau klien untuk menambah, melihat, mencari, dan menghapus data sesi konsultasi pasien secara terstruktur dengan dukungan pembatas asal CORS khusus frontend.

Base URL lokal: `http://localhost:8000`
Base URL produksi: Belum tersedia (diisi Sesi 14)

## Model data

Sistem ini menggunakan struktur data utama untuk manajemen konsultasi:
1. **tabel `users`**: Menyimpan data akun pengguna atau staf sistem.
2. **tabel `consultations` (Induk/Entitas Utama)**: Menyimpan informasi dasar sesi konsultasi klinik.
3. **tabel `consultations_detail` (Anak)**: Menyimpan rincian lengkap pendaftaran. Berdasarkan skema, atribut yang digunakan meliputi: `id` (int, wajib, dibuat server), `nama_pasien` (str, wajib), `nama_dokter` (str, wajib), `poli` (str, wajib), `waktu_konsultasi` (datetime, wajib), dan `keluhan` (str, wajib).
Relasi *one-to-many* diterapkan di mana satu entitas utama konsultasi memiliki rincian data pasien terkait.

## Autentikasi

Belum menggunakan mekanisme token pada Sesi 7 ini (bersifat publik atau diatur lokal sesuai kebutuhan pengembangan awal).

## Endpoint

### `GET /consultations`

| Bagian | Isi |
|---|---|
| Tujuan | Mengambil daftar seluruh jadwal konsultasi dengan opsi paginasi dan pencarian. |
| Auth | Publik |
| Query params | `skip` (int, default=0, ge=0), `limit` (int, default=5, ge=1, le=100), `search` (str \| None, opsional) |
| Body permintaan | Tidak ada |
| Balasan 2xx | Mengembalikan daftar objek konsultasi dalam format data terstruktur. |
| Balasan error | 422 Unprocessable Entity jika parameter query tidak memenuhi validasi. |

### `GET /consultations/{id}`

| Bagian | Isi |
|---|---|
| Tujuan | Mengambil detail satu data konsultasi spesifik berdasarkan ID. |
| Auth | Publik |
| Query params | Tidak ada |
| Body permintaan | Tidak ada |
| Balasan 2xx | `{"sukses": true, "pesan": "Konsultasi ditemukan", "data": {"id": 1, "nama_pasien": "Budi", "nama_dokter": "Dr. Andi", "poli": "Umum", "waktu_konsultasi": "2026-03-30T10:00:00", "keluhan": "Pusing"}}` |
| Balasan error | 404 Not Found dengan badan `{"sukses": false, "pesan": "Konsultasi tidak ditemukan"}` jika ID tidak ada. |

### `POST /consultations`

| Bagian | Isi |
|---|---|
| Tujuan | Menambahkan jadwal konsultasi baru ke sistem. |
| Auth | Publik |
| Query params | Tidak ada |
| Body permintaan | `{"nama_pasien": "Siti", "nama_dokter": "Dr. Budi", "poli": "Anak", "waktu_konsultasi": "2026-03-31T09:30:00", "keluhan": "Demam"}` |
| Balasan 2xx | Status `201 Created`: `{"sukses": true, "pesan": "Konsultasi berhasil ditambahkan", "data": {...}}` |
| Balasan error | 422 Unprocessable Entity jika struktur JSON tidak sesuai dengan skema Pydantic (`ConsultationCreate`). |

### `DELETE /consultations/{id}`

| Bagian | Isi |
|---|---|
| Tujuan | Menghapus data jadwal konsultasi berdasarkan ID. |
| Auth | Publik |
| Query params | Tidak ada |
| Body permintaan | Tidak ada |
| Balasan 2xx | `{"sukses": true, "pesan": "Konsultasi berhasil dihapus", "data": {...}}` |
| Balasan error | 404 Not Found dengan badan `{"sukses": false, "pesan": "Konsultasi tidak ditemukan"}` jika ID tidak ditemukan. |

### `GET /health`

| Bagian | Isi |
|---|---|
| Tujuan | Mengecek status kesehatan atau keaktifan server. |
| Auth | Publik |
| Query params | Tidak ada |
| Body permintaan | Tidak ada |
| Balasan 2xx | `{"status": "ok"}` |
| Balasan error | - |

## Status code yang dipakai

| Kode | Kapan dipakai di API ini |
|---|---|
| 200 | Digunakan saat permintaan GET berhasil mengambil data atau operasi sukses secara umum. |
| 201 | Digunakan secara khusus pada endpoint POST (`status.HTTP_201_CREATED`) saat data baru berhasil dibuat. |
| 204 | Tidak digunakan secara aktif di API ini. |
| 400 / 422 | 422 dikembalikan otomatis oleh Pydantic/FastAPI jika tipe data atau parameter permintaan klien tidak valid. |
| 401 vs 403 | 401 (Unauthorized) jika belum terautentikasi, 403 (Forbidden) jika tidak memiliki hak akses. |
| 404 | Digunakan saat data dengan ID tertentu (`get_consultation` atau `delete_consultation`) menghasilkan nilai kosong (`None`). |

## Versioning

Kontrak ini akan diperbarui secara berkala. Jika terjadi perubahan struktur endpoint setelah digunakan oleh kelompok lain, penyesuaian versi akan dikoordinasikan bersama tim.