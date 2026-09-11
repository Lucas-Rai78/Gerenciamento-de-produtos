<script setup lang="ts">
import type { Produto } from '@/produto_modules/types/produto'
import type { Movimentacao } from '@/movimentacoes_modules/services/movimentacaoService'
import { useMovimentacaoForm } from '@/movimentacoes_modules/composables/useMovimentacoesForm'
import BaseInput from '@/shared/components/BaseInput.vue'
import BaseSelect from '@/shared/components/BaseSelect.vue'
import BaseModal from '@/shared/components/BaseModal.vue'

const props = defineProps<{
  isOpen: boolean
  produtos: Produto[]
  carregando: boolean
  erro: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'salvar', dados: Omit<Movimentacao, 'id'>): void
}>()

const {
  form,
  unidadesMedida,
  categoriasDisponiveis,
  produtoSelecionado,
  estoqueInsuficiente,
  alterarTipo,
  fecharModal,
  handleSubmit,
} = useMovimentacaoForm(props, emit)
</script>

<template>
  <BaseModal :is-open="isOpen" title="Registrar Movimentação" @close="fecharModal">
    <div class="flex gap-2 mb-5">
      <button
        type="button"
        :class="[
          'flex-1 p-[0.6rem] border rounded-md font-semibold cursor-pointer transition-all duration-200 ease',
          form.tipo === 'entrada'
            ? 'bg-[#00bf63] text-white border-[#00bf63]'
            : 'bg-gray-200 text-[#64748b] border-gray-300',
        ]"
        @click="alterarTipo('entrada')"
      >
        + Entrada
      </button>
      <button
        type="button"
        :class="[
          'flex-1 p-[0.6rem] border rounded-md font-semibold cursor-pointer transition-all duration-200 ease',
          form.tipo === 'saida'
            ? 'bg-red-500 text-white border-red-500'
            : 'bg-gray-200 text-[#64748b] border-gray-300',
        ]"
        @click="alterarTipo('saida')"
      >
        - Saída
      </button>
    </div>

    <p v-if="erro" class="text-red-700 bg-red-100 px-3 py-2 rounded-md text-base mb-4">
      {{ erro }}
    </p>

    <form class="flex flex-col gap-4" @submit.prevent="handleSubmit">
      <div class="flex flex-col gap-1.5">
        <label class="text-sm font-semibold text-[#334155]"
          >Produto <span class="text-red-500">*</span></label
        >
        <select
          v-model="form.produtoId"
          required
          class="p-2.5 border border-gray-300 outline-none text-base bg-white rounded-md"
        >
          <option value="" disabled selected>Selecione um produto</option>
          <option v-for="prod in produtos" :key="prod.id" :value="prod.id">
            {{ prod.nome }} (Estoque: {{ prod.quantidadeEstoque }})
          </option>
        </select>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
        <BaseSelect
          v-model="form.categoriaMovimentacao"
          label="Origem / Motivo"
          :options="categoriasDisponiveis"
          required
        />
        <BaseSelect
          v-model="form.unidadeMedida"
          label="Unidade"
          :options="unidadesMedida"
          required
        />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <BaseInput
          v-model.number="form.quantidade"
          type="number"
          label="Quantidade"
          step="any"
          :min="1"
          required
        />
        <BaseInput
          v-model.number="form.precoUnitario"
          type="number"
          label="Preço Unitário (R$)"
          step="0.01"
          required
        />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <BaseInput v-model="form.data" type="date" label="Data" required />
        <BaseInput
          v-if="form.tipo === 'entrada'"
          v-model="form.validade"
          type="date"
          label="Validade (Opcional)"
        />
      </div>

      <button
        type="submit"
        class="mt-2 py-3 px-5 bg-[#00bf63] text-white border-none rounded-md font-semibold cursor-pointer transition-colors duration-200 hover:bg-[#01923d] disabled:bg-[#94a3b8] disabled:cursor-not-allowed"
        :disabled="carregando || estoqueInsuficiente"
      >
        {{ carregando ? 'Processando...' : 'Registrar Movimentação' }}
      </button>

      <p
        v-if="estoqueInsuficiente"
        class="text-red-600 bg-red-100 rounded-md text-base py-2 px-3 mt-2"
      >
        Quantidade informada é maior que o estoque atual ({{
          produtoSelecionado?.quantidadeEstoque
        }}).
      </p>
    </form>
  </BaseModal>
</template>
