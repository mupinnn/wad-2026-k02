<script setup lang="ts">
import { onMounted, onUnmounted, ref } from "vue";
import ConsultationForm from "./components/ConsultationForm.vue";
import ConsultationList from "./components/ConsultationList.vue";

interface Consultation {
  id: number;
  nama_pasien: string;
  nama_dokter: string;
  poli: string;
  waktu_konsultasi: string;
  keluhan: string;
}

const items = ref<Consultation[]>([]);
const searchInput = ref("");
const search = ref("");
const skip = ref(0);
const limit = 5;
const loading = ref(false);
const error = ref("");
const actionError = ref("");
const showForm = ref(false);
let activeRequest: AbortController | null = null;

async function loadConsultations() {
  activeRequest?.abort();
  const controller = new AbortController();
  activeRequest = controller;
  loading.value = true;
  error.value = "";

  const params = new URLSearchParams({
    skip: String(skip.value),
    limit: String(limit),
  });
  if (search.value) params.set("search", search.value);

  try {
    const response = await fetch(
      `http://localhost:8000/consultations?${params.toString()}`,
      { signal: controller.signal },
    );
    if (!response.ok) throw new Error("Gagal memuat jadwal konsultasi.");
        const body = (await response.json()) as { data: Consultation[] };     
        items.value = body.data;
  } catch (cause) {
    if (cause instanceof Error && cause.name !== "AbortError") {
      error.value = cause.message || "Tidak bisa menghubungi server.";
    }
  } finally {
    if (activeRequest === controller) {
      loading.value = false;
      activeRequest = null;
    }
  }
}

function submitSearch() {
  search.value = searchInput.value.trim();
  skip.value = 0;
  void loadConsultations();
}

function changePage(offset: number) {
  skip.value = Math.max(0, skip.value + offset);
  void loadConsultations();
}

function refreshAfterCreate() {
  showForm.value = false;
  void loadConsultations();
}

async function deleteConsultation(id: number) {
  if (!window.confirm("Yakin ingin menghapus jadwal konsultasi ini?")) return;

  actionError.value = "";
  try {
    const response = await fetch(`http://localhost:8000/consultations/${id}`, {
      method: "DELETE",
    });
    if (!response.ok) {
      const body = await response.json().catch(() => null);
      throw new Error(body?.detail || body?.message || "Gagal menghapus jadwal.");
    }

    if (items.value.length === 1 && skip.value > 0) {
      skip.value = Math.max(0, skip.value - limit);
    }
    await loadConsultations();
  } catch (cause) {
    actionError.value = cause instanceof Error
      ? cause.message
      : "Tidak bisa menghubungi server.";
  }
}

onMounted(() => void loadConsultations());
onUnmounted(() => activeRequest?.abort());
</script>

<template>
  <div class="min-h-screen bg-neutral-50">
    <header class="border-b bg-white px-6 py-5">
      <h1 class="mx-auto max-w-5xl text-2xl font-semibold tracking-tight">Jadwal Konsultasi</h1>
    </header>
    <main class="mx-auto max-w-5xl space-y-8 px-6 py-8">
      <section class="space-y-4" aria-label="Tambah jadwal konsultasi">
        <button
          type="button"
          class="rounded-xl bg-neutral-900 px-5 py-3 text-sm font-medium text-white hover:bg-neutral-700"
          :aria-expanded="showForm"
          @click="showForm = !showForm"
        >
          {{ showForm ? "Tutup formulir" : "Tambah jadwal" }}
        </button>
        <ConsultationForm v-if="showForm" @created="refreshAfterCreate" />
      </section>

      <section aria-labelledby="list-heading" class="space-y-5">
        <div>
          <h2 id="list-heading" class="text-xl font-semibold">Daftar jadwal</h2>
          <p class="mt-1 text-sm text-neutral-600">Cari berdasarkan nama pasien atau dokter.</p>
        </div>

        <p v-if="actionError" class="rounded-xl border border-red-200 bg-white p-4 text-sm text-red-700" role="alert">
          {{ actionError }}
        </p>

        <form class="flex gap-3" role="search" @submit.prevent="submitSearch">
          <label class="sr-only" for="consultation-search">Cari jadwal konsultasi</label>
          <input
            id="consultation-search"
            v-model="searchInput"
            type="search"
            placeholder="Cari nama pasien atau dokter"
            class="min-w-0 flex-1 rounded-xl border border-neutral-300 bg-white px-4 py-3 text-sm"
          />
          <button
            type="submit"
            class="rounded-xl bg-neutral-900 px-5 py-3 text-sm font-medium text-white hover:bg-neutral-700"
          >
            Cari
          </button>
        </form>

        <p v-if="loading" class="rounded-xl border bg-white p-6 text-sm text-neutral-600" role="status">
          Memuat jadwal...
        </p>
        <div v-else-if="error" class="rounded-xl border border-red-200 bg-white p-6" role="alert">
          <p class="text-sm text-red-700">{{ error }}</p>
          <button
            type="button"
            class="mt-3 rounded-lg border px-4 py-2 text-sm font-medium hover:bg-neutral-50"
            @click="loadConsultations"
          >
            Coba lagi
          </button>
        </div>
        <p v-else-if="items.length === 0" class="rounded-xl border bg-white p-6 text-sm text-neutral-600">
          Belum ada jadwal yang cocok.
        </p>
        <ConsultationList v-else :items="items" @delete="deleteConsultation" />

        <nav v-if="!loading && !error && items.length > 0" class="flex items-center justify-between" aria-label="Pagination">
          <button
            type="button"
            :disabled="skip === 0"
            class="rounded-lg border bg-white px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
            @click="changePage(-limit)"
          >
            Sebelumnya
          </button>
          <span class="text-sm text-neutral-600">Halaman {{ Math.floor(skip / limit) + 1 }}</span>
          <button
            type="button"
            :disabled="items.length < limit"
            class="rounded-lg border bg-white px-4 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50"
            @click="changePage(limit)"
          >
            Berikutnya
          </button>
        </nav>
      </section>
    </main>
  </div>
</template>