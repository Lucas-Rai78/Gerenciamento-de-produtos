<script setup lang="ts">
import { ref } from 'vue'

interface NavRoute {
  name: string
  path: string
  label: string
}

const routes: NavRoute[] = [
  { name: 'produtos', path: '/produtos', label: 'Produtos' },
  { name: 'movimentacoes', path: '/movimentacoes', label: 'Movimentações' },
]

const menuAberto = ref<boolean>(false)

function toggleMenu(): void {
  menuAberto.value = !menuAberto.value
}
</script>

<template>
  <header class="flex items-center justify-between bg-[#00bf63] px-6! py-3! text-gray-900 shadow-md">
    <div class="flex items-center gap-2">
      <h1 class="text-5 font-semibold m-0">Sistema LaPiazza</h1>
    </div>

    <button class="hidden max-md:block bg-transparent border-none text-gray-100 text-2xl cursor-pointer" aria-label="Abrir Menu" @click="toggleMenu">☰</button>

    <nav class="flex gap-2 max-md:hidden max-md:absolute max-md:top-15 max-md:inset-x-0 max-md:flex-col max-md:bg-[#00bf63] max-md:p-4 max-md:gap-2 max-md:shadow-xl max-md:z-50 [&.is-open]:max-md:flex" :class="{ 'is-open': menuAberto }">
      <router-link
        v-for="route in routes"
        :key="route.name"
        :to="route.path"
        class="text-gray-900 decoration-none px-3.5! py-2! text-base font-semibold transition-all ease-in-out duration-200 hover:text-white"
        active-class="text-white "
        @click="menuAberto = false"
      >
        {{ route.label }}
      </router-link>
    </nav>
  </header>
</template>
