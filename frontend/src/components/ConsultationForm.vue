<script setup lang="ts">
import { reactive, ref } from "vue";
import { useFetch } from "../composables/useFetch";

const emit = defineEmits<{ created: [] }>();

const form = reactive({
  nama_pasien: "",
  nama_dokter: "",
  poli: "",
  waktu_konsultasi: "",
  keluhan: "",
});

const clientError = ref("");

const { loading: submitting, error: serverError, execute } = useFetch({
  url: "/consultations",
  method: "POST",
  immediate: false,
  body: () => ({
    ...form,
    waktu_konsultasi: new Date(form.waktu_konsultasi).toISOString(),
  }),
});

function isLengkap() {
  return Object.values(form).every((v) => v.trim() !== "");
}

async function onSubmit() {
  clientError.value = "";
  serverError.value = null;

  if (!isLengkap()) {
    clientError.value = "Semua kolom wajib diisi.";
    return;
  }

  await execute();
  if (serverError.value) return;

  Object.keys(form).forEach((k) => (form[k as keyof typeof form] = ""));
  emit("created");
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