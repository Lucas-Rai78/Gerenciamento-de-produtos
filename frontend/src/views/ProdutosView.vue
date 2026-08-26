<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { Produto, ProdutoCreate, Categoria, UnidadeMedida } from '@/types/produto';
import { produtoService } from '@/services/produtoService';
import ProdutoForm from '@/components/ProdutoForm.vue';
import ProdutoTable from '@/components/ProdutoTable.vue';

const categorias: Categoria[] = ['não perecíveis', 'frezer', 'hortifruti', 'embalagens', 'bebidas'];
const unidadesMedida: UnidadeMedida[] = ['g', 'kg', 'mL', 'L'];

const listaProdutos = ref<Produto[]>([]);
const carregando = ref<boolean>(false);
const idEmEdicao = ref<number | null>(null);

const form = ref<ProdutoCreate>({
  nome: '', descricao: '', quantidadeEstoque: 0, estoqueMinimo: 0, precoUnidade: 0, peso: 'kg', categoria: 'não perecíveis',
});

function resetForm(): void {
  form.value = { nome: '', descricao: '', quantidadeEstoque: 0, estoqueMinimo: 0, precoUnidade: 0, peso: 'kg', categoria: 'não perecíveis' };
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
    if (idEmEdicao.value) await produtoService.atualizar(idEmEdicao.value, form.value);
    else await produtoService.criar(form.value);
    resetForm();
    await carregarProdutos();
  } catch (error) {
    console.error('Erro ao salvar produto:', error);
  }
}

function prepararEdicao(prod: Produto): void {
  idEmEdicao.value = prod.id;
  // Copia os dados do produto para o formulário
  Object.assign(form.value, prod);
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

onMounted(() => carregarProdutos());
</script>

<template>
  <main class="container">
    <ProdutoForm
      v-model="form"
      :isEditing="!!idEmEdicao"
      :categorias="categorias"
      :unidadesMedida="unidadesMedida"
      @salvar="salvarProduto"
      @cancelar="resetForm"
    />

    <ProdutoTable
      :produtos="listaProdutos"
      :carregando="carregando"
      @editar="prepararEdicao"
      @excluir="excluirProduto"
    />
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
</style>
