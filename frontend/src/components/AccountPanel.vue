<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import { useFetch } from "../composables/useFetch";

interface UserProfile {
  id: number;
  nama: string;
  email: string;
  role: "user" | "admin";
}

interface ApiResponse<T> {
  status: "success";
  message: string;
  data: T;
}

interface AccountForm {
  nama: string;
  email: string;
  password: string;
}

const profileForm = reactive<AccountForm>({
  nama: "",
  email: "",
  password: "",
});
const createForm = reactive<AccountForm & { role: "user" | "admin" }>({
  nama: "",
  email: "",
  password: "",
  role: "user",
});
const profileMessage = ref("");
const createMessage = ref("");

const {
  data: profileResponse,
  loading: loadingProfile,
  error: profileError,
  execute: loadProfile,
} = useFetch<ApiResponse<UserProfile>>({
  url: "/users/me",
});

const { loading: savingProfile, error: saveError, execute: saveProfile } =
  useFetch<ApiResponse<UserProfile>>({
    url: "/users/me",
    method: "PATCH",
    immediate: false,
    body: () => ({
      nama: profileForm.nama.trim(),
      email: profileForm.email.trim().toLowerCase(),
      ...(profileForm.password ? { password: profileForm.password } : {}),
    }),
  });

const { loading: creatingAccount, error: createError, execute: createAccount } =
  useFetch<ApiResponse<UserProfile>>({
    url: "/users",
    method: "POST",
    immediate: false,
    body: () => ({
      nama: createForm.nama.trim(),
      email: createForm.email.trim().toLowerCase(),
      password: createForm.password,
      role: createForm.role,
    }),
  });

async function submitProfile() {
  profileMessage.value = "";
  saveError.value = null;
  await saveProfile();
  if (saveError.value) return;

  profileForm.password = "";
  profileMessage.value = "Profil berhasil diperbarui.";
  await loadProfile();
  if (!profileError.value) syncProfileForm();
}

async function submitAccount() {
  createMessage.value = "";
  createError.value = null;
  await createAccount();
  if (createError.value) return;

  createForm.nama = "";
  createForm.email = "";
  createForm.password = "";
  createForm.role = "user";
  createMessage.value = "Akun berhasil dibuat.";
}

function syncProfileForm() {
  const profile = profileResponse.value?.data;
  if (!profile) return;
  profileForm.nama = profile.nama;
  profileForm.email = profile.email;
}

watch(profileResponse, syncProfileForm, { immediate: true });
</script>

<template>
  <section class="mx-auto max-w-3xl space-y-8">
    <div class="space-y-1">
      <h2 class="text-xl font-semibold">Akun saya</h2>
      <p class="text-sm text-neutral-600">Lihat dan perbarui informasi profil Anda.</p>
    </div>

    <div v-if="loadingProfile" class="rounded-xl border bg-white p-5 text-sm text-neutral-600" aria-live="polite">
      Memuat profil...
    </div>

    <div v-else-if="profileError" class="rounded-xl border border-red-200 bg-white p-5" role="alert">
      <p class="text-sm text-red-700">{{ profileError }}</p>
      <button
        type="button"
        class="mt-3 rounded-lg border px-4 py-2 text-sm font-medium hover:bg-neutral-50"
        @click="loadProfile().then(syncProfileForm)"
      >
        Coba lagi
      </button>
    </div>

    <template v-else-if="profileResponse?.data">
      <form class="space-y-4 rounded-xl border bg-white p-5" @submit.prevent="submitProfile">
        <p class="text-sm text-neutral-600">
          Masuk sebagai {{ profileResponse.data.role === "admin" ? "admin" : "pengguna" }}.
        </p>

        <div class="space-y-1.5">
          <label for="profile-name" class="text-sm font-medium text-neutral-700">Nama</label>
          <input
            id="profile-name"
            v-model="profileForm.nama"
            required
            autocomplete="name"
            class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm"
          />
        </div>

        <div class="space-y-1.5">
          <label for="profile-email" class="text-sm font-medium text-neutral-700">Email</label>
          <input
            id="profile-email"
            v-model="profileForm.email"
            type="email"
            required
            autocomplete="email"
            class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm"
          />
        </div>

        <div class="space-y-1.5">
          <label for="profile-password" class="text-sm font-medium text-neutral-700">
            Kata sandi baru <span class="font-normal text-neutral-500">(opsional)</span>
          </label>
          <input
            id="profile-password"
            v-model="profileForm.password"
            type="password"
            autocomplete="new-password"
            class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm"
          />
        </div>

        <p v-if="profileMessage" class="text-sm text-green-700" role="status">{{ profileMessage }}</p>
        <p v-if="saveError" class="text-sm text-red-700" role="alert">{{ saveError }}</p>

        <button
          type="submit"
          :disabled="savingProfile"
          class="rounded-xl bg-neutral-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-neutral-700 disabled:opacity-50"
        >
          {{ savingProfile ? "Menyimpan..." : "Simpan profil" }}
        </button>
      </form>

      <form
        v-if="profileResponse.data.role === 'admin'"
        class="space-y-4 rounded-xl border bg-white p-5"
        @submit.prevent="submitAccount"
      >
        <div class="space-y-1">
          <h3 class="font-semibold">Buat akun</h3>
          <p class="text-sm text-neutral-600">Tambahkan pengguna tanpa mengubah sesi admin ini.</p>
        </div>

        <div class="space-y-1.5">
          <label for="new-account-name" class="text-sm font-medium text-neutral-700">Nama</label>
          <input
            id="new-account-name"
            v-model="createForm.nama"
            required
            autocomplete="off"
            class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm"
          />
        </div>

        <div class="space-y-1.5">
          <label for="new-account-email" class="text-sm font-medium text-neutral-700">Email</label>
          <input
            id="new-account-email"
            v-model="createForm.email"
            type="email"
            required
            autocomplete="off"
            class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm"
          />
        </div>

        <div class="space-y-1.5">
          <label for="new-account-password" class="text-sm font-medium text-neutral-700">Kata sandi</label>
          <input
            id="new-account-password"
            v-model="createForm.password"
            type="password"
            required
            autocomplete="new-password"
            class="block w-full rounded-xl border border-neutral-300 px-3 py-2 text-sm"
          />
        </div>

        <div class="space-y-1.5">
          <label for="new-account-role" class="text-sm font-medium text-neutral-700">Peran</label>
          <select
            id="new-account-role"
            v-model="createForm.role"
            class="block w-full rounded-xl border border-neutral-300 bg-white px-3 py-2 text-sm"
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <p v-if="createMessage" class="text-sm text-green-700" role="status">{{ createMessage }}</p>
        <p v-if="createError" class="text-sm text-red-700" role="alert">{{ createError }}</p>

        <button
          type="submit"
          :disabled="creatingAccount"
          class="rounded-xl bg-neutral-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-neutral-700 disabled:opacity-50"
        >
          {{ creatingAccount ? "Membuat akun..." : "Buat akun" }}
        </button>
      </form>
    </template>
  </section>
</template>