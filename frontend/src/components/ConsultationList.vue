<script setup lang="ts">
import { Skeleton } from "@/components/ui/skeleton";
import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
} from "@/components/ui/empty";

interface Consultation {
  id: number;
  nama_pasien: string;
  nama_dokter: string;
  poli: string;
  waktu_konsultasi: string;
  keluhan: string;
}

defineProps<{
  items: Consultation[];
  loading: boolean;
}>();

const emit = defineEmits<{
  select: [id: number];
  delete: [id: number];
}>();

function formatWaktu(value: string) {
  return new Date(value).toLocaleString("id-ID", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}
</script>

<template>
  <!-- Loading Skeleton -->
  <ul v-if="loading" class="space-y-4" aria-label="Memuat jadwal konsultasi" aria-busy="true">
    <li v-for="n in 5" :key="n">
      <article class="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
        <div class="flex items-center justify-between gap-3">
          <div class="space-y-2">
            <Skeleton class="h-6 w-40" />
            <Skeleton class="h-4 w-56" />
            <Skeleton class="h-4 w-32" />
          </div>

          <Skeleton class="h-9 w-20 rounded-lg" />
        </div>
      </article>
    </li>

    <span class="sr-only">Memuat jadwal konsultasi...</span>
  </ul>

  <!-- Empty State -->
  <Empty v-else-if="items.length === 0">
    <EmptyHeader>
      <EmptyTitle>Belum ada jadwal konsultasi</EmptyTitle>

      <EmptyDescription>
        Tidak ada jadwal yang cocok dengan pencarian kamu.
      </EmptyDescription>
    </EmptyHeader>
  </Empty>

  <!-- Daftar Konsultasi -->
  <ul v-else class="space-y-4" aria-label="Daftar jadwal konsultasi">
    <li v-for="item in items" :key="item.id">
      <article
        class="flex items-center justify-between gap-3 rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm">
        <button type="button"
          class="min-w-0 flex-1 cursor-pointer rounded-lg text-left outline-none focus-visible:ring-2 focus-visible:ring-neutral-400"
          @click="emit('select', item.id)">
          <h2 class="text-lg font-semibold">
            {{ item.nama_pasien }}
          </h2>

          <p class="mt-1 text-sm text-neutral-600">
            {{ item.nama_dokter }}
          </p>

          <time class="mt-1 block text-sm text-neutral-500" :datetime="item.waktu_konsultasi">
            {{ formatWaktu(item.waktu_konsultasi) }}
          </time>
        </button>

        <button type="button"
          class="shrink-0 rounded-lg border border-red-200 px-4 py-2 text-sm font-medium text-red-700 hover:bg-red-50 focus-visible:ring-2 focus-visible:ring-red-300 focus-visible:outline-none"
          :aria-label="`Hapus jadwal ${item.nama_pasien}`" @click.stop="emit('delete', item.id)">
          Hapus
        </button>
      </article>
    </li>
  </ul>
</template>
