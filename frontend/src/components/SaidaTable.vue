<script setup lang="ts">
import type { SaidaProduto, Produto } from '@/types/produto'

const props = defineProps<{
  saidas: SaidaProduto[]
  produtos: Produto[]
  carregando: boolean
}>()

function getNomeProduto(produtoId: number | string): string {
  const prod = props.produtos.find((p) => p.id === Number(produtoId))
  return prod ? prod.nome : `Produto #${produtoId}`
}
</script>

<template>
  <section class="card">
    <h3 class="subtitle">Histórico de Saídas</h3>

    <div v-if="carregando" class="loading">Carregando saídas...</div>

    <div v-else-if="saidas.length > 0" class="table-responsive">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Produto</th>
            <th>Motivo</th>
            <th>Qtd. Baixada</th>
            <th>Data Saída</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in saidas" :key="item.id">
            <td>#{{ item.id }}</td>
            <td>
              <strong>{{ getNomeProduto(item.produtoId) }}</strong>
            </td>
            <td>
              <span class="badge badge-out">{{ item.motivo }}</span>
            </td>
            <td class="out-stock">-{{ item.quantidade }} {{ item.unidadeMedida }}</td>
            <td>{{ item.dataSaida }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="empty-msg">Nenhuma saída registrada.</p>
  </section>
</template>

<style scoped>
.card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}
.subtitle {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}
.table-responsive {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.9rem;
}
th,
td {
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}
.badge-out {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}
.out-stock {
  color: #dc2626;
  font-weight: 600;
}
.empty-msg,
.loading {
  color: #64748b;
  text-align: center;
  padding: 1rem 0;
}
</style>
