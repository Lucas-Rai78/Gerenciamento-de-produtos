import { ref } from 'vue'

export interface NavRoute {
  name: string
  path: string
  label: string
}

const ROUTES: NavRoute[] = [
  { name: 'produtos', path: '/produtos', label: 'Produtos' },
  { name: 'movimentacoes', path: '/movimentacoes', label: 'Movimentações' },
]

export function useNavbar() {
  const menuAberto = ref<boolean>(false)

  function toggleMenu(): void {
    menuAberto.value = !menuAberto.value
  }

  function fecharMenu(): void {
    menuAberto.value = false
  }

  return {
    routes: ROUTES,
    menuAberto,
    toggleMenu,
    fecharMenu,
  }
}
