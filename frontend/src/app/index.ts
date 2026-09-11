import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/produtos',
  },
  {
    path: '/produtos',
    name: 'Produtos',
    component: () => import('@/produto_modules/views/ProdutosView.vue'),
  },
  { path: '/movimentacoes',
    name: 'movimentacoes',
    component:() => import('@/movimentacoes_modules/views/MovimentacoesView.vue')},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
