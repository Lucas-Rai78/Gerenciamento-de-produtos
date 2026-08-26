<script setup lang="ts">
import type { Produto } from '@/types/produto'

defineProps<{
  produtos: Produto[]
  carregando: boolean
}>()

const emit = defineEmits<{
  (e: 'editar', produto: Produto): void
  (e: 'excluir', id: number): void
}>()
</script>

<template>
  <section class="card table-card">
    <h3 class="subtitle">Lista de Produtos</h3>

    <div v-if="carregando" class="loading">Carregando produtos...</div>

    <div v-else-if="produtos.length > 0" class="table-responsive">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Categoria</th>
            <th>Preço Un.</th>
            <th>Estoque</th>
            <th>Medida</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prod in produtos" :key="prod.id">
            <td>#{{ prod.id }}</td>
            <td>
              <strong>{{ prod.nome }}</strong>
              <span class="desc-text">{{ prod.descricao }}</span>
            </td>
            <td>
              <span class="badge">{{ prod.categoria }}</span>
            </td>
            <td>R$ {{ prod.precoUnidade.toFixed(2) }}</td>
            <td :class="{ 'low-stock': prod.quantidadeEstoque <= prod.estoqueMinimo }">
              {{ prod.quantidadeEstoque }}
            </td>
            <td>{{ prod.peso }}</td>
            <td class="action-buttons">
              <button class="btn-edit" title="Editar" @click="emit('editar', prod)">✏️</button>
              <button class="btn-delete" title="Excluir" @click="emit('excluir', prod.id)">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="empty-msg">Nenhum produto cadastrado no banco.</p>
  </section>
</template>

<style scoped>
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

th {
  color: #475569;
  font-weight: 600;
}

.desc-text {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
}

.badge {
  background-color: #e2e8f0;
  color: #334155;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
}

.low-stock {
  color: #dc2626;
  font-weight: 600;
}

.action-buttons {
  display: flex;
  gap: 0.25rem;
}

.btn-edit,
.btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  font-size: 1rem;
}

.empty-msg,
.loading {
  color: #64748b;
  font-size: 0.9rem;
  text-align: center;
  padding: 1rem 0;
}
</style>
