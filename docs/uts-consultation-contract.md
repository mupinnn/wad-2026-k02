# Kontrak UTS — Jadwal konsultasi pasien

Kelompok 02. API ini mencatat jadwal konsultasi pasien di sebuah klinik. Petugas melihat daftar, menambah jadwal, dan menghapus jadwal. Tidak ada halaman detail dan tidak ada endpoint ubah.

Base URL lokal: `http://localhost:8000`

Data awal ada di [`backend/app/data.py`](../backend/app/data.py) sebagai `CONSULTATIONS`: 12 baris fiktif. Jangan memakai data pribadi sungguhan.

Skema Pydantic ditambahkan di `backend/app/schemas.py`. Operasi data ditambahkan di `backend/app/services.py`. Route baru didaftarkan di `backend/app/main.py`. Tambahkan fungsi atau route baru. Jangan mengubah milik anggota lain.

## Bentuk data

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `id` | int | hanya pada balasan | Diisi server. Tidak boleh dikirim saat membuat. |
| `nama_pasien` | string | ya | Nama fiktif |
| `nama_dokter` | string | ya | |
| `poli` | string | ya | Contoh: Umum, Gigi, Anak, Mata, Kulit |
| `waktu_konsultasi` | datetime | ya | ISO 8601, contoh `2026-09-28T08:00:00` |
| `keluhan` | string | ya | |

Contoh satu record:

```json
{
  "id": 1,
  "nama_pasien": "Sari Wulandari",
  "nama_dokter": "dr. Aditya Pratama",
  "poli": "Umum",
  "waktu_konsultasi": "2026-09-28T08:00:00",
  "keluhan": "Demam dan batuk sejak dua hari"
}
```

Skema masuk (`ConsultationCreate`) tidak berisi `id`. Skema keluar (`Consultation`) berisi semua field di atas, termasuk `id`. Keduanya terpisah.

## `GET /consultations`

| Bagian | Isi |
|---|---|
| Tujuan | Daftar jadwal, bisa dipotong halaman dan dicari |
| Auth | Tidak ada |
| Query `skip` | int, default `0`, minimal `0`. Lewati sebanyak ini setelah filter pencarian. |
| Query `limit` | int, default `5`, minimal `1`, maksimal `100` |
| Query `search` | string, opsional. Jika ada, cocokkan sebagai substring tanpa memedulikan huruf besar. Cocok bila ada di `nama_pasien` atau `nama_dokter`. |
| Body permintaan | Tidak ada |
| Balasan 200 | JSON array of record. Bukan objek pembungkus. Urutan mengikuti data, lalu `skip` dan `limit`. |
| Balasan error | Query yang bukan angka atau di luar batas: `422` bawaan FastAPI |

Contoh: `GET /consultations?skip=0&limit=5&search=sari` mengembalikan jadwal yang nama pasien atau dokternya mengandung "sari".

## `GET /consultations/{id}`

| Bagian | Isi |
|---|---|
| Tujuan | Satu jadwal. Diuji lewat `/docs`, bukan halaman terpisah. |
| Auth | Tidak ada |
| Query params | Tidak ada |
| Body permintaan | Tidak ada |
| Balasan 200 | Satu record, bentuk sama dengan contoh di atas |
| Balasan 404 | Id tidak ada. Badan: `{"detail": "Jadwal konsultasi tidak ditemukan."}` |

## `POST /consultations`

| Bagian | Isi |
|---|---|
| Tujuan | Menambah satu jadwal |
| Auth | Tidak ada |
| Query params | Tidak ada |
| Body permintaan | `ConsultationCreate`: `nama_pasien`, `nama_dokter`, `poli`, `waktu_konsultasi`, `keluhan`. Semua wajib. Tanpa `id`. |
| Balasan 201 | Record yang tersimpan, termasuk `id` baru. Bentuk `Consultation`. |
| Balasan 422 | Body tidak lengkap atau tipe salah. Pakai bentuk error bawaan FastAPI. |

`id` baru = id terbesar yang ada + 1.

## `DELETE /consultations/{id}`

| Bagian | Isi |
|---|---|
| Tujuan | Menghapus satu jadwal |
| Auth | Tidak ada |
| Query params | Tidak ada |
| Body permintaan | Tidak ada |
| Balasan 204 | Badan kosong |
| Balasan 404 | Id tidak ada. Badan sama dengan `GET /consultations/{id}`. |

## CORS

Hanya origin `http://localhost:5173`. Origin lain tidak mendapat `Access-Control-Allow-Origin`. Sudah dipasang di `backend/app/main.py`.

## Layar daftar

Supaya Anggota 2 dan Anggota 4 tidak mengedit komponen yang sama:

- Anggota 4 membuat halaman yang memanggil `GET /consultations`. Halaman itu yang memilih keadaan: `loading`, `error`, `empty` (berhasil dan nol baris), atau `data` (berhasil dan minimal satu baris). Permintaan dibatalkan saat halaman dilepas.
- Anggota 2 membuat komponen daftar yang hanya menerima prop `items` (array konsultasi). Komponen itu tidak memanggil API.
- Saat keadaan `data`, halaman merender komponen daftar itu. Sebelum berkas daftar ada, halaman boleh merender `<ul>` biasa, lalu diganti. Penggantian itu satu-satunya langkah integrasi.

Setiap input pada form tambah punya elemen `<label>` sendiri yang menunjuk ke input itu. Jangan memakai placeholder sebagai pengganti label.

## Berkas UI yang disarankan

Nama ini supaya pekerjaan tidak bertabrakan. Belum dibuat.

| Berkas | Pemilik | Isi |
|---|---|---|
| `frontend/src/components/ConsultationList.vue` | Anggota 2 | Daftar. Prop: `items` saja. |
| `frontend/src/components/ConsultationPage.vue` | Anggota 4 | Fetch, empat keadaan, tombol coba lagi |
| `frontend/src/components/ConsultationForm.vue` | Anggota 3 | Form tambah, validasi klien, error server, label |
| `frontend/src/components/DeleteConsultationDialog.vue` | Anggota 4 | Konfirmasi hapus, lalu muat ulang daftar |
