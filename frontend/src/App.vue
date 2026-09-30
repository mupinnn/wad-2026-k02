<script setup lang="ts">
import { computed, ref } from "vue";
import ConsultationDetailDialog from "./components/ConsultationDetailDialog.vue";
import ConsultationForm from "./components/ConsultationForm.vue";
import ConsultationList from "./components/ConsultationList.vue";
import DeleteConsultationDialog from "./components/DeleteConsultationDialog.vue";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useFetch } from "./composables/useFetch";

interface Consultation {
  id: number;
  nama_pasien: string;
  nama_dokter: string;
  poli: string;
  waktu_konsultasi: string;
  keluhan: string;
}

const searchInput = ref("");
const search = ref("");
const skip = ref(0);
const limit = 5;
const showForm = ref(false);
const selectedId = ref<number | null>(null);
const deleteOpen = ref(false);
const deleteId = ref(0);

const detailOpen = computed({
  get: () => selectedId.value !== null,
  set: (value: boolean) => {
    if (!value) selectedId.value = null;
  },
});

function listQuery() {
  const params = new URLSearchParams({
    skip: String(skip.value),
    limit: String(limit),
  });
  if (search.value) params.set("search", search.value);
  return `/consultations?${params.toString()}`;
}

const { data, loading, error, execute } = useFetch<{ data: Consultation[] }>({
  url: listQuery,
  method: "GET",
});

const items = computed(() => data.value?.data ?? []);

const { error: actionError, execute: remove } = useFetch({
  url: () => `/consultations/${deleteId.value}`,
  method: "DELETE",
  immediate: false,
});

function submitSearch() {
  search.value = searchInput.value.trim();
  skip.value = 0;
  void execute();
}

function changePage(offset: number) {
  skip.value = Math.max(0, skip.value + offset);
  void execute();
}

function refreshAfterCreate() {
  showForm.value = false;
  void execute();
}

function openDetail(id: number) {
  selectedId.value = id;
}

function requestDelete(id: number) {
  deleteId.value = id;
  deleteOpen.value = true;
}

async function confirmDelete() {
  await remove();
  if (actionError.value) return;

  if (items.value.length === 1 && skip.value > 0) {
    skip.value = Math.max(0, skip.value - limit);
  }
  await execute();
}
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
          @click="showForm = true"
        >
          Tambah jadwal
        </button>
        <Dialog v-model:open="showForm">
          <DialogContent class="max-h-[calc(100vh-2rem)] overflow-y-auto sm:max-w-lg">
            <DialogHeader>
              <DialogTitle>Tambah jadwal</DialogTitle>
              <DialogDescription>Isi data jadwal konsultasi baru.</DialogDescription>
            </DialogHeader>
            <ConsultationForm @created="refreshAfterCreate" />
          </DialogContent>
        </Dialog>
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

        <div v-if="error" class="rounded-xl border border-red-200 bg-white p-6" role="alert"
        >
          <p class="text-sm text-red-700">{{ error }}</p>

          <button
            type="button"
            class="mt-3 rounded-lg border px-4 py-2 text-sm font-medium hover:bg-neutral-50"
            @click="execute"
          >
            Coba lagi
          </button>
        </div>

        <ConsultationList
          v-else
          :items="items"
          :loading="loading"
          @select="openDetail"
          @delete="requestDelete"
        />

        <ConsultationDetailDialog v-model:open="detailOpen" :id="selectedId" />
        <DeleteConsultationDialog v-model:open="deleteOpen" @confirm="confirmDelete" />

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