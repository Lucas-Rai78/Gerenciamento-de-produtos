<script setup lang="ts">
import { ref } from 'vue';
import type { Produto, Categoria } from '../types/inventory';
import BaseInput from '../components/BaseInput.vue';
import BaseSelect from '../components/BaseSelect.vue';

const categorias: Categoria[] = ['estoque seco', 'doce'];

const form = ref<Produto>({
  nome: '',
  descricao: '',
  quantidadeEstoque: 0,
  estoqueMinimo: 0,
  precoUnidade: 0,
  categoria: 'estoque seco'
});

const listaProdutos = ref<Produto[]>([]);

function salvarProduto(): void {
  listaProdutos.value.push({ ...form.value, id: crypto.randomUUID() });

  // Reset do formulário
  form.value = {
    nome: '',
    descricao: '',
    quantidadeEstoque: 0,
    estoqueMinimo: 0,
    precoUnidade: 0,
    categoria: 'estoque seco'
  };
}
</script>

<template>
  <main class="container">
    <h2>Cadastro de Produtos</h2>

    <form class="form-card" @submit.prevent="salvarProduto">
      <BaseInput
        v-model="form.nome"
        label="Nome do Produto"
        placeholder="Ex: Farinha de Trigo"
        required
      />

      <BaseInput
        v-model="form.descricao"
        label="Descrição"
        placeholder="Ex: Marca X, Tipo 1"
      />

      <div class="form-row">
        <BaseSelect
          v-model="form.categoria"
          label="Categoria"
          :options="categorias"
          required
        />

        <BaseInput
          v-model.number="form.precoUnidade"
          type="number"
          label="Preço Unitário (R$)"
          step="0.01"
          required
        />
      </div>

      <div class="form-row">
        <BaseInput
          v-model.number="form.quantidadeEstoque"
          type="number"
          label="Quantidade Inicial em Estoque"
          required
        />

        <BaseInput
          v-model.number="form.estoqueMinimo"
          type="number"
          label="Estoque Mínimo"
          required
        />
      </div>

      <button type="submit" class="btn-primary">Cadastrar Produto</button>
    </form>
  </main>
</template>

<style scoped>
.container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.form-card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background-color: #2563eb;
  color: #ffffff;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #1d4ed8;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
