<script setup lang="ts">
import type { ProdutoCreate, Categoria, UnidadeMedida } from '@/types/produto';
import BaseInput from '@/components/BaseInput.vue';
import BaseSelect from '@/components/BaseSelect.vue';

interface Props {
  isEditing: boolean;
  categorias: Categoria[];
  unidadesMedida: UnidadeMedida[];
}

defineProps<Props>();

const form = defineModel<ProdutoCreate>({ required: true });

const emit = defineEmits<{
  (e: 'salvar'): void;
  (e: 'cancelar'): void;
}>();
</script>

<template>
  <section class="card">
    <h2 class="title">{{ isEditing ? 'Editar Produto' : 'Cadastro de Produtos' }}</h2>

    <form class="form-grid" @submit.prevent="emit('salvar')">
      <BaseInput v-model="form.nome" label="Nome do Produto" required />
      <BaseInput v-model="form.descricao" label="Descrição" required />

      <div class="form-row">
        <BaseSelect v-model="form.categoria" label="Categoria" :options="categorias" required />
        <BaseSelect v-model="form.peso" label="Unidade de Medida" :options="unidadesMedida" required />
      </div>

      <div class="form-row">
        <BaseInput v-model.number="form.precoUnidade" type="number" label="Preço Unitário (R$)" step="0.01" required />
        <BaseInput v-model.number="form.quantidadeEstoque" type="number" label="Estoque Inicial" required />
      </div>

      <BaseInput v-model.number="form.estoqueMinimo" type="number" label="Estoque Mínimo" required />

      <div class="actions">
        <button type="submit" class="btn-primary">
          {{ isEditing ? 'Atualizar Produto' : 'Cadastrar Produto' }}
        </button>
        <button v-if="isEditing" type="button" class="btn-secondary" @click="emit('cancelar')">
          Cancelar
        </button>
      </div>
    </form>
  </section>
</template>

<style scoped>
.container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.title {
  color: #121212;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  border-left: 4px solid #00bf63;
  padding-left: 0.5rem;
}

.subtitle {
  color: #121212;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.form-grid {
  display: flex;
  flex-direction: column;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.btn-primary {
  flex: 1;
  padding: 0.75rem;
  background-color: #00bf63;
  color: #121212;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-primary:hover {
  background-color: #01923d;
  color: #ffffff;
}

.btn-secondary {
  padding: 0.75rem 1rem;
  background-color: #64748b;
  color: #ffffff;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
}

.table-responsive {
  overflow-x: auto;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
