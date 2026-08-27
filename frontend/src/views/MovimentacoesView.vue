<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Produto, UnidadeMedida } from '@/types/produto'
import { produtoService } from '@/services/produtoService'
import { movimentacaoService, type Movimentacao } from '@/services/movimentacaoService'
import BaseInput from '@/components/BaseInput.vue'
import BaseSelect from '@/components/BaseSelect.vue'

const unidadesMedida: UnidadeMedida[] = ['g', 'kg', 'mL', 'L']
const opcoesEntrada = ['compra', 'producao']
const opcoesSaida = ['venda', 'descarte', 'producao']

const produtos = ref<Produto[]>([])
const movimentacoes = ref<Movimentacao[]>([])
const carregando = ref<boolean>(false)
const erro = ref<string>('')

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
      precoUnitario: form.value.tipo === 'entrada' ? form.value.precoUnitario : 0,
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

onMounted(() => {
  carregarDados()
})
</script>

<template>
  <main class="container">
    <section class="card">
      <h2 class="title">Gerenciador de Movimentações</h2>

      <!-- Seletor Entrada / Saída -->
      <div class="toggle-container">
        <button
          type="button"
          :class="['toggle-btn', { active: form.tipo === 'entrada' }]"
          @click="alterarTipo('entrada')"
        >
          + Entrada
        </button>
        <button
          type="button"
          :class="['toggle-btn', 'btn-out', { active: form.tipo === 'saida' }]"
          @click="alterarTipo('saida')"
        >
          - Saída
        </button>
      </div>

      <p v-if="erro" class="error-banner">{{ erro }}</p>

      <form class="form-grid" @submit.prevent="salvarMovimentacao">
        <div class="select-group">
          <label class="select-label">Produto <span class="required">*</span></label>
          <select v-model="form.produtoId" required class="select-field">
            <option value="" disabled selected>Selecione um produto</option>
            <option v-for="prod in produtos" :key="prod.id" :value="prod.id">
              {{ prod.nome }} (Estoque: {{ prod.quantidadeEstoque }})
            </option>
          </select>
        </div>

        <div class="form-row">
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

        <div class="form-row">
          <BaseInput
            v-model.number="form.quantidade"
            type="number"
            label="Quantidade"
            step="any"
            :min="1"
            required
          />
          <BaseInput
            v-if="form.tipo === 'entrada'"
            v-model.number="form.precoUnitario"
            type="number"
            label="Preço Unitário (R$)"
            step="0.01"
            required
          />
          <BaseInput v-model="form.data" type="date" label="Data" required />
          <div v-if="form.tipo === 'entrada'">
            <BaseInput v-model="form.validade" type="date" label="Validade (Opcional)" />
          </div>
        </div>


        <button type="submit" class="btn-submit" :disabled="carregando">
          {{ carregando ? 'Processando...' : 'Registrar Movimentação' }}
        </button>
      </form>
    </section>

    <!-- Tabela Unificada de Movimentações -->
    <section class="card">
      <h3 class="subtitle">Histórico do Estoque</h3>

      <div v-if="movimentacoes.length > 0" class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Tipo</th>
              <th>Produto</th>
              <th>Categoria</th>
              <th>Qtd.</th>
              <th>Preço Un.</th>
              <th>Total Lote</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in movimentacoes" :key="item.id">
              <td>#{{ item.id }}</td>
              <td>
                <span :class="['badge', item.tipo === 'entrada' ? 'badge-in' : 'badge-out']">
                  {{ item.tipo.toUpperCase() }}
                </span>
              </td>
              <td>
                <strong>{{ getNomeProduto(item.produto_id) }}</strong>
              </td>
              <td>{{ item.categoriaMovimentacao }}</td>
              <td :class="item.tipo === 'entrada' ? 'text-in' : 'text-out'">
                {{ item.tipo === 'entrada' ? '+' : '-' }}{{ item.quantidade }}
                {{ item.unidadeMedida }}
              </td>
              <td>{{ item.precoUnitario ? `R$ ${item.precoUnitario.toFixed(2)}` : '-' }}</td>
              <td>
                {{
                  item.tipo === 'entrada' && item.precoUnitario
                    ? `R$ ${(item.quantidade * item.precoUnitario).toFixed(2)}`
                    : '-'
                }}
              </td>
              <td>{{ item.data }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="empty-msg">Nenhuma movimentação registrada.</p>
    </section>
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
  background: #fff;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}
.title {
  font-size: 1.25rem;
  font-weight: 600;
  border-left: 4px solid #00bf63;
  padding-left: 0.5rem;
  margin-bottom: 1rem;
}
.subtitle {
  font-size: 1.1rem;
  margin-bottom: 1rem;
}
.toggle-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}
.toggle-btn {
  flex: 1;
  padding: 0.6rem;
  border: 1px solid #d4d4d4;
  background: #f8fafc;
  cursor: pointer;
  border-radius: 0.375rem;
  font-weight: 600;
  color: #64748b;
}
.toggle-btn.active {
  background-color: #00bf63;
  color: #fff;
  border-color: #00bf63;
}
.toggle-btn.btn-out.active {
  background-color: #ef4444;
  color: #fff;
  border-color: #ef4444;
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
}
.required {
  color: #ef4444;
}
.select-field {
  padding: 0.625rem;
  border: 1px solid #d4d4d4;
  border-radius: 0.375rem;
  outline: none;
}
.btn-submit {
  margin-top: 1rem;
  padding: 0.75rem;
  background: #00bf63;
  color: #fff;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  cursor: pointer;
}
.btn-submit:hover {
  background: #01923d;
}
.table-responsive {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.9rem;
}
th,
td {
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}
.badge {
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: bold;
}
.badge-in {
  background-color: #dcfce7;
  color: #15803d;
}
.badge-out {
  background-color: #fee2e2;
  color: #b91c1c;
}
.text-in {
  color: #16a34a;
  font-weight: 600;
}
.text-out {
  color: #dc2626;
  font-weight: 600;
}
.error-banner {
  color: #b91c1c;
  background: #fee2e2;
  padding: 0.5rem;
  border-radius: 0.25rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
.empty-msg {
  text-align: center;
  color: #64748b;
  padding: 1rem 0;
}
</style>
