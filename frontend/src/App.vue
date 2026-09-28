<script setup lang="ts">
import ConsultationForm from "./components/ConsultationForm.vue";
</script>

<template>
  <div class="min-h-screen">
    <header class="border-b px-6 py-4">
      <h1 class="text-2xl font-semibold tracking-tight">Jadwal Konsultasi</h1>
    </header>
    <main class="px-6 py-6">
      <p class="text-muted-foreground mb-4">Pencatat jadwal konsultasi pasien.</p>
      <ConsultationForm />
    </main>
  </div>
</template>