<script setup lang="ts">
import { reactive, ref } from "vue";
import { useAuth } from "../composables/useAuth";

const { register, loading, error } = useAuth();

const form = reactive({ nama: "", email: "", password: "" });
const clientError = ref("");

async function onSubmit() {
  clientError.value = "";

  if (form.nama.trim() === "" || form.email.trim() === "" || form.password === "") {
    clientError.value = "Semua kolom wajib diisi.";
    return;
  }
  if (form.password.length < 8) {
    clientError.value = "Kata sandi minimal 8 karakter.";
    return;
  }

  // Berhasil: register langsung login, token tersimpan, App.vue berganti layar.
  await register(form.nama, form.email, form.password);
}
</script>

<template>
  <form class="space-y-4" novalidate @submit.prevent="onSubmit">
    <div class="space-y-1.5">
      <label for="register_nama" class="text-sm font-medium text-neutral-700">Nama</label>
      <input
        id="register_nama"
        v-model="form.nama"
        type="text"
        autocomplete="name"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      />
    </div>
    <div class="space-y-1.5">
      <label for="register_email" class="text-sm font-medium text-neutral-700">Email</label>
      <input
        id="register_email"
        v-model="form.email"
        type="email"
        autocomplete="email"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      />
    </div>
    <div class="space-y-1.5">
      <label for="register_password" class="text-sm font-medium text-neutral-700">Kata sandi</label>
      <input
        id="register_password"
        v-model="form.password"
        type="password"
        autocomplete="new-password"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      />
    </div>

    <p v-if="clientError" role="alert" class="text-sm text-red-600">{{ clientError }}</p>
    <p v-if="error" role="alert" class="text-sm text-red-600">{{ error }}</p>

    <button
      type="submit"
      :disabled="loading"
      class="w-full rounded-xl bg-neutral-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-neutral-700 disabled:opacity-50"
    >
      {{ loading ? "Mendaftar..." : "Daftar" }}
    </button>
  </form>
</template>