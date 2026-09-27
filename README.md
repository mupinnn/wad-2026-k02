# The Build — Starter

**CIK3101 · Web Application Development · Sains Data · Semester 3 · Universitas Cakrawala**

Repo ini adalah tempat kerja kelompokmu selama 16 sesi. Artefak tiap sesi dikerjakan **di dalam
sesi** dan di-commit sebelum kelas selesai. **Tidak ada pekerjaan rumah.**

Repo ini sengaja **belum berisi aplikasi**. `frontend/` dan `backend/` kosong — kamu yang
mengisinya, mulai malam ini di Sesi 2. Yang sudah disediakan hanyalah rel: dokumen, CI, dan
pemeriksa nilai.

> **Proyek akhir mata kuliah ini bernama The Build, bobot 20% (Tugas Kelompok).**
> The Build bukan tugas tambahan. The Build adalah gabungan artefak Sesi 2–14 di repo ini,
> didemokan di Sesi 15 dan diverifikasi di Sesi 16. Baca **[`docs/PROJECT.md`](docs/PROJECT.md)**
> — itu piagam proyekmu, dan diisi malam ini.

---

## 0. Membuat repo kelompok (sekali saja, di Sesi 2)

Ini **administratif**, bukan tugas — sama seperti membawa laptop. Dikerjakan **ketua kelompok**,
sekali, di awal lab.

```bash
# 1. Di GitHub: buka repo template ini, klik "Use this template" -> "Create a new repository"
#    Nama repo : wad-2026-kNN     (NN = nomor kelompokmu, contoh wad-2026-k04)
#    Visibility: PUBLIC           (wajib — branch protection tidak tersedia di repo privat gratis)

# 2. Tambahkan 3 anggota lain sebagai collaborator
#    Settings -> Collaborators -> Add people   (pakai username GitHub mereka)

# 3. Semua anggota clone repo KELOMPOK, bukan template-nya
git clone https://github.com/<username-ketua>/wad-2026-kNN
cd wad-2026-kNN
cp .env.example .env
```

**4. Lindungi `main`** — ini butir 1 rubrik malam ini, dan dilakukan ketua:

> Settings → Branches → **Add branch protection rule**
> - Branch name pattern: `main`
> - ☑ **Require a pull request before merging**
> - ☑ **Do not allow bypassing the above settings**
> - Save changes

Setelah itu `git push` langsung ke `main` akan ditolak. Itu memang tujuannya. Semua perubahan
lewat branch `feature/*` dan pull request.

> "Require approvals" **jangan** dinyalakan malam ini — undangan collaborator mungkin belum
> diterima semua anggota, dan kamu akan terkunci tidak bisa merge. Naikkan ke 1 approval di
> Sesi 3, setelah semua anggota masuk.

**5. Kirim URL repo kelompokmu ke thread RISE.** Tanpa itu dosen tidak tahu ke mana harus menilai.

---

## 1. Prasyarat

| Alat | Versi | Cek |
|---|---|---|
| Git | apa saja | `git --version` |
| Node.js | 20 LTS atau lebih baru | `node -v` |
| Python | 3.11 atau lebih baru | `python --version` |
| Akun GitHub | — | sudah jadi anggota repo ini |

> Windows: saat install Python dari python.org, **centang "Add Python to PATH"**.
> Kalau `python` tidak dikenali, coba `py`.

Tidak ada yang perlu di-install untuk basis data sampai Sesi 5. Sampai sesi itu repo memakai
SQLite, yang sudah menyatu dengan Python.

## 2. Layanan

| Layanan | Port lokal | Mulai dipakai | Catatan |
|---|---|---|---|
| Frontend (Vite + Vue 3) | `5173` | Sesi 2 | kerangka shadcn-vue; fitur jadwal belum ada |
| Backend (FastAPI + Uvicorn) | `8000` | Sesi 2 | `/health` dan CORS; route konsultasi belum ada |
| Basis data | — | Sesi 3 | SQLite lokal; ganti ke Postgres (Neon) di Sesi 5 lewat `DATABASE_URL` |

