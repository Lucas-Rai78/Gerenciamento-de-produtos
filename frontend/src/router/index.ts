import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/produtos'
  },
  {
    path: '/produtos',
    name: 'Produtos',
    component: () => import('@/views/ProdutosView.vue')
  },
  {
    path: '/entradas',
    name: 'Entradas',
    component: () => import('@/views/EntradasView.vue')
  },
  {
    path: '/saidas',
    name: 'Saidas',
    component: () => import('@/views/SaidasView.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
