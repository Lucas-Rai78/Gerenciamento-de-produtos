<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Produto, UnidadeMedida } from '@/features/types/produto'
import type { Movimentacao } from '@/features/services/movimentacaoService'
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

const unidadesMedida: UnidadeMedida[] = ['g', 'kg', 'mL', 'L']
const opcoesEntrada = ['compra', 'producao']
const opcoesSaida = ['venda', 'descarte', 'producao']

const form = ref({
  produtoId: '',
  tipo: 'entrada' as 'entrada' | 'saida',
  categoriaMovimentacao: 'compra',
  unidadeMedida: 'kg',
  quantidade: 1,
  precoUnitario: 0,
  data: new Date().toISOString().split('T')[0] ?? '',
  validade: '',
})

const categoriasDisponiveis = computed(() => {
  return form.value.tipo === 'entrada' ? opcoesEntrada : opcoesSaida
})

const produtoSelecionado = computed(() => {
  return props.produtos.find((p) => p.id === Number(form.value.produtoId))
})

const estoqueInsuficiente = computed(() => {
  if (form.value.tipo !== 'saida' || !produtoSelecionado.value) return false
  return form.value.quantidade > produtoSelecionado.value.quantidadeEstoque
})

function alterarTipo(novoTipo: 'entrada' | 'saida') {
  form.value.tipo = novoTipo
  form.value.categoriaMovimentacao = novoTipo === 'entrada' ? 'compra' : 'venda'
}

function resetForm() {
  form.value = {
    produtoId: '',
    tipo: 'entrada',
    categoriaMovimentacao: 'compra',
    unidadeMedida: 'kg',
    quantidade: 1,
    precoUnitario: 0,
    data: new Date().toISOString().split('T')[0] ?? '',
    validade: '',
  }
}

function fecharModal() {
  resetForm()
  emit('close')
}

function handleSubmit() {
  emit('salvar', {
    produto_id: Number(form.value.produtoId),
    tipo: form.value.tipo,
    categoriaMovimentacao: form.value.categoriaMovimentacao,
    unidadeMedida: form.value.unidadeMedida,
    quantidade: form.value.quantidade,
    precoUnitario: form.value.precoUnitario,
    data: form.value.data,
    validade: form.value.tipo === 'entrada' ? form.value.validade || null : null,
  })
}

watch(
  () => form.value.produtoId,
  (novoId) => {
    if (!novoId) return
    const produtoEncontrado = props.produtos.find((p) => p.id === Number(novoId))

    if (produtoEncontrado) {
      if (typeof produtoEncontrado.precoUnidade === 'number') {
        form.value.precoUnitario = produtoEncontrado.precoUnidade
      }
      if (
        produtoEncontrado.peso &&
        unidadesMedida.includes(produtoEncontrado.peso as UnidadeMedida)
      ) {
        form.value.unidadeMedida = produtoEncontrado.peso as UnidadeMedida
      }
    }
  },
)

watch(() => props.isOpen, (novoEstado) => {
  if (!novoEstado) {
    resetForm()
  }
})
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

    <p v-if="erro" class="text-red-700 bg-red-100 px-3 py-2 rounded-md text-base mb-4">{{ erro }}</p>

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
