import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/produtos',
  },
  {
    path: '/produtos',
    name: 'Produtos',
    component: () => import('@/features/views/ProdutosView.vue'),
  },
  { path: '/movimentacoes',
    name: 'movimentacoes',
    component:() => import('@/features/views/MovimentacoesView.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
