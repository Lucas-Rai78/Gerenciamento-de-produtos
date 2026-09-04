<script setup lang="ts">
import type { ProdutoCreate, Categoria, UnidadeMedida } from '@/types/produto'
import BaseInput from '@/components/BaseInput.vue'
import BaseSelect from '@/components/BaseSelect.vue'

interface Props {
  isEditing: boolean
  categorias: Categoria[]
  unidadesMedida: UnidadeMedida[]
}

defineProps<Props>()

const form = defineModel<ProdutoCreate>({ required: true })

const emit = defineEmits<{
  (e: 'salvar'): void
  (e: 'cancelar'): void
}>()
</script>

<template>
  <section class="bg-white p-6 rounded-lg shadow-[0_2px_4px_rgba(0,0,0,0.08)]">
    <h2 class="text-black text-xl font-semibold mb-5 border-l-4 border-[#00bf63] pl-2">
      {{ isEditing ? 'Editar Produto' : 'Cadastro de Produtos' }}
    </h2>

    <form class="flex flex-col gap-4 w-full" @submit.prevent="emit('salvar')">
      <BaseInput v-model="form.nome" label="Nome do Produto" required />
      <BaseInput v-model="form.descricao" label="Descrição" required />

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
        <BaseSelect v-model="form.categoria" label="Categoria" :options="categorias" required />
        <BaseSelect
          v-model="form.peso"
          label="Unidade de Medida"
          :options="unidadesMedida"
          required
        />
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
        <BaseInput
          v-model.number="form.precoUnidade"
          type="number"
          label="Preço Unitário (R$)"
          step="0.01"
          required
        />
        <BaseInput
          v-model.number="form.quantidadeEstoque"
          type="number"
          label="Estoque Inicial"
          required
        />
      </div>

      <BaseInput
        v-model.number="form.estoqueMinimo"
        type="number"
        label="Estoque Mínimo"
        required
      />

      <div class="flex gap-2 mt-2 w-full">
        <button type="submit" class="flex-1 py-3 bg-[#00bf63] text-white border-none rounded-md font-semibold text-base cursor-pointer transition-colors duration-200 hover:bg-[#01923d] hover:text-white">
          {{ isEditing ? 'Atualizar Produto' : 'Cadastrar Produto' }}
        </button>
        <button v-if="isEditing" type="button" class="py-3 px-4 bg-[#64748b] border-none rounded-md font-semibold cursor-pointer" @click="emit('cancelar')">
          Cancelar
        </button>
      </div>
    </form>
  </section>
</template>
