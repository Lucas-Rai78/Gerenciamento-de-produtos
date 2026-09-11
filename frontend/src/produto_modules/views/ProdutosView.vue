<script setup lang="ts">
import BaseModal from '@/shared/components/BaseModal.vue'
import ProdutoForm from '@/produto_modules/components/ProdutoForm.vue'
import ProdutoTable from '@/produto_modules/components/ProdutoTable.vue'
import { useProdutosView } from '@/produto_modules/composables/useProdutosView'

const {
  categorias,
  unidadesMedida,
  listaProdutos,
  carregando,
  idEmEdicao,
  isModalOpen,
  form,
  resetForm,
  abrirModalNovo,
  salvarProduto,
  prepararEdicao,
  excluirProduto,
} = useProdutosView()
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
