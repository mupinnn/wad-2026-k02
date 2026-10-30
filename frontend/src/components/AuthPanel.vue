<script setup lang="ts">
import { ref } from "vue";
import LoginForm from "./LoginForm.vue";
import RegisterForm from "./RegisterForm.vue";

const mode = ref<"login" | "register">("login");
</script>

<template>
  <section
    class="mx-auto w-full max-w-md space-y-5 rounded-2xl border bg-white p-6"
    aria-labelledby="auth-heading"
  >
    <h2 id="auth-heading" class="text-xl font-semibold">
      {{ mode === "login" ? "Masuk" : "Buat akun" }}
    </h2>

    <LoginForm v-if="mode === 'login'" />
    <RegisterForm v-else />

    <p class="text-sm text-neutral-600">
      {{ mode === "login" ? "Belum punya akun?" : "Sudah punya akun?" }}
      <button
        type="button"
        class="font-medium text-neutral-900 underline"
        @click="mode = mode === 'login' ? 'register' : 'login'"
      >
        {{ mode === "login" ? "Daftar" : "Masuk" }}
      </button>
    </p>
  </section>
</template>