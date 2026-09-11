<script setup lang="ts">
import type { Movimentacao } from '@/movimentacoes_modules/services/movimentacaoService'
import type { Produto } from '@/produto_modules/types/produto'
import { useMovimentacoesTable } from '@/movimentacoes_modules/composables/useMovimentacoesTable'

const props = defineProps<{
  movimentacoes: Movimentacao[]
  produtos: Produto[]
}>()

const { getNomeProduto } = useMovimentacoesTable(props)
</script>

<template>
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
              class="text-[#475569] font-semibold px-3 py-3.5 border-b border-gray-200 align-middle"
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
                    : 'bg-red-100 text-red-600',
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
                item.precoUnitario ? `R$ ${(item.quantidade * item.precoUnitario).toFixed(2)}` : '-'
              }}
            </td>
            <td class="px-3 py-3.5 border-b border-gray-200 align-middle">{{ item.data }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p v-else class="text-center text-gray-500 my-4">Nenhuma movimentação registrada.</p>
  </section>
</template>
