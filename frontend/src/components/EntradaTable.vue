<script setup lang="ts">
import type { EntradaProduto, Produto } from '@/types/produto'

const props = defineProps<{
  entradas: EntradaProduto[]
  produtos: Produto[]
  carregando: boolean
}>()

function getNomeProduto(produtoId: number | string): string {
  const prod = props.produtos.find((p) => p.id === Number(produtoId))
  return prod ? prod.nome : `Produto #${produtoId}`
}

function calcularTotal(quantidade: number, precoUnitario: number): string {
  return (quantidade * precoUnitario).toFixed(2)
}
</script>

<template>
  <section class="card">
    <h3 class="subtitle">Histórico de Entradas</h3>

    <div v-if="carregando" class="loading">Carregando entradas...</div>

    <div v-else-if="entradas.length > 0" class="table-responsive">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Produto</th>
            <th>Origem</th>
            <th>Qtd. Entrou</th>
            <th>Preço Un.</th>
            <th>Total do Lote</th>
            <th>Validade</th>
            <th>Data Entrada</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in entradas" :key="item.id">
            <td>#{{ item.id }}</td>
            <td>
              <strong>{{ getNomeProduto(item.produtoId) }}</strong>
            </td>
            <td>
              <span class="badge badge-in">{{ item.classificacao }}</span>
            </td>
            <td>+{{ item.quantidade }} {{ item.unidadeMedida }}</td>
            <td>R$ {{ item.precoUnitario.toFixed(2) }}</td>
            <td class="total-price">R$ {{ calcularTotal(item.quantidade, item.precoUnitario) }}</td>
            <td>{{ item.validade || '-' }}</td>
            <td>{{ item.dataEntrada }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="empty-msg">Nenhuma entrada registrada.</p>
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
.badge-in {
  background-color: #dcfce7;
  color: #15803d;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}
.total-price {
  font-weight: 600;
  color: #0f172a;
}
.empty-msg,
.loading {
  color: #64748b;
  text-align: center;
  padding: 1rem 0;
}
</style>
