<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Produto, SaidaProduto, MotivoSaida, UnidadeMedida } from '@/types/produto'
import { produtoService } from '@/services/produtoService'
import { movimentacaoService } from '@/services/movimentacaoService'
import BaseInput from '@/components/BaseInput.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import SaidaTable from '@/components/SaidaTable.vue'

const motivosSaida: MotivoSaida[] = ['venda', 'descarte', 'producao']
const unidadesMedida: UnidadeMedida[] = ['g', 'kg', 'mL', 'L']

const produtos = ref<Produto[]>([])
const saidas = ref<SaidaProduto[]>([])
const carregando = ref<boolean>(false)

type FormSaida = Omit<SaidaProduto, 'id'>

const form = ref<FormSaida>({
  produtoId: '',
  motivo: 'venda',
  unidadeMedida: 'kg',
  quantidade: 0,
  dataSaida: new Date().toISOString().split('T')[0],
} as FormSaida)

function resetForm(): void {
  form.value = {
    produtoId: '',
    motivo: 'venda',
    unidadeMedida: 'kg',
    quantidade: 0,
    dataSaida: new Date().toISOString().split('T')[0],
  } as FormSaida
}

async function carregarDados(): Promise<void> {
  try {
    carregando.value = true
    const [listaProdutos, listaSaidas] = await Promise.all([
      produtoService.listar(),
      movimentacaoService.listarSaidas(),
    ])
    produtos.value = listaProdutos
    saidas.value = listaSaidas
  } catch (error) {
    console.error('Erro ao carregar dados de saídas:', error)
  } finally {
    carregando.value = false
  }
}

async function registrarSaida(): Promise<void> {
  try {
    carregando.value = true
    type CriarSaidaPayload = Parameters<typeof movimentacaoService.criarSaida>[0]
    const payload: CriarSaidaPayload = {
      produtoId: form.value.produtoId,
      motivo: form.value.motivo,
      unidadeMedida: form.value.unidadeMedida,
      quantidade: form.value.quantidade,
      dataSaida: form.value.dataSaida,
    }

    await movimentacaoService.criarSaida(payload)
    resetForm()
    await carregarDados()
  } catch (error) {
    console.error('Erro ao registrar saída:', error)
  } finally {
    carregando.value = false
  }
}

onMounted(() => {
  carregarDados()
})
</script>

<template>
  <main class="container">
    <!-- Formulário -->
    <section class="card">
      <h2 class="title">Saída de Produtos</h2>

      <form class="form-grid" @submit.prevent="registrarSaida">
        <div class="select-group">
          <label class="select-label">Produto <span class="required-asterisk">*</span></label>
          <select v-model="form.produtoId" required class="select-field">
            <option value="" disabled selected>Selecione um produto</option>
            <option v-for="prod in produtos" :key="prod.id" :value="prod.id">
              {{ prod.nome }} (Estoque atual: {{ prod.quantidadeEstoque }})
            </option>
          </select>
        </div>

        <div class="form-row">
          <BaseSelect
            v-model="form.motivo"
            label="Motivo da Saída"
            :options="motivosSaida"
            required
          />
          <BaseSelect
            v-model="form.unidadeMedida"
            label="Unidade de Medida"
            :options="unidadesMedida"
            required
          />
        </div>

        <div class="form-row">
          <BaseInput
            v-model.number="form.quantidade"
            type="number"
            label="Quantidade"
            step="any"
            required
          />
          <BaseInput v-model="form.dataSaida" type="date" label="Data de Saída" required />
        </div>

        <div class="actions">
          <button type="submit" class="btn-primary" :disabled="carregando">
            {{ carregando ? 'Processando...' : 'Registrar Saída' }}
          </button>
        </div>
      </form>
    </section>

    <!-- Tabela de Histórico -->
    <SaidaTable :saidas="saidas" :produtos="produtos" :carregando="carregando" />
  </main>
</template>

<style scoped>
.container {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.card {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}
.title {
  color: #121212;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  border-left: 4px solid #00bf63;
  padding-left: 0.5rem;
}
.form-grid {
  display: flex;
  flex-direction: column;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.select-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  margin-bottom: 1rem;
}
.select-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #121212;
}
.required-asterisk {
  color: #ef4444;
}
.select-field {
  padding: 0.625rem 0.75rem;
  border: 1px solid #d4d4d4;
  border-radius: 0.375rem;
  font-size: 0.95rem;
  background-color: #ffffff;
  outline: none;
}
.select-field:focus {
  border-color: #00bf63;
  box-shadow: 0 0 0 3px rgba(0, 191, 99, 0.15);
}
.actions {
  display: flex;
  margin-top: 0.5rem;
}
.btn-primary {
  flex: 1;
  padding: 0.75rem;
  background-color: #00bf63;
  color: #121212;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
}
.btn-primary:hover:not(:disabled) {
  background-color: #01923d;
  color: #ffffff;
}
.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