## 3. Cara menjalankan

Dua server harus jalan bersamaan. Backend di port `8000`, frontend di port `5173`.

```bash
# sekali saja, setelah clone
cp .env.example .env

# --- backend (terminal 1) ---
cd backend
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# --- frontend (terminal 2) ---
cd frontend
npm install
npm run dev
```

## 4. Cara memverifikasi

Satu perintah, dipakai sepanjang semester:

```bash
python verify.py --sesi 2
```

`verify.py` adalah **perintah yang sama persis** yang dipakai dosen untuk memeriksa artefakmu.
Kalau hijau di laptopmu, hijau juga saat dinilai. Jalankan sebelum kamu keluar dari sesi.

> **CI merah saat repo baru itu normal.** Pemeriksa berjalan juga di GitHub Actions, dan pada
> repo kosong ia memang gagal — belum ada `frontend/` dan `backend/`. **Membuatnya hijau adalah
> tugasmu malam ini.** Ketentuan 7 (CI merah = 0 fungsionalitas) dinilai pada akhir sesi, bukan
> pada commit pertama.

Verifikasi manual yang juga dinilai:

- `http://localhost:5173` — halaman kerangka muncul, masih rapi di lebar 360px
- `http://localhost:8000/health` — balas `200` dengan `{"status":"ok"}`
- `http://localhost:8000/docs` — OpenAPI terbuka

## 5. Masalah yang sering muncul

| Gejala | Sebab biasanya | Tindakan |
|---|---|---|
| `python` tidak dikenali (Windows) | PATH tidak dicentang saat install | pakai `py`, atau install ulang dan centang "Add Python to PATH" |
| `npm run dev` jalan tapi halaman kosong | `index.html` tidak menunjuk `src/main.ts` | cek `<script type="module" src="/src/main.ts">` |
| `/health` 404 | `app.main` bukan modul yang dijalankan | jalankan `uvicorn` dari dalam folder `backend/` |
| CI merah karena `secret-scan` | ada rahasia ter-commit | **hapus nilainya, rotasi, commit ulang** — lihat Ketentuan 8 di bawah |
| `venv/` ikut ter-commit | `.gitignore` diubah | kembalikan `.gitignore` bawaan repo |
| Menu **Branches → Add rule** tidak ada | repo dibuat **Private** | Settings → General → Danger Zone → **Change visibility → Public** |
| Tidak bisa merge PR sendiri | "Require approvals" sudah dinyalakan | matikan dulu malam ini (lihat bagian 0 langkah 4) |

---

## UTS — Kelompok 02

Aplikasi ini mencatat **jadwal konsultasi pasien** di sebuah klinik. Kontrak yang dipakai saat mengimplementasikan ada di [`docs/uts-consultation-contract.md`](docs/uts-consultation-contract.md). Path-nya `/consultations`, bukan `/sessions`.

`GET /health`, CORS untuk `http://localhost:5173`, dan 12 baris fiktif di `backend/app/data.py` sudah ada. Route konsultasi dan perilaku UI belum.

### Alur aplikasi

1. Petugas membuka aplikasi dan melihat daftar jadwal konsultasi.
2. Layar punya empat keadaan: sedang memuat, ada data, tidak ada data, gagal dimuat. Gagal punya tombol coba lagi.
3. Petugas mencari nama pasien atau dokter dan berpindah halaman (`skip` / `limit`).
4. Petugas menambah jadwal lewat form. Form menolak isian yang tidak lengkap sebelum dikirim, dan menampilkan pesan error dari server.
5. Petugas menghapus satu jadwal hanya setelah konfirmasi. Daftar dimuat ulang.
6. Id yang tidak ada membalas 404. Itu diuji di `http://localhost:8000/docs`, bukan lewat halaman terpisah.

