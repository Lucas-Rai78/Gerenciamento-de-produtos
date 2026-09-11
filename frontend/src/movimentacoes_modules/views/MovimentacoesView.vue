<script setup lang="ts">
import { useMovimentacoes } from '@/movimentacoes_modules/composables/useMovimentacoesView'
import MovimentacaoTable from '@/movimentacoes_modules/components/MovimentacoesTable.vue'
import MovimentacaoModal from '@/movimentacoes_modules/components/MovimentacoesForm.vue'

const {
  produtos,
  movimentacoes,
  carregando,
  erro,
  isModalOpen,
  salvarMovimentacao,
  abrirModal,
  fecharModal,
} = useMovimentacoes()
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
        @click="abrirModal"
      >
        + Registrar Movimentação
      </button>
    </div>

    <MovimentacaoTable :movimentacoes="movimentacoes" :produtos="produtos" />

    <MovimentacaoModal
      :is-open="isModalOpen"
      :produtos="produtos"
      :carregando="carregando"
      :erro="erro"
      @close="fecharModal"
      @salvar="salvarMovimentacao"
    />
  </main>
</template>
