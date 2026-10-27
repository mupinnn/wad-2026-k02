<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import { useFetch } from "../composables/useFetch";

interface Consultation {
    id: number;
    nama_pasien: string;
    nama_dokter: string;
    poli: string;
    waktu_konsultasi: string;
    keluhan: string;
}

const props = defineProps<{ consultation: Consultation | null }>();
const emit = defineEmits<{ saved: []; close: [] }>();

const form = reactive({
    nama_pasien: "",
    nama_dokter: "",
    poli: "",
    waktu_konsultasi: "",
    keluhan: "",
});

const clientError = ref("");

// ISO UTC dari server -> format datetime-local (waktu lokal browser)
function toLocalInput(iso: string) {
    const d = new Date(iso);
    const pad = (n: number) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

const { loading: submitting, error: serverError, execute } = useFetch({
    url: () => `/consultations/${props.consultation?.id}`,
    method: "PATCH",
    immediate: false,
    body: () => ({
        ...form,
        waktu_konsultasi: new Date(form.waktu_konsultasi).toISOString(),

    }),

});

// Isi form setiap kali dialog dibuka dengan data baru
watch(
    () => props.consultation,
    (c) => {
        if (!c) return;
        form.nama_pasien = c.nama_pasien;
        form.nama_dokter = c.nama_dokter;
        form.poli = c.poli;
        form.waktu_konsultasi = toLocalInput(c.waktu_konsultasi);
        form.keluhan = c.keluhan;
        clientError.value = "";
        serverError.value = null;
    },
    { immediate: true },
);

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

    console.log("Request URL:", `/consultations/${props.consultation?.id}`);
    console.log("Request Method:", "PATCH");

    await execute();
    if (serverError.value) return;

    emit("saved");
    emit("close");
}
</script>

<template>
  <form class="space-y-4" @submit.prevent="onSubmit">
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
      {{ submitting ? "Menyimpan..." : "Edit Jadwal" }}
    </button>
  </form>
</template>