Layar daftar dibagi dua berkas. @mohammadbaiqi mengambil data dan memilih keadaan. @ghinaat hanya merender prop `items`. Keduanya tidak mengedit komponen yang sama. Di `main.py`, `schemas.py`, dan `services.py`, tambahkan fungsi atau route baru dan jangan mengubah milik anggota lain.

@ghinaat, @likicop, dan @mohammadbaiqi bisa mulai bersamaan setelah pondasi ini. Tidak ada tugas yang harus selesai sebelum anggota lain mulai menulis.

### Cara verifikasi requirement

Jalankan kedua server seperti bagian 3, lalu cek satu per satu. Yang belum diimplementasikan memang masih gagal.

| Kode | Cara cek | Status sekarang |
|---|---|---|
| B1 | `GET /consultations?skip=0&limit=5&search=sari` di `/docs`. Balasan array, terpotong halaman, dan `search` cocok ke nama pasien atau dokter tanpa memedulikan huruf besar. | Belum |
| B2 | `GET /consultations/1` membalas 200. `GET /consultations/999` membalas 404 dengan `{"detail":"Jadwal konsultasi tidak ditemukan."}`. | Belum |
| B3 | `POST /consultations` dengan body lengkap membalas 201 dan record yang punya `id`. Body tanpa `nama_pasien` membalas 422. Skema masuk tidak berisi `id`. | Belum |
| B4 | `DELETE /consultations/1` membalas 204 dengan badan kosong. Id yang tidak ada membalas 404. | Belum |
| B5 | Dari origin `http://localhost:5173`, response punya `Access-Control-Allow-Origin` itu. Origin lain tidak. | Sudah |
| F1 | Buka `http://localhost:5173`. Daftar terisi dari API saat halaman dibuka, dan permintaan dibatalkan saat halaman ditutup. | Belum |
| F2 | Throttle jaringan: terlihat loading. Data 12 baris: terlihat daftar. `search` yang tidak cocok: terlihat kosong. Backend dimatikan: terlihat error dan tombol coba lagi yang memuat ulang. | Belum |
| F3 | Form kosong tidak terkirim, dan pesan validasi tampil. Error 422 dari server juga tampil di form. | Belum |
| F4 | Hapus meminta konfirmasi. Setelah ya, daftar dimuat ulang tanpa jadwal itu. | Belum |
| Q1 | Ada `header`, `main`, dan `h1`. Setiap input form punya `<label>`. | Kerangka halaman sudah; label menunggu form |
| Q2 | Seluruh UI bisa dipakai dengan Tab dan Enter. Focus terlihat. | Belum |
| Q3 | Console browser tidak punya error atau unhandled rejection saat alur di atas dijalankan. | Belum |
| Q4 | Tidak ada berkas sumber lebih dari 100 baris. Komponen terpecah sesuai kontrak. | Belum |
| Q5 | `git log` punya minimal tiga commit yang pesannya menjelaskan perubahan. Tiap anggota commit bagiannya sendiri. | Berjalan |

### Pembagian tugas

@mupinnn memegang pondasi, jadi sisa tugas produknya kecil. Tiga anggota lain membagi fitur (19 / 19 / 20). Q5 dikerjakan bersama.

**@mupinnn — pondasi.** Kerangka backend dan frontend, kontrak termasuk prop komponen daftar, B5 CORS (2), 12 baris fiktif di `data.py`, dan Q1 (3): kerangka semantik sudah, `<label>` pada setiap input menyusul saat form ada.

Blokir: label Q1 menunggu form @likicop (F3). Aturan label sudah di kontrak, jadi @likicop tidak menunggu @mupinnn. Setelah CORS, data, dan kontrak ada, @mupinnn tidak memblokir siapa pun.

