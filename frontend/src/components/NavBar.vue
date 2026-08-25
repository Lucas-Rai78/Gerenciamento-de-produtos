<script setup lang="ts">
import { ref } from 'vue'

interface NavRoute {
  name: string
  path: string
  label: string
}

const routes: NavRoute[] = [
  { name: 'produtos', path: '/produtos', label: 'Produtos' },
  { name: 'entradas', path: '/entradas', label: 'Entrada de Produtos' },
  { name: 'saidas', path: '/saidas', label: 'Saída de Produtos' },
]

const menuAberto = ref<boolean>(false)

function toggleMenu(): void {
  menuAberto.value = !menuAberto.value
}
</script>

<template>
  <header class="navbar-container">
    <div class="brand">
      <h1 class="logo-title">Sistema LaPiazza</h1>
    </div>

    <button class="menu-toggle" aria-label="Abrir Menu" @click="toggleMenu">☰</button>

    <nav class="nav-menu" :class="{ 'is-open': menuAberto }">
      <router-link
        v-for="route in routes"
        :key="route.name"
        :to="route.path"
        class="nav-link"
        active-class="nav-link-active"
        @click="menuAberto = false"
      >
        {{ route.label }}
      </router-link>
    </nav>
  </header>
</template>

<style scoped>
.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #00bf63;
  padding: 0.75rem 1.5rem;
  color: #121212;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);

}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.nav-menu {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  color: #121212;
  text-decoration: none;
  padding: 0.5rem 0.875rem;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: #d0cfcf;
}

.nav-link-active {
  color: #ffffff;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: #f8fafc;
  font-size: 1.5rem;
  cursor: pointer;
}

@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .nav-menu {
    display: none;
    position: absolute;
    top: 60px;
    left: 0;
    right: 0;
    flex-direction: column;
    background-color: #01923d;
    padding: 1rem;
    gap: 0.5rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    z-index: 50;
  }

  .nav-menu.is-open {
    display: flex;
  }
}
</style>
