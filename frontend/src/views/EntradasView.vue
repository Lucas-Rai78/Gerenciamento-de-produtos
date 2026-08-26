<script setup lang="ts">
import { ref, onMounted } from 'vue';
import type { Produto, EntradaProduto, Classificacao, UnidadeMedida } from '@/types/produto';
import { produtoService } from '@/services/produtoService';
import BaseInput from '@/components/BaseInput.vue';
import BaseSelect from '@/components/BaseSelect.vue';

const classificacoes: Classificacao[] = ['compra', 'producao'];
const unidadesMedida: UnidadeMedida[] = ['g', 'kg', 'mL', 'L'];

const produtos = ref<Produto[]>([]);
const carregando = ref<boolean>(false);

// Tipo explícito para o formulário garantindo compatibilidade com datas e strings vazias
type FormEntrada = Omit<EntradaProduto, 'id' | 'validade'> & { validade: string };

const form = ref<FormEntrada>({
  produtoId: '',
  classificacao: 'compra',
  unidadeMedida: 'kg',
  quantidade: 0,
  precoUnitario: 0,
  dataEntrada: new Date().toISOString().split('T')[0],
  validade: '',
  } as FormEntrada
);

function resetForm(): void {
  form.value = {
    produtoId: '',
    classificacao: 'compra',
    unidadeMedida: 'kg',
    quantidade: 0,
    precoUnitario: 0,
    dataEntrada: new Date().toISOString().split('T')[0],
    validade: '',
  } as FormEntrada;
}

async function carregarProdutos(): Promise<void> {
  try {
    carregando.value = true;
    produtos.value = await produtoService.listar();
  } catch (error) {
    console.error('Erro ao carregar produtos para o select:', error);
  } finally {
    carregando.value = false;
  }
}

async function registrarEntrada(): Promise<void> {
  try {
    carregando.value = true;
    console.log('Registrando entrada:', form.value);
    alert('Entrada registrada com sucesso!');
    resetForm();
  } catch (error) {
    console.error('Erro ao registrar entrada:', error);
  } finally {
    carregando.value = false;
  }
}

onMounted(() => {
  carregarProdutos();
});
</script>

<template>
  <main class="container">
    <section class="card">
      <h2 class="title">Entrada de Produtos</h2>

      <form class="form-grid" @submit.prevent="registrarEntrada">
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
            v-model="form.classificacao"
            label="Classificação"
            :options="classificacoes"
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
          <BaseInput
            v-model.number="form.precoUnitario"
            type="number"
            label="Preço Unitário (R$)"
            step="0.01"
            required
          />
        </div>

        <div class="form-row">
          <BaseInput
            v-model="form.dataEntrada"
            type="date"
            label="Data de Entrada"
            required
          />
          <BaseInput
            v-model="form.validade"
            type="date"
            label="Data de Validade (Opcional)"
          />
        </div>

        <div class="actions">
          <button type="submit" class="btn-primary" :disabled="carregando">
            {{ carregando ? 'Processando...' : 'Registrar Entrada' }}
          </button>
        </div>
      </form>
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
  transition: border-color 0.2s, box-shadow 0.2s;
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
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease, opacity 0.2s;
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