**@ghinaat — menelusuri jadwal (19).** B1 daftar + pagination + `search` (6). F1 komponen daftar dengan prop `items` saja, dirender dari data yang dimuat saat mount dan dibersihkan saat unmount (6). B2 detail 404 (4). Q2 bisa dioperasikan keyboard dan gaya focus terlihat di CSS global (3).

Blokir: tidak ada yang menghalangi mulai. Kerjakan B1 dulu supaya barisnya terlihat. Pengecekan keyboard terakhir menunggu form @likicop (F3) dan dialog hapus @mohammadbaiqi (F4). Kamu memblokir integrasi keadaan data @mohammadbaiqi sampai komponen daftar ada, dan memblokir cek keadaan kosong/data sampai B1 mengembalikan baris sungguhan. Kamu tidak memblokir mereka membangun loading, error, atau coba lagi.

**@likicop — menambah jadwal (19).** B3 buat jadwal, skema masuk dan keluar terpisah, 201 (9). F3 form, validasi klien, tampilan error server (7). Tiap input punya `<label>` sendiri; itu menyelesaikan Q1 @mupinnn. Q3 tidak ada error console dan unhandled rejection (3).

Blokir: tidak ada yang menghalangi mulai. Tampilkan error server setelah B3 milikmu sendiri jalan. Pengecekan console terakhir menunggu daftar @ghinaat serta keadaan dan dialog @mohammadbaiqi ada di halaman. Formmu memblokir @mupinnn menutup Q1, dan memblokir pengecekan keyboard terakhir @ghinaat.

**@mohammadbaiqi — keadaan layar dan membatalkan jadwal (20).** F2 loading, data, kosong, error, dan tombol coba lagi yang bekerja (11). Kamu yang memanggil API di halaman; keadaan data merender daftar @ghinaat. B4 hapus 204 (4). F4 konfirmasi hapus dan daftar dimuat ulang (3); muat ulang memanggil fungsi load milikmu sendiri. Q4 komponen terpecah, tidak ada berkas lebih dari 100 baris (2).

Blokir: loading, error, coba lagi, hapus, dan dialog konfirmasi tidak menunggu siapa pun. Cek keadaan kosong dan data menunggu B1 (@ghinaat). Mengganti `<ul>` biasa dengan komponen @ghinaat menunggu F1. Dialogmu memblokir pengecekan keyboard terakhir @ghinaat. Kamu tidak memblokir @ghinaat atau @likicop untuk mulai.

**Semua anggota — Q5 (2).** Tiap orang commit bagiannya sendiri. Repo butuh minimal tiga commit yang pesannya bermakna. Ini tidak menunggu siapa pun.

---

## Berkas siapa

| Punya kamu — kerjakan | Punya dosen — jangan diubah |
|---|---|
| `frontend/` (seluruhnya) | `verify.py` |
| `backend/` (seluruhnya) | `.github/workflows/` |
| `docs/PROJECT.md` (isian piagam) | `Dockerfile` |
| `docs/api-contract.md`, `docs/state.md` | `.gitignore`, `.env.example` |
| `CONTRIBUTORS.md` (isian nama) | `docs/DEPLOY.md` |
| `README.md` bagian 1–5 di atas | bagian **Ketentuan** di bawah |

Mengubah berkas milik dosen agar `verify.py` jadi hijau dihitung sebagai artefak yang tidak dapat
dipertahankan — nilainya 0 (Ketentuan 5).

## Peta sesi

