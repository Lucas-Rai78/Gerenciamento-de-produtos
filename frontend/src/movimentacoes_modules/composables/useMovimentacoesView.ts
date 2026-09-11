import { ref, onMounted } from 'vue'
import type { Produto } from '@/produto_modules/types/produto'
import { produtoService } from '@/produto_modules/services/produtoService'
import {
  movimentacaoService,
  type Movimentacao,
} from '@/movimentacoes_modules/services/movimentacaoService'

export function useMovimentacoes() {
  const produtos = ref<Produto[]>([])
  const movimentacoes = ref<Movimentacao[]>([])
  const carregando = ref<boolean>(false)
  const erro = ref<string>('')
  const isModalOpen = ref<boolean>(false)

  async function carregarDados(): Promise<void> {
    try {
      carregando.value = true
      erro.value = ''
      const [prods, movs] = await Promise.all([
        produtoService.listar(),
        movimentacaoService.listar(),
      ])
      produtos.value = prods
      movimentacoes.value = movs
    } catch (e) {
      erro.value = `Falha ao carregar dados: ${e instanceof Error ? e.message : String(e)}`
    } finally {
      carregando.value = false
    }
  }

  async function salvarMovimentacao(dados: Omit<Movimentacao, 'id'>): Promise<void> {
    try {
      carregando.value = true
      erro.value = ''

      await movimentacaoService.criar(dados)
      isModalOpen.value = false
      await carregarDados()
    } catch (e) {
      erro.value = e instanceof Error ? e.message : String(e)
    } finally {
      carregando.value = false
    }
  }

  function abrirModal(): void {
    erro.value = ''
    isModalOpen.value = true
  }

  function fecharModal(): void {
    erro.value = ''
    isModalOpen.value = false
  }

  onMounted(() => {
    carregarDados()
  })

  return {
    produtos,
    movimentacoes,
    carregando,
    erro,
    isModalOpen,
    carregarDados,
    salvarMovimentacao,
    abrirModal,
    fecharModal,
  }
}
