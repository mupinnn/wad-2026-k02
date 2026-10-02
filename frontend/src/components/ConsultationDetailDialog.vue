<script setup lang="ts">
import { computed, watch } from "vue";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { useFetch } from "../composables/useFetch";

interface Consultation {
  id: number;
  nama_pasien: string;
  nama_dokter: string;
  poli: string;
  waktu_konsultasi: string;
  keluhan: string;
}

const open = defineModel<boolean>("open", { required: true });

const props = defineProps<{
  id: number | null;
}>();

const { data, loading, error, execute } = useFetch<{ data: Consultation }>({
  url: () => `/consultations/${props.id}`,
  method: "GET",
  immediate: false,
});

const consultation = computed(() => data.value?.data ?? null);

watch(
  () => [open.value, props.id] as const,
  ([isOpen, id]) => {
    if (isOpen && id != null) void execute();
  },
);

function formatWaktu(value: string) {
  return new Date(value).toLocaleString("id-ID", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}
</script>

<template>
  <Dialog v-model:open="open">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>Detail jadwal</DialogTitle>
        <DialogDescription>
          Data lengkap jadwal konsultasi.
        </DialogDescription>
      </DialogHeader>

      <div v-if="loading" class="space-y-3" aria-busy="true">
        <Skeleton class="h-4 w-2/3" />
        <Skeleton class="h-4 w-1/2" />
        <Skeleton class="h-4 w-full" />
        <span class="sr-only">Memuat detail jadwal...</span>
      </div>

      <div v-else-if="error" role="alert" class="space-y-3">
        <p class="text-sm text-red-700">{{ error }}</p>
        <button
          type="button"
          class="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-neutral-50"
          @click="execute"
        >
          Coba lagi
        </button>
      </div>

      <dl v-else-if="consultation" class="space-y-3 text-sm">
        <div>
          <dt class="font-medium text-neutral-500">Nama pasien</dt>
          <dd class="mt-0.5 text-neutral-900">{{ consultation.nama_pasien }}</dd>
        </div>
        <div>
          <dt class="font-medium text-neutral-500">Nama dokter</dt>
          <dd class="mt-0.5 text-neutral-900">{{ consultation.nama_dokter }}</dd>
        </div>
        <div>
          <dt class="font-medium text-neutral-500">Poli</dt>
          <dd class="mt-0.5 text-neutral-900">{{ consultation.poli }}</dd>
        </div>
        <div>
          <dt class="font-medium text-neutral-500">Waktu konsultasi</dt>
          <dd class="mt-0.5 text-neutral-900">
            <time :datetime="consultation.waktu_konsultasi">
              {{ formatWaktu(consultation.waktu_konsultasi) }}
            </time>
          </dd>
        </div>
        <div>
          <dt class="font-medium text-neutral-500">Keluhan</dt>
          <dd class="mt-0.5 text-neutral-900">{{ consultation.keluhan }}</dd>
        </div>
      </dl>
    </DialogContent>
  </Dialog>
</template>
