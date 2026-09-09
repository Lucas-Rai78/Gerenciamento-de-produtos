<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Produto } from '@/features/types/produto'
import { produtoService } from '@/features/services/produtoService'
import { movimentacaoService, type Movimentacao } from '@/features/services/movimentacaoService'
import MovimentacaoTable from '@/shared/components/MovimentacoesTable.vue'
import MovimentacaoModal from '@/shared/components/MovimentacoesForm.vue'

const produtos = ref<Produto[]>([])
const movimentacoes = ref<Movimentacao[]>([])
const carregando = ref<boolean>(false)
const erro = ref<string>('')
const isModalOpen = ref<boolean>(false)

async function carregarDados() {
  try {
    carregando.value = true
    const [prods, movs] = await Promise.all([produtoService.listar(), movimentacaoService.listar()])
    produtos.value = prods
    movimentacoes.value = movs
  } catch (e) {
    erro.value = `Falha ao carregar dados: ${e}`
  } finally {
    carregando.value = false
  }
}

async function salvarMovimentacao(dados: Omit<Movimentacao, 'id'>) {
  try {
    carregando.value = true
    erro.value = ''

    await movimentacaoService.criar(dados)
    isModalOpen.value = false
    await carregarDados()
  } catch (e) {
    erro.value = e instanceof Error ? e.message : String(e)
  } finally {
    carregando.value = false
  }
}

onMounted(() => {
  carregarDados()
})
</script>

<template>
  <main class="max-w-300 my-8 mx-auto px-6 py-0 flex flex-col gap-6">
    <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
      <h2 class="text-gray-900 text-2xl font-semibold border-l-4 border-[#00bf63] pl-2 m-0">
        Histórico de Movimentações
      </h2>
      <button
        type="button"
        class="px-3 py-5 bg-[#00bf63] text-white border-none rounded-md font-semibold cursor-pointer text-base transition-colors duration-200 hover:bg-[#01923d]"
        @click="isModalOpen = true"
      >
        + Registrar Movimentação
      </button>
    </div>

    <MovimentacaoTable
      :movimentacoes="movimentacoes"
      :produtos="produtos"
    />

    <MovimentacaoModal
      :is-open="isModalOpen"
      :produtos="produtos"
      :carregando="carregando"
      :erro="erro"
      @close="isModalOpen = false"
      @salvar="salvarMovimentacao"
    />
  </main>
</template>
