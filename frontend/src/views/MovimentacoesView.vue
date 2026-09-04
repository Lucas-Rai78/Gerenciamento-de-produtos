<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import type { Produto, UnidadeMedida } from '@/types/produto'
import { produtoService } from '@/services/produtoService'
import { movimentacaoService, type Movimentacao } from '@/services/movimentacaoService'
import BaseInput from '@/components/BaseInput.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import BaseModal from '@/components/BaseModal.vue'

const unidadesMedida: UnidadeMedida[] = ['g', 'kg', 'mL', 'L']
const opcoesEntrada = ['compra', 'producao']
const opcoesSaida = ['venda', 'descarte', 'producao']

const produtos = ref<Produto[]>([])
const movimentacoes = ref<Movimentacao[]>([])
const carregando = ref<boolean>(false)
const erro = ref<string>('')
const isModalOpen = ref<boolean>(false)

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
  return produtos.value.find((p) => p.id === Number(form.value.produtoId))
})

const estoqueInsuficiente = computed(() => {
  if (form.value.tipo !== 'saida' || !produtoSelecionado.value) return false
  return form.value.quantidade > produtoSelecionado.value.quantidadeEstoque
})

function alterarTipo(novoTipo: 'entrada' | 'saida') {
  form.value.tipo = novoTipo
  form.value.categoriaMovimentacao = novoTipo === 'entrada' ? 'compra' : 'venda'
}

function getNomeProduto(produtoId: number): string {
  const prod = produtos.value.find((p) => p.id === produtoId)
  return prod ? prod.nome : `Produto #${produtoId}`
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
  isModalOpen.value = false
}

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

async function salvarMovimentacao() {
  try {
    carregando.value = true
    erro.value = ''

    await movimentacaoService.criar({
      produto_id: Number(form.value.produtoId),
      tipo: form.value.tipo,
      categoriaMovimentacao: form.value.categoriaMovimentacao,
      unidadeMedida: form.value.unidadeMedida,
      quantidade: form.value.quantidade,
      precoUnitario: form.value.precoUnitario,
      data: form.value.data,
      validade: form.value.tipo === 'entrada' ? form.value.validade || null : null,
    })

    resetForm()
    await carregarDados()
  } catch (e) {
    erro.value = e instanceof Error ? e.message : String(e)
  } finally {
    carregando.value = false
  }
}

watch(
  () => form.value.produtoId,
  (novoId) => {
    if (!novoId) return
    const produtoEncontrado = produtos.value.find((p) => p.id === Number(novoId))

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

    <section class="bg-white p-7 rounded-lg shadow-[0_2px_4px_rgba(0,0,0,0.08)] w-full">
      <div v-if="movimentacoes.length > 0" class="overflow-x-auto">
        <table class="w-full border-collapse text-left text-base">
          <thead>
            <tr>
              <th
                class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-200 align-middle"
              >
                ID
              </th>
              <th
                class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-100 align-middle"
              >
                Tipo
              </th>
              <th
                class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-200 align-middle"
              >
                Produto
              </th>
              <th
                class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-200 align-middle"
              >
                Categoria
              </th>
              <th
                class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-200 align-middle"
              >
                Qtd.
              </th>
              <th
                class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-200 align-middle"
              >
                Preço Un.
              </th>
              <th
                class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-200 align-middle"
              >
                Total Lote
              </th>
              <th
                class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-200 align-middle"
              >
                Data
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in movimentacoes" :key="item.id">
              <td class="px-3 py-3.5 border-b border-gray-200 align-middle">#{{ item.id }}</td>
              <td class="px-3 py-3.5 border-b border-gray-200 align-middle">
                <span
                  :class="[
                    'inline-block whitespace-nowrap py-1 px-2.5 rounded text-sm font-semibold',
                    item.tipo === 'entrada'
                      ? 'bg-green-100 text-[#15803d]'
                      : 'bg-red-100 text-[#b91c1c]',
                  ]"
                >
                  {{ item.tipo.toUpperCase() }}
                </span>
              </td>
              <td class="px-3 py-3.5 border-b border-gray-200 align-middle">
                <strong>{{ getNomeProduto(item.produto_id) }}</strong>
              </td>
              <td class="px-3 py-3.5 border-b border-gray-200 align-middle">
                {{ item.categoriaMovimentacao }}
              </td>
              <td
                :class="
                  item.tipo === 'entrada'
                    ? 'text-[#16a34a] font-semibold'
                    : 'text-red-600 font-semibold'
                "
              >
                {{ item.tipo === 'entrada' ? '+' : '-' }}{{ item.quantidade }}
                {{ item.unidadeMedida }}
              </td>
              <td class="px-3 py-3.5 border-b border-gray-200 align-middle">
                {{ item.precoUnitario ? `R$ ${item.precoUnitario.toFixed(2)}` : '-' }}
              </td>
              <td class="px-3 py-3.5 border-b border-gray-200 align-middle">
                {{
                  item.precoUnitario
                    ? `R$ ${(item.quantidade * item.precoUnitario).toFixed(2)}`
                    : '-'
                }}
              </td>
              <td class="px-3 py-3.5 border-b border-gray-200 align-middle">{{ item.data }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="empty-msg">Nenhuma movimentação registrada.</p>
    </section>

    <BaseModal :is-open="isModalOpen" title="Registrar Movimentação" @close="resetForm">
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

      <p v-if="erro" class="text-red-700 bg-red-100 px-3 py-2 rounded-md text-base">{{ erro }}</p>

      <form class="flex flex-col gap-4" @submit.prevent="salvarMovimentacao">
        <div class="flex flex-col gap-1.5">
          <label class="text-sm font-semibold text-[#334155]"
            >Produto <span class="text-red-500">*</span></label
          >
          <select
            v-model="form.produtoId"
            required
            class="p-2.5 border border-gray-300 outline-none text-base bg-white"
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
          class="mt-2 p-3 bg-[#00bf63] text-white border-none rounded-md font-semibold cursor-pointer transition-colors duration-200 hover:bg-[#01923d] disabled:bg-[#94a3b8] disabled:cursor-not-allowed"
          :disabled="carregando || estoqueInsuficiente"
        >
          {{ carregando ? 'Processando...' : 'Registrar Movimentação' }}
        </button>

        <p
          v-if="estoqueInsuficiente"
          class="text-red-600 bg-red-100 rounded-md text-base py-2 px-3"
          style="margin-top: 0.5rem"
        >
          Quantidade informada é maior que o estoque atual ({{
            produtoSelecionado?.quantidadeEstoque
          }}).
        </p>
      </form>
    </BaseModal>
  </main>
</template>
