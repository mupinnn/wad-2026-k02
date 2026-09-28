<script setup lang="ts">
import { reactive, ref } from "vue";

const emit = defineEmits<{ created: [] }>();

const form = reactive({
  nama_pasien: "",
  nama_dokter: "",
  poli: "",
  waktu_konsultasi: "",
  keluhan: "",
});

const clientError = ref("");
const serverError = ref("");
const submitting = ref(false);

function isLengkap() {
  return Object.values(form).every((v) => v.trim() !== "");
}

async function onSubmit() {
  clientError.value = "";
  serverError.value = "";

  if (!isLengkap()) {
    clientError.value = "Semua kolom wajib diisi.";
    return;
  }

  submitting.value = true;
  try {
    const res = await fetch("http://localhost:8000/consultations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...form,
        waktu_konsultasi: new Date(form.waktu_konsultasi).toISOString(),
      }),
    });

    if (!res.ok) {
      const body = await res.json().catch(() => null);
      serverError.value = body?.detail
        ? JSON.stringify(body.detail)
        : "Gagal menyimpan jadwal.";
      return;
    }

    Object.keys(form).forEach((k) => (form[k as keyof typeof form] = ""));
    emit("created");
  } catch {
    serverError.value = "Tidak bisa menghubungi server.";
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form
    class="mx-auto max-w-xl space-y-4 rounded-2xl border border-neutral-200 bg-white p-6 shadow-sm"
    @submit.prevent="onSubmit"
  >
    <div class="space-y-1.5">
      <label for="nama_pasien" class="text-sm font-medium text-neutral-700">Nama pasien</label>
      <input
        id="nama_pasien"
        v-model="form.nama_pasien"
        type="text"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      />
    </div>
    <div class="space-y-1.5">
      <label for="nama_dokter" class="text-sm font-medium text-neutral-700">Nama dokter</label>
      <input
        id="nama_dokter"
        v-model="form.nama_dokter"
        type="text"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      />
    </div>
    <div class="space-y-1.5">
      <label for="poli" class="text-sm font-medium text-neutral-700">Poli</label>
      <input
        id="poli"
        v-model="form.poli"
        type="text"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      />
    </div>
    <div class="space-y-1.5">
      <label for="waktu_konsultasi" class="text-sm font-medium text-neutral-700">Waktu konsultasi</label>
      <input
        id="waktu_konsultasi"
        v-model="form.waktu_konsultasi"
        type="datetime-local"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      />
    </div>
    <div class="space-y-1.5">
      <label for="keluhan" class="text-sm font-medium text-neutral-700">Keluhan</label>
      <textarea
        id="keluhan"
        v-model="form.keluhan"
        rows="3"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      ></textarea>
    </div>

    <p v-if="clientError" class="text-sm text-red-600">{{ clientError }}</p>
    <p v-if="serverError" class="text-sm text-red-600">{{ serverError }}</p>

    <button
      type="submit"
      :disabled="submitting"
      class="w-full rounded-xl bg-neutral-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-neutral-700 disabled:opacity-50"
    >
      {{ submitting ? "Menyimpan..." : "Tambah jadwal" }}
    </button>
  </form>
</template>