| Sesi | Bobot | Yang jadi di ruang kelas |
|---|---|---|
| 1 | 2% | Jejak permintaan beranotasi |
| **2** | **2%** | **Repo + kerangka frontend/backend + README + 1 PR + piagam `docs/PROJECT.md`** |
| 3 | 2% | Endpoint pertama berjalan (FastAPI, Pydantic, status code) |
| 4 | **5%** | Diagram lapisan MVC + refactor satu endpoint |
| 5 | 2% | CRUD persisten + migrasi Alembic diterapkan · **pindah ke Postgres** |
| 6 | 2% | Rute + controller tipis + penanganan error terpusat |
| 7 | **5%** | `docs/api-contract.md` + model data (peer review) |
| **8** | **25%** | **UTS — ujian praktik individual** |
| 9 | 2% | Alur login berfungsi (JWT + bcrypt) |
| 10 | 2% | Otorisasi tingkat objek + RBAC |
| 11 | **5%** | Kerentanan ditemukan dan ditutup (break-in round) |
| 12 | 2% | Frontend terhubung + dua grafik + `docs/state.md` |
| 13 | 2% | Lima pengujian berjalan + tabel pengukuran di README |
| 14 | **5%** | **URL publik aktif + CI hijau** |
| 15 | 2% | **Demo The Build 8 menit di URL publik + pembelaan** |
| **16** | **25%** | **UAS — verifikasi submission + pembelaan tertulis** |

Urutan ini mengikuti RPS, bukan nomor berkas catatan mingguan.

## Ketentuan yang paling sering menghapus nilai

1. **Artefak wajib dapat dipertahankan.** Kode yang tidak bisa kamu jelaskan bernilai **0**,
   sebagus apa pun hasilnya. Berlaku juga untuk bagian yang ditulis anggota lain. Riwayat commit
   adalah bukti utama kepemilikan.
2. **Tidak dapat dijalankan = 0 fungsionalitas.** Gagal run, gagal build, atau CI merah bernilai
   0 pada komponen fungsionalitas. Aplikasi dinilai dengan **dijalankan di hadapan dosen**, bukan
   dari tangkapan layar.
3. **Tanpa commit atas namamu sendiri = 0 Tugas Kelompok**, berapa pun nilai timmu. Nilai
   individu = nilai kelompok × faktor kontribusi (0–1) dari commit/PR sendiri, peer assessment,
   dan kemampuan menjelaskan bagian **mana pun** dari kode.
4. **Kredensial ter-commit membatalkan nilai artefak sesi itu** — kunci API, kata sandi basis
   data, token. Berlaku **sejak Sesi 2**, jauh sebelum keamanan diajarkan formal. Karena itu
   `.env` ada di `.gitignore` dan CI menjalankan pemindai rahasia.
5. **Commit sebelum keluar.** Semua tenggat adalah akhir sesi. Waktu commit adalah bukti kerjamu
   dilakukan di dalam sesi.

## Penggunaan AI assistant

AI assistant **diizinkan** pada sesi praktikum, dan **dilarang pada UTS (Sesi 8) dan UAS
(Sesi 16)**. Syaratnya satu: tulis pengungkapan singkat di bawah ini, dan perbarui saat berubah.
Ketentuan 1 tetap berlaku penuh — kalau kamu tidak bisa menjelaskan kode yang dihasilkan AI,
nilainya 0.

<!-- ISI BAGIAN INI. Contoh:
- Sesi 2 — Claude, untuk menjelaskan pesan error `npm ERR! ENOENT`. Kode ditulis sendiri.
- Sesi 5 — GitHub Copilot, autocomplete pada model SQLAlchemy. Ditinjau dan diubah manual.
-->

- Pondasi UTS Kelompok 02 (kerangka backend dan frontend, kontrak, CORS, 12 baris data) disusun dengan bantuan AI assistant sebelum Sesi 8. Route konsultasi dan UI fitur belum ditulis; itu tugas anggota sesuai bagian pembagian di bawah.

## Kalau kamu tersendat

Tersendat di satu sesi tidak menghapus nilai sesi lain — **berhenti total yang menghapusnya**.
Kalau `frontend` atau `backend` tim belum jalan, tetap masuk sesi berikutnya, kerjakan yang bisa
dikerjakan, lalu minta waktu di 10 menit pertama sesi berikutnya. Lapor di thread RISE dengan
**seluruh pesan error**, bukan ringkasannya.
