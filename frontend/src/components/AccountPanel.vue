<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
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

const profileOpen = ref(false);
const createOpen = ref(false);
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

function syncProfileForm() {
  const profile = profileResponse.value?.data;
  if (!profile) return;
  profileForm.nama = profile.nama;
  profileForm.email = profile.email;
}

function openProfile() {
  syncProfileForm();
  profileForm.password = "";
  saveError.value = null;
  profileOpen.value = true;
}

function openCreate() {
  createForm.nama = "";
  createForm.email = "";
  createForm.password = "";
  createForm.role = "user";
  createError.value = null;
  createOpen.value = true;
}

async function submitProfile() {
  saveError.value = null;
  await saveProfile();
  if (saveError.value) return;

  profileForm.password = "";
  profileOpen.value = false;
  await loadProfile();
  if (!profileError.value) syncProfileForm();
}

async function submitAccount() {
  createError.value = null;
  await createAccount();
  if (createError.value) return;

  createOpen.value = false;
}

watch(profileResponse, syncProfileForm, { immediate: true });
</script>

<template>
  <section class="space-y-4" aria-label="Akun">
    <div v-if="loadingProfile" class="text-sm text-neutral-600" aria-live="polite">
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

    <div v-else-if="profileResponse?.data" class="flex flex-wrap gap-3">
      <button
        type="button"
        class="rounded-xl bg-neutral-900 px-5 py-3 text-sm font-medium text-white hover:bg-neutral-700"
        @click="openProfile"
      >
        Ubah profil
      </button>
      <button
        v-if="profileResponse.data.role === 'admin'"
        type="button"
        class="rounded-xl bg-neutral-900 px-5 py-3 text-sm font-medium text-white hover:bg-neutral-700"
        @click="openCreate"
      >
        Buat akun
      </button>
    </div>

    <Dialog v-model:open="profileOpen">
      <DialogContent class="max-h-[calc(100vh-2rem)] overflow-y-auto sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Ubah profil</DialogTitle>
          <DialogDescription>
            Masuk sebagai {{ profileResponse?.data?.role === "admin" ? "admin" : "pengguna" }}.
          </DialogDescription>
        </DialogHeader>
        <form class="space-y-4" @submit.prevent="submitProfile">
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
          <p v-if="saveError" class="text-sm text-red-700" role="alert">{{ saveError }}</p>
          <button
            type="submit"
            :disabled="savingProfile"
            class="w-full rounded-xl bg-neutral-900 px-4 py-2 text-sm font-medium text-white hover:bg-neutral-700 disabled:opacity-50"
          >
            {{ savingProfile ? "Menyimpan..." : "Simpan profil" }}
          </button>
        </form>
      </DialogContent>
    </Dialog>

    <Dialog v-model:open="createOpen">
      <DialogContent class="max-h-[calc(100vh-2rem)] overflow-y-auto sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Buat akun</DialogTitle>
          <DialogDescription>Tambahkan pengguna tanpa mengubah sesi admin ini.</DialogDescription>
        </DialogHeader>
        <form class="space-y-4" @submit.prevent="submitAccount">
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
          <p v-if="createError" class="text-sm text-red-700" role="alert">{{ createError }}</p>
          <button
            type="submit"
            :disabled="creatingAccount"
            class="w-full rounded-xl bg-neutral-900 px-4 py-2 text-sm font-medium text-white hover:bg-neutral-700 disabled:opacity-50"
          >
            {{ creatingAccount ? "Membuat akun..." : "Buat akun" }}
          </button>
        </form>
      </DialogContent>
    </Dialog>
  </section>
</template>
