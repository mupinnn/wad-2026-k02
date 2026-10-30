<script setup lang="ts">
import { reactive, ref } from "vue";
import { useAuth } from "../composables/useAuth";

const { login, loading, error } = useAuth();

const form = reactive({ email: "", password: "" });
const clientError = ref("");

async function onSubmit() {
  clientError.value = "";

  if (form.email.trim() === "" || form.password === "") {
    clientError.value = "Email dan kata sandi wajib diisi.";
    return;
  }

  // Berhasil: token tersimpan dan App.vue otomatis berganti layar.
  await login(form.email, form.password);
}
</script>

<template>
  <form class="space-y-4" novalidate @submit.prevent="onSubmit">
    <div class="space-y-1.5">
      <label for="login_email" class="text-sm font-medium text-neutral-700">Email</label>
      <input
        id="login_email"
        v-model="form.email"
        type="email"
        autocomplete="email"
        class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-neutral-500"
      />
    </div>
    <div class="space-y-1.5">
      <label for="login_password" class="text-sm font-medium text-neutral-700">Kata sandi</label>
      <input
        id="login_password"
        v-model="form.password"
        type="password"
        autocomplete="current-password"
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
      {{ loading ? "Masuk..." : "Masuk" }}
    </button>
  </form>
</template>