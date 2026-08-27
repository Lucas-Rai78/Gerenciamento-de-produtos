<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { Produto, ProdutoCreate, Categoria, UnidadeMedida } from '@/types/produto';
import { produtoService } from '@/services/produtoService';
import BaseInput from '@/components/BaseInput.vue';
import BaseSelect from '@/components/BaseSelect.vue';

const categorias: Categoria[] = [
  'não perecíveis',
  'frezer',
  'hortifruti',
  'embalagens',
  'bebidas',
];

const unidadesMedida: UnidadeMedida[] = ['g', 'kg', 'mL', 'L'];

const listaProdutos = ref<Produto[]>([]);
const carregando = ref<boolean>(false);
const idEmEdicao = ref<number | null>(null);

const form = ref<ProdutoCreate>({
  nome: '',
  descricao: '',
  quantidadeEstoque: 0,
  estoqueMinimo: 0,
  precoUnidade: 0,
  peso: 'kg',
  categoria: 'não perecíveis',
});

function resetForm(): void {
  form.value = {
    nome: '',
    descricao: '',
    quantidadeEstoque: 0,
    estoqueMinimo: 0,
    precoUnidade: 0,
    peso: 'kg',
    categoria: 'não perecíveis',
  };
  idEmEdicao.value = null;
}

async function carregarProdutos(): Promise<void> {
  try {
    carregando.value = true;
    listaProdutos.value = await produtoService.listar();
  } catch (error) {
    console.error('Falha na comunicação com o backend:', error);
  } finally {
    carregando.value = false;
  }
}

async function salvarProduto(): Promise<void> {
  try {
    if (idEmEdicao.value) {
      await produtoService.atualizar(idEmEdicao.value, form.value);
    } else {
      await produtoService.criar(form.value);
    }
    resetForm();
    await carregarProdutos();
  } catch (error) {
    console.error('Erro ao salvar produto:', error);
  }
}

function prepararEdicao(prod: Produto): void {
  idEmEdicao.value = prod.id;
  form.value = {
    nome: prod.nome,
    descricao: prod.descricao,
    quantidadeEstoque: prod.quantidadeEstoque,
    estoqueMinimo: prod.estoqueMinimo,
    precoUnidade: prod.precoUnidade,
    peso: prod.peso,
    categoria: prod.categoria,
  };
}

async function excluirProduto(id: number): Promise<void> {
  if (confirm('Tem certeza que deseja remover este produto?')) {
    try {
      await produtoService.deletar(id);
      await carregarProdutos();
    } catch (error) {
      console.error('Erro ao excluir produto:', error);
    }
  }
}

onMounted(() => {
  carregarProdutos();
});
</script>

<template>
  <main class="container">
    <!-- Formulário -->
    <section class="card">
      <h2 class="title">
        {{ idEmEdicao ? 'Editar Produto' : 'Cadastro de Produtos' }}
      </h2>

      <form class="form-grid" @submit.prevent="salvarProduto">
        <BaseInput
          v-model="form.nome"
          label="Nome do Produto"
          placeholder="Ex: Queijo Mozzarella"
          required
        />

        <BaseInput
          v-model="form.descricao"
          label="Descrição"
          placeholder="Ex: Peça inteira para fatiar"
          required
        />

        <div class="form-row">
          <BaseSelect
            v-model="form.categoria"
            label="Categoria"
            :options="categorias"
            required
          />

          <BaseSelect
            v-model="form.peso"
            label="Unidade de Medida (Peso/Vol.)"
            :options="unidadesMedida"
            required
          />
        </div>

        <div class="form-row">
          <BaseInput
            v-model.number="form.precoUnidade"
            type="number"
            label="Preço Unitário (R$)"
            step="0.01"
            required
          />

          <BaseInput
            v-model.number="form.quantidadeEstoque"
            type="number"
            label="Estoque Inicial"
            required
          />
        </div>

        <BaseInput
          v-model.number="form.estoqueMinimo"
          type="number"
          label="Estoque Mínimo"
          required
        />

        <div class="actions">
          <button type="submit" class="btn-primary">
            {{ idEmEdicao ? 'Atualizar Produto' : 'Cadastrar Produto' }}
          </button>
          <button
            v-if="idEmEdicao"
            type="button"
            class="btn-secondary"
            @click="resetForm"
          >
            Cancelar
          </button>
        </div>
      </form>
    </section>

    <!-- Tabela -->
    <section class="card table-card">
      <h3 class="subtitle">Lista de Produtos</h3>
      <div v-if="carregando" class="loading">Carregando produtos...</div>

      <div v-else-if="listaProdutos.length > 0" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Categoria</th>
              <th>Preço Un.</th>
              <th>Estoque</th>
              <th>Estoque Mín.</th>
              <th>Medida</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prod in listaProdutos" :key="prod.id">
              <td>#{{ prod.id }}</td>
              <td>
                <strong>{{ prod.nome }}</strong>
                <span class="desc-text">{{ prod.descricao }}</span>
              </td>
              <td><span class="badge">{{ prod.categoria }}</span></td>
              <td>R$ {{ prod.precoUnidade.toFixed(2) }}</td>
              <td :class="{ 'low-stock': prod.quantidadeEstoque <= prod.estoqueMinimo }">
                {{ prod.quantidadeEstoque }}
              </td>
              <td>{{ prod.estoqueMinimo }}</td>
              <td>{{ prod.peso }}</td>
              <td class="action-buttons">
                <button class="btn-edit" title="Editar" @click="prepararEdicao(prod)">✏️</button>
                <button class="btn-delete" title="Excluir" @click="excluirProduto(prod.id)">🗑️</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="empty-msg">Nenhum produto cadastrado no banco.</p>
    </section>
  </main>
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

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.9rem;
}

th, td {
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

.btn-edit, .btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  font-size: 1rem;
}

.empty-msg, .loading {
  color: #64748b;
  font-size: 0.9rem;
  text-align: center;
  padding: 1rem 0;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>