<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Produto, ProdutoCreate, Categoria, UnidadeMedida } from '@/types/produto'
import { produtoService } from '@/services/produtoService'
import BaseModal from '@/components/BaseModal.vue'
import ProdutoForm from '@/components/ProdutoForm.vue'
import ProdutoTable from '@/components/ProdutoTable.vue'

const categorias: Categoria[] = ['não perecíveis', 'frezer', 'hortifruti', 'embalagens', 'bebidas']
const unidadesMedida: UnidadeMedida[] = ['g', 'kg', 'mL', 'L']

const listaProdutos = ref<Produto[]>([])
const carregando = ref<boolean>(false)
const idEmEdicao = ref<number | null>(null)
const isModalOpen = ref<boolean>(false)

const form = ref<ProdutoCreate>({
  nome: '',
  descricao: '',
  quantidadeEstoque: 0,
  estoqueMinimo: 0,
  precoUnidade: 0,
  peso: 'kg',
  categoria: 'não perecíveis',
})

function resetForm(): void {
  form.value = {
    nome: '',
    descricao: '',
    quantidadeEstoque: 0,
    estoqueMinimo: 0,
    precoUnidade: 0,
    peso: 'kg',
    categoria: 'não perecíveis',
  }
  idEmEdicao.value = null
  isModalOpen.value = false
}

function abrirModalNovo(): void {
  resetForm()
  isModalOpen.value = true
}

async function carregarProdutos(): Promise<void> {
  try {
    carregando.value = true
    listaProdutos.value = await produtoService.listar()
  } catch (error) {
    console.error('Falha na comunicação com o backend:', error)
  } finally {
    carregando.value = false
  }
}

async function salvarProduto(): Promise<void> {
  try {
    if (idEmEdicao.value) {
      await produtoService.atualizar(idEmEdicao.value, form.value)
    } else {
      await produtoService.criar(form.value)
    }
    resetForm()
    await carregarProdutos()
  } catch (error) {
    console.error('Erro ao salvar produto:', error)
  }
}

function prepararEdicao(prod: Produto): void {
  idEmEdicao.value = prod.id
  form.value = {
    nome: prod.nome,
    descricao: prod.descricao,
    quantidadeEstoque: prod.quantidadeEstoque,
    estoqueMinimo: prod.estoqueMinimo,
    precoUnidade: prod.precoUnidade,
    peso: prod.peso,
    categoria: prod.categoria,
  }
  isModalOpen.value = true
}

async function excluirProduto(id: number): Promise<void> {
  if (confirm('Tem certeza que deseja remover este produto?')) {
    try {
      await produtoService.deletar(id)
      await carregarProdutos()
    } catch (error) {
      alert(`Erro ao excluir: ${error instanceof Error ? error.message : String(error)}`)
    }
  }
}

onMounted(() => {
  carregarProdutos()
})
</script>

<template>
  <main class="max-w-300 mx-auto my-8 px-6 flex flex-col gap-6">
    <div class="flex justify-between items-center flex-wrap gap-4">
    <h2 class="text-[#121212] text-2xl font-semibold border-l-4 border-[#00bf63] pl-2">
      Cadastro de Produtos
      </h2>
      <button
        type="button"
        class="py-3 px-5 bg-[#00bf63] text-white border-none rounded-md font-semibold text-base cursor-pointer hover:bg-[#01923d] transition-colors"
        @click="abrirModalNovo"
      >
        + Cadastrar Produto
      </button>
    </div>

    <ProdutoTable
      :produtos="listaProdutos"
      :carregando="carregando"
      @editar="prepararEdicao"
      @excluir="excluirProduto"
    />

    <BaseModal
      :is-open="isModalOpen"
      :title="idEmEdicao ? 'Editar Produto' : 'Cadastrar Novo Produto'"
      @close="resetForm"
    >
      <ProdutoForm
        v-model="form"
        :is-editing="!!idEmEdicao"
        :categorias="categorias"
        :unidades-medida="unidadesMedida"
        @salvar="salvarProduto"
        @cancelar="resetForm"
      />
    </BaseModal>
  </main>
</template>
