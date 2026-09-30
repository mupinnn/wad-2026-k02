<script setup lang="ts">
import { Skeleton } from "@/components/ui/skeleton";
import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
} from "@/components/ui/empty";
import type { Consultation } from "@/interface/ConsultationInterface";

defineProps<{
  items: Consultation[];
  loading: boolean;
}>();

const emit = defineEmits<{
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
  <ul
    v-if="loading"
    class="space-y-4"
    aria-label="Memuat jadwal konsultasi"
    aria-busy="true"
  >
    <li v-for="n in 5" :key="n">
      <article
        class="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm"
      >
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div class="space-y-2">
            <Skeleton class="h-6 w-40" />
            <Skeleton class="h-4 w-56" />
          </div>

          <Skeleton class="h-7 w-32 rounded-full" />
        </div>

        <div class="mt-4 space-y-2">
          <Skeleton class="h-4 w-20" />
          <Skeleton class="h-4 w-3/4" />
        </div>

        <div class="mt-4 flex justify-end">
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
  <ul
    v-else
    class="space-y-4"
    aria-label="Daftar jadwal konsultasi"
  >
    <li v-for="item in items" :key="item.id">
      <article
        class="rounded-2xl border border-neutral-200 bg-white p-5 shadow-sm"
      >
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div>
            <h2 class="text-lg font-semibold">
              {{ item.nama_pasien }}
            </h2>

            <p class="mt-1 text-sm text-neutral-600">
              {{ item.nama_dokter }} · Poli {{ item.poli }}
            </p>
          </div>

          <time
            class="rounded-full bg-neutral-100 px-3 py-1 text-sm text-neutral-700"
            :datetime="item.waktu_konsultasi"
          >
            {{ formatWaktu(item.waktu_konsultasi) }}
          </time>
        </div>

        <p class="mt-4 text-sm text-neutral-700">
          <span class="font-medium">Keluhan:</span>
          {{ item.keluhan }}
        </p>

        <div class="mt-4 flex justify-end">
          <button
            type="button"
            class="rounded-lg border border-red-200 px-4 py-2 text-sm font-medium text-red-700 hover:bg-red-50"
            :aria-label="`Hapus jadwal ${item.nama_pasien}`"
            @click="emit('delete', item.id)"
          >
            Hapus
          </button>
        </div>
      </article>
    </li>
  </ul>
</template>
