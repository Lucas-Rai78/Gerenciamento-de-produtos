<script setup lang="ts">
import type { Produto } from '@/types/produto'

defineProps<{
  produtos: Produto[]
  carregando: boolean
}>()

const emit = defineEmits<{
  (e: 'editar', produto: Produto): void
  (e: 'excluir', id: number): void
}>()
</script>

<template>
  <section class="bg-white p-6 rounded-lg shadow-[0_2px_4px_rgba(0,0,0,0.08)]">
    <h3 class="text-[#121212] text-lg font-semibold mb-4">Lista de Produtos</h3>

    <div v-if="carregando" class="text-[#64748b] text-sm text-center py-4">
      Carregando produtos...
    </div>

    <div v-else-if="produtos.length > 0" class="overflow-x-auto">
      <table class="w-full border-collapse text-center text-md">
        <thead>
          <tr class="text-[#475569] font-semibold">
            <th class="py-3 px-2 border-b border-gray-200 text-[#475569] font-semibold">ID</th>
            <th class="py-3 px-2 border-b border-gray-200 text-[#475569] font-semibold">Nome</th>
            <th class="py-3 px-2 border-b border-gray-200 text-[#475569] font-semibold">Categoria</th>
            <th class="py-3 px-2 border-b border-gray-200 text-[#475569] font-semibold">Preço Un.</th>
            <th class="py-3 px-2 border-b border-gray-200 text-[#475569] font-semibold">Estoque</th>
            <th class="py-3 px-2 border-b border-gray-200 text-[#475569] font-semibold">Medida</th>
            <th class="py-3 px-2 border-b border-gray-200 text-[#475569] font-semibold">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prod in produtos" :key="prod.id">
            <td class="py-3 px-2 border-b border-gray-200">#{{ prod.id }}</td>
            <td class="py-3 px-2 border-b border-gray-200">
              <strong class="font-semibold text-gray-900">{{ prod.nome }}</strong>
              <span class="block text-[0.75rem] text-[#64748b]">{{ prod.descricao }}</span>
            </td>
            <td class="py-3 px-2 border-b border-gray-200">
              <span class="inline-block bg-gray-200 text-gray-900 px-2 py-0.5 rounded text-sm font-medium">
                {{ prod.categoria }}
              </span>
            </td>
            <td class="py-3 px-2 border-b border-gray-200">R$ {{ prod.precoUnidade.toFixed(2) }}</td>
            <td
              class="py-3 px-2 border-b border-gray-200"
              :class="{ 'text-red-500 font-semibold': prod.quantidadeEstoque <= prod.estoqueMinimo }"
            >
              {{ prod.quantidadeEstoque }}
            </td>
            <td class="py-3 px-2 border-b border-gray-200">{{ prod.peso }}</td>
            <td class="py-3 px-2 border-b border-gray-200">
              <div class="flex gap-1 items-center justify-center">
                <button
                  class="bg-transparent border-2 border-orange-400 text-orange-400 hover:bg-orange-400 hover:text-white rounded cursor-pointer px-2! py-1! text-base shadow-[0_2px_4px_rgba(0,0,0,0.08)] transition-all duration-150 font-medium"
                  title="Editar"
                  @click="emit('editar', prod)"
                >
                  Editar
                </button>
                <button
                  class="bg-transparent border-2 text-red-600 border-red-600 hover:bg-red-600 hover:text-white rounded cursor-pointer px-2! py-1! text-base shadow-[0_2px_4px_rgba(0,0,0,0.08)] transition-all duration-150 font-medium"
                  title="Excluir"
                  @click="emit('excluir', prod.id)"
                >
                  Excluir
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-[#64748b] text-sm text-center py-4">
      Nenhum produto cadastrado no banco.
    </p>
  </section>
</template>
