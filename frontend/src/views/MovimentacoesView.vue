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
  }
)

onMounted(() => {
  carregarDados()
})
</script>

<template>
  <main class="container">
    <!-- Cabeçalho da página -->
    <div class="page-header">
      <h2 class="title">Histórico de Movimentações</h2>
      <button type="button" class="btn-primary" @click="isModalOpen = true">
        + Registrar Movimentação
      </button>
    </div>

    <!-- Tabela principal -->
    <section class="card table-card">
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
                  item.precoUnitario
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

    <!-- Modal com o Formulário -->
    <BaseModal :is-open="isModalOpen" title="Registrar Movimentação" @close="resetForm">
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
            v-model.number="form.precoUnitario"
            type="number"
            label="Preço Unitário (R$)"
            step="0.01"
            required
          />
        </div>

        <div class="form-row">
          <BaseInput v-model="form.data" type="date" label="Data" required />
          <BaseInput
            v-if="form.tipo === 'entrada'"
            v-model="form.validade"
            type="date"
            label="Validade (Opcional)"
          />
        </div>

        <button type="submit" class="btn-submit" :disabled="carregando || estoqueInsuficiente">
          {{ carregando ? 'Processando...' : 'Registrar Movimentação' }}
        </button>

        <p v-if="estoqueInsuficiente" class="error-banner" style="margin-top: 0.5rem">
          Quantidade informada é maior que o estoque atual ({{
            produtoSelecionado?.quantidadeEstoque
          }}).
        </p>
      </form>
    </BaseModal>
  </main>
</template>

<style scoped>
.container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  color: #121212;
  font-size: 1.5rem;
  font-weight: 600;
  border-left: 4px solid #00bf63;
  padding-left: 0.5rem;
  margin: 0;
}

.card {
  background: #ffffff;
  padding: 1.75rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.table-card {
  width: 100%;
}

.btn-primary {
  padding: 0.75rem 1.25rem;
  background-color: #00bf63;
  color: #fff;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-primary:hover {
  background-color: #01923d;
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
  transition: all 0.2s ease;
}

.toggle-btn.active {
  background-color: #00bf63;
  color: #ffffff;
  border-color: #00bf63;
}

.toggle-btn.btn-out.active {
  background-color: #ef4444;
  color: #ffffff;
  border-color: #ef4444;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
}

.select-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #334155;
}

.required {
  color: #ef4444;
}

.select-field {
  padding: 0.625rem;
  border: 1px solid #d4d4d4;
  border-radius: 0.375rem;
  outline: none;
  font-size: 0.95rem;
  background-color: #fff;
}

.btn-submit {
  margin-top: 0.5rem;
  padding: 0.75rem;
  background-color: #00bf63;
  color: #ffffff;
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-submit:hover {
  background-color: #01923d;
}

.btn-submit:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
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
  padding: 0.875rem 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  vertical-align: middle;
}

th {
  color: #475569;
  font-weight: 600;
  white-space: nowrap;
}

.badge {
  display: inline-block;
  white-space: nowrap;
  padding: 0.25rem 0.6rem;
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
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.9rem;
}

.empty-msg {
  color: #64748b;
  font-size: 0.9rem;
  text-align: center;
  padding: 1rem 0;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
