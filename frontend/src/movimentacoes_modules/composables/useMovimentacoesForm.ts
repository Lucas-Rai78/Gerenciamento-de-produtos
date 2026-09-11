import { ref, computed, watch } from 'vue'
import type { Produto, UnidadeMedida } from '@/produto_modules/types/produto'
import type { Movimentacao } from '@/movimentacoes_modules/services/movimentacaoService'

interface UseMovimentacaoFormProps {
  isOpen: boolean
  produtos: Produto[]
}

interface UseMovimentacaoFormEmits {
  (e: 'close'): void
  (e: 'salvar', dados: Omit<Movimentacao, 'id'>): void
}

const UNIDADES_MEDIDA: UnidadeMedida[] = ['g', 'kg', 'mL', 'L']
const OPCOES_ENTRADA = ['compra', 'producao']
const OPCOES_SAIDA = ['venda', 'descarte', 'producao']

function criarFormularioVazio() {
  return {
    produtoId: '',
    tipo: 'entrada' as 'entrada' | 'saida',
    categoriaMovimentacao: 'compra',
    unidadeMedida: 'kg',
    quantidade: 1,
    precoUnitario: 0,
    data: new Date().toISOString().split('T')[0] ?? '',
    validade: '',
  }
}

export function useMovimentacaoForm(props: UseMovimentacaoFormProps, emit: UseMovimentacaoFormEmits) {
  const form = ref(criarFormularioVazio())

  const categoriasDisponiveis = computed(() => {
    return form.value.tipo === 'entrada' ? OPCOES_ENTRADA : OPCOES_SAIDA
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
    form.value = criarFormularioVazio()
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
          UNIDADES_MEDIDA.includes(produtoEncontrado.peso as UnidadeMedida)
        ) {
          form.value.unidadeMedida = produtoEncontrado.peso as UnidadeMedida
        }
      }
    },
  )

  watch(
    () => props.isOpen,
    (novoEstado) => {
      if (!novoEstado) {
        resetForm()
      }
    },
  )

  return {
    form,
    unidadesMedida: UNIDADES_MEDIDA,
    categoriasDisponiveis,
    produtoSelecionado,
    estoqueInsuficiente,
    alterarTipo,
    fecharModal,
    handleSubmit,
  }